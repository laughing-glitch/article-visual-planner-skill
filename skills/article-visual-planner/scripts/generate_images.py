#!/usr/bin/env python3
"""Generate article images from an article-visual-planner Markdown prompt file.

This script intentionally uses only the Python standard library for API calls.
Pillow is optional; it is only required when final pixel normalization is requested.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_OPENAI_MODEL = "gpt-image-1"
DEFAULT_GOOGLE_MODEL = "gemini-3.1-flash-image"
DEFAULT_RELAY_MODEL = "gpt-image-1"


@dataclass
class ImageJob:
    index: int
    title: str
    prompt: str
    ratio: str
    final_size: tuple[int, int] | None
    kind: str


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def slugify(value: str, max_len: int = 48) -> str:
    value = value.strip().lower()
    value = re.sub(r"[\\/:*?\"<>|]+", "-", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        value = "image"
    return value[:max_len].strip("-") or "image"


def parse_size(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"\s*(\d+)\s*[xX*]\s*(\d+)\s*", value)
    if not match:
        raise argparse.ArgumentTypeError("Size must look like WIDTHxHEIGHT")
    width = int(match.group(1))
    height = int(match.group(2))
    if width < 64 or height < 64:
        raise argparse.ArgumentTypeError("Size must be at least 64x64")
    return width, height


def parse_ratio(value: str) -> str:
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)\s*", value)
    if not match:
        raise argparse.ArgumentTypeError("Ratio must look like 2.35:1 or 16:9")
    width = float(match.group(1))
    height = float(match.group(2))
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("Ratio numbers must be positive")
    return f"{match.group(1)}:{match.group(2)}"


def optional_size(value: str | None) -> tuple[int, int] | None:
    if not value:
        return None
    return parse_size(value)


def parse_prompt_file(
    path: Path,
    cover_ratio: str,
    body_ratio: str,
    cover_final_size: tuple[int, int] | None,
    body_final_size: tuple[int, int] | None,
) -> list[ImageJob]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    jobs: list[ImageJob] = []

    for i, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end].strip()

        if heading.startswith(("视觉策划", "全局风格", "使用方式")):
            continue
        if not (heading.startswith("封面图") or heading.startswith("正文配图")):
            continue
        if not section:
            continue

        kind = "cover" if heading.startswith("封面图") else "body"
        ratio = cover_ratio if kind == "cover" else body_ratio
        final_size = cover_final_size if kind == "cover" else body_final_size
        jobs.append(
            ImageJob(
                index=len(jobs) + 1,
                title=heading,
                prompt=strip_markdown_fences(section),
                ratio=ratio,
                final_size=final_size,
                kind=kind,
            )
        )

    if not jobs:
        raise ValueError(
            "No image prompt sections found. Expected headings like '## 封面图 - ...' or '## 正文配图1 - ...'."
        )
    return jobs


def strip_markdown_fences(text: str) -> str:
    stripped = text.strip()
    fence = re.fullmatch(r"```(?:text|markdown)?\n(.*?)\n```", stripped, re.DOTALL)
    if fence:
        return fence.group(1).strip()
    return stripped


def http_json(url: str, headers: dict[str, str], payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed for {url}: {exc}") from exc


def generate_openai(job: ImageJob, args: argparse.Namespace, api_key: str) -> bytes:
    base_url = args.base_url.rstrip("/") if args.base_url else "https://api.openai.com/v1"
    payload: dict[str, Any] = {
        "model": args.model or DEFAULT_OPENAI_MODEL,
        "prompt": prompt_with_ratio(job),
        "quality": args.quality,
        "n": 1,
    }
    if args.api_size:
        payload["size"] = args.api_size
    if args.output_format:
        payload["output_format"] = args.output_format
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = http_json(f"{base_url}/images/generations", headers, payload, args.timeout)
    try:
        b64 = data["data"][0]["b64_json"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Could not find base64 image data in OpenAI response: {data}") from exc
    return base64.b64decode(b64)


def generate_google(job: ImageJob, args: argparse.Namespace, api_key: str) -> bytes:
    model = args.model or DEFAULT_GOOGLE_MODEL
    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_with_ratio(job)}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["Image"],
            "responseFormat": {
                "image": {
                    "aspectRatio": job.ratio,
                    "imageSize": args.google_image_size,
                }
            },
        },
    }
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }
    data = http_json(url, headers, payload, args.timeout)
    for candidate in data.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"])
    raise RuntimeError(f"Could not find inline image data in Google response: {data}")


def prompt_with_ratio(job: ImageJob) -> str:
    return (
        job.prompt
        + f"\n\nGenerate one final image using aspect ratio {job.ratio}. "
        + "Prioritize matching this ratio over a fixed pixel size."
    )


def generate_relay(job: ImageJob, args: argparse.Namespace, api_key: str) -> bytes:
    if not args.base_url:
        raise ValueError("--base-url is required when --provider relay")
    relay_args = argparse.Namespace(**vars(args))
    relay_args.model = args.model or DEFAULT_RELAY_MODEL
    return generate_openai(job, relay_args, api_key)


def save_raw_image(image_bytes: bytes, path: Path) -> None:
    path.write_bytes(image_bytes)


def fit_image(input_path: Path, output_path: Path, target_size: tuple[int, int]) -> None:
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is required for final resizing. Install it with: python -m pip install pillow"
        ) from exc

    with Image.open(input_path) as image:
        image = image.convert("RGB")
        target_w, target_h = target_size
        src_w, src_h = image.size
        target_ratio = target_w / target_h
        src_ratio = src_w / src_h

        if src_ratio > target_ratio:
            new_w = int(src_h * target_ratio)
            left = (src_w - new_w) // 2
            box = (left, 0, left + new_w, src_h)
        else:
            new_h = int(src_w / target_ratio)
            top = (src_h - new_h) // 2
            box = (0, top, src_w, top + new_h)

        image = image.crop(box).resize(target_size)
        image.save(output_path, format="PNG")


def resolve_api_key(args: argparse.Namespace) -> str:
    env_name = args.api_key_env
    if not env_name:
        if args.provider == "openai":
            env_name = "OPENAI_API_KEY"
        elif args.provider == "google":
            env_name = "GOOGLE_API_KEY"
        else:
            env_name = "OPENAI_API_KEY"
    api_key = os.environ.get(env_name)
    if not api_key:
        raise RuntimeError(f"Missing API key. Set environment variable {env_name}.")
    return api_key


def write_manifest(path: Path, records: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate images from an article visual prompt Markdown file.")
    parser.add_argument("--prompts-file", required=True, type=Path, help="Markdown file generated by article-visual-planner.")
    parser.add_argument("--provider", choices=["openai", "google", "relay"], default="openai")
    parser.add_argument("--model", help="Provider model name.")
    parser.add_argument("--base-url", help="OpenAI-compatible base URL for relay providers.")
    parser.add_argument("--api-key-env", help="Environment variable containing the API key.")
    parser.add_argument("--output-dir", type=Path, default=Path("generated-images"))
    parser.add_argument("--cover-ratio", type=parse_ratio, default="2.35:1")
    parser.add_argument("--body-ratio", type=parse_ratio, default="16:9")
    parser.add_argument(
        "--cover-final-size",
        type=optional_size,
        help="Optional final pixel size for local normalization, for example WIDTHxHEIGHT.",
    )
    parser.add_argument(
        "--body-final-size",
        type=optional_size,
        help="Optional final pixel size for local normalization, for example WIDTHxHEIGHT.",
    )
    parser.add_argument(
        "--api-size",
        help="Optional provider-specific OpenAI/relay size. Leave empty to request by ratio in the prompt.",
    )
    parser.add_argument("--google-image-size", default="1K", help="Google image size hint, for example 1K, 2K, or 4K.")
    parser.add_argument("--quality", default="medium", choices=["low", "medium", "high", "auto"])
    parser.add_argument("--output-format", default="png", choices=["png", "jpeg", "webp"])
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds to wait between jobs.")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--limit", type=int, help="Generate only the first N images.")
    parser.add_argument("--dry-run", action="store_true", help="Parse and print jobs without calling APIs.")
    parser.add_argument("--keep-raw", action="store_true", help="Keep raw provider images before final crop.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        jobs = parse_prompt_file(
            args.prompts_file,
            args.cover_ratio,
            args.body_ratio,
            args.cover_final_size,
            args.body_final_size,
        )
        if args.limit:
            jobs = jobs[: args.limit]

        print(f"Found {len(jobs)} image job(s).")
        for job in jobs:
            suffix = f", normalize to {job.final_size[0]}x{job.final_size[1]}" if job.final_size else ""
            print(f"- {job.index:02d} {job.title} -> ratio {job.ratio}{suffix}")

        if args.dry_run:
            return 0

        api_key = resolve_api_key(args)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        raw_dir = args.output_dir / "_raw"
        if args.keep_raw:
            raw_dir.mkdir(parents=True, exist_ok=True)

        manifest: list[dict[str, Any]] = []
        for offset, job in enumerate(jobs):
            print(f"\nGenerating {job.index:02d}: {job.title}")
            if args.provider == "openai":
                image_bytes = generate_openai(job, args, api_key)
            elif args.provider == "google":
                image_bytes = generate_google(job, args, api_key)
            else:
                image_bytes = generate_relay(job, args, api_key)

            filename = f"{job.index:02d}-{job.kind}-{slugify(job.title)}.png"
            final_path = args.output_dir / filename
            if job.final_size:
                raw_path = raw_dir / filename if args.keep_raw else args.output_dir / f".raw-{filename}"
                save_raw_image(image_bytes, raw_path)
                fit_image(raw_path, final_path, job.final_size)
                if not args.keep_raw:
                    raw_path.unlink(missing_ok=True)
            else:
                save_raw_image(image_bytes, final_path)

            record = {
                "index": job.index,
                "title": job.title,
                "kind": job.kind,
                "provider": args.provider,
                "model": args.model,
                "ratio": job.ratio,
                "final_size": f"{job.final_size[0]}x{job.final_size[1]}" if job.final_size else None,
                "path": str(final_path),
            }
            manifest.append(record)
            print(f"Saved: {final_path}")
            if offset < len(jobs) - 1 and args.sleep > 0:
                time.sleep(args.sleep)

        write_manifest(args.output_dir / "manifest.json", manifest)
        print(f"\nDone. Manifest: {args.output_dir / 'manifest.json'}")
        return 0
    except Exception as exc:
        eprint(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
