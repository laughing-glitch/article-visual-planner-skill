#!/usr/bin/env python3
"""Check automatic image generation configuration."""

from __future__ import annotations

import argparse
import os
import sys


def default_env(provider: str) -> str:
    if provider == "google":
        return "GOOGLE_API_KEY"
    return "OPENAI_API_KEY"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check API key configuration for article image generation.")
    parser.add_argument("--provider", choices=["openai", "google", "relay"], default="openai")
    parser.add_argument("--api-key-env")
    parser.add_argument("--base-url")
    args = parser.parse_args()

    env_name = args.api_key_env or default_env(args.provider)
    ok = True

    if os.environ.get(env_name):
        print(f"OK: {env_name} is set.")
    else:
        print(f"Missing: {env_name} is not set.")
        ok = False

    if args.provider == "relay":
        if args.base_url:
            print(f"OK: relay base URL is {args.base_url}")
        else:
            print("Missing: --base-url is required for relay providers.")
            ok = False

    try:
        import PIL  # noqa: F401

        print("OK: Pillow is installed for final image resizing.")
    except ImportError:
        print("Missing: Pillow is required for final resizing. Install with: python -m pip install pillow")
        ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
