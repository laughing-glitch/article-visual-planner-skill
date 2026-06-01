# API Options For Automatic Image Generation

Automatic drawing is optional. Always remind the user they can use manual drawing with the generated prompts.

The built-in lightweight path uses:

```text
scripts/check_config.py
scripts/generate_images.py
```

## Choice Flow

Ask the user to choose:

```text
你想用哪种方式自动绘图？
A. OpenAI API Key
B. Google AI Studio API Key
C. 中转站 API Key（OpenAI-compatible）
```

## Dry Run First

Always preview the parsed jobs before spending API credits:

```bash
python scripts/generate_images.py --prompts-file "文章配图提示词.md" --dry-run
```

## OpenAI API Key

Use when the user has an OpenAI API key and wants OpenAI image generation.

Collect:

- API key environment variable name, default `OPENAI_API_KEY`
- Model name, default `gpt-image-1`
- Output folder

Never ask the user to paste secrets into article files or prompt files.

Example:

```bash
export OPENAI_API_KEY="你的 Key"
python scripts/check_config.py --provider openai
python scripts/generate_images.py --prompts-file "文章配图提示词.md" --provider openai --output-dir outputs
```

## Google AI Studio API Key

Use when the user has a Google AI Studio key.

Collect:

- API key environment variable name, default `GOOGLE_API_KEY`
- Model name, default `gemini-3.1-flash-image`
- Output folder

Example:

```bash
export GOOGLE_API_KEY="你的 Key"
python scripts/check_config.py --provider google
python scripts/generate_images.py --prompts-file "文章配图提示词.md" --provider google --output-dir outputs
```

## Relay / OpenAI-Compatible API

Use when the user has a relay endpoint.

Collect:

- API key environment variable name
- Base URL
- Model name
- Output folder

Example:

```bash
export OPENAI_API_KEY="你的中转站 Key"
python scripts/check_config.py --provider relay --base-url "https://example.com/v1"
python scripts/generate_images.py --prompts-file "文章配图提示词.md" --provider relay --base-url "https://example.com/v1" --model "你的模型名" --output-dir outputs
```

## Ratio Behavior

- Cover prompts default to `2.35:1`.
- Body prompts default to `16:9`.
- The script passes each target ratio to providers by default.
- For Google, the script passes the target aspect ratio and a clarity-level hint.
- For OpenAI-compatible providers, the script writes the target ratio into the prompt and only passes a provider-specific size if the user explicitly sets `--api-size`.
- If the user explicitly needs fixed pixel exports, they can use optional local normalization flags. Do not introduce these flags in the normal beginner flow.

## Safety

- Do not hard-code API keys into scripts or Markdown output.
- Prefer environment variables.
- Keep `--dry-run` as the first step for new users.
