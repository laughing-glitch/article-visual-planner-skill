---
name: article-visual-planner
description: 根据文章内容设计公众号文章封面图和正文配图提示词的视觉策划 Skill。Use when the user asks to turn an article, draft, markdown file,公众号文章, blog post, or long-form content into image prompts, cover image prompts, article illustrations,正文配图, or a unified visual plan. Also use when the user uploads one or more reference images and asks to analyze, imitate, migrate, or apply the image style to article visuals.
---

# Article Visual Planner

## Purpose

Turn an article into a visual plan and a structured Markdown prompt file for:

- 1 WeChat Official Account cover image: default ratio `2.35:1`
- Multiple body illustrations with one unified ratio, default `16:9`
- Optional reference-image style analysis before prompt writing
- Optional manual or API-based image generation after prompts are ready

Core principle: do not merely generate pretty image prompts. First decide how images help the article be clicked, understood, trusted, and remembered.

## References

Load only what is needed:

- Read `references/visual-strategy.md` before recommending a visual plan.
- Read `references/style-presets.md` when choosing or changing visual style.
- Read `references/reference-image-analysis.md` when the user uploads reference images or asks to imitate a style.
- Read `references/output-format.md` before writing the final Markdown prompt file.
- Read `references/api-options.md` only when the user chooses automatic image generation. Use `scripts/check_config.py` and `scripts/generate_images.py` for the lightweight built-in automation path.

## Workflow

### 1. Collect Article Input

Use the article text, pasted draft, or local file provided by the user. If the article is missing, ask for it briefly.

If the user provides reference images before an article, analyze the image style first, then ask for the article to apply it to.

### 2. Analyze Content

Summarize:

- Article topic
- Article type: tutorial, opinion, case story, list, review, personal reflection, product/service introduction, or other
- Target reader and reader state
- Communication goal: click, understanding, trust, memory, conversion, or emotion
- Key points worth visualizing
- Recommended number of body images

Use the visual strategy rules in `references/visual-strategy.md`.

### 3. Recommend A Visual Plan

Output a concise plan before writing final prompts:

- Recommended visual direction
- Recommended style preset or custom style
- Cover image strategy
- Body image structure
- Image count
- Size plan
- Why this plan fits the article

Then ask the user to choose the next step:

```text
请选择下一步：
A. 按这套方案生成完整提示词
B. 我有参考图，先做风格分析再生成
C. 调整风格/数量/比例/是否有人物
```

Do not produce the final full prompt file until the user confirms, unless the user explicitly asks to skip confirmation.

### 4. Optional Reference Image Style Analysis

When the user uploads one or more images or chooses option B:

1. Ask whether they want `标准参考` or `高相似度参考` if unclear.
2. Analyze the images using `references/reference-image-analysis.md`.
3. Output a structured style report.
4. Explain how the style will be migrated to the current article.
5. Ask for confirmation before writing final prompts.

Use this boundary:

- Standard reference: extract style rules and adapt them naturally.
- High-similarity reference: strongly preserve color ratio, layout rhythm, whitespace, typography mood, decorative language, and image-text relationship.
- Never copy exact original copywriting, logos, watermarks, brand marks, identifiable private people, IP characters, or proprietary commercial assets.

### 5. Write Final Prompt File

After confirmation, write the final Markdown prompt content using `references/output-format.md`.

If working in a local project and a suitable folder exists, save the file. Prefer:

```text
01-内容生产/待发布/文章配图/[文章标题]_配图提示词.md
```

If that folder does not exist, save to the current working directory or ask for an output folder when necessary.

The final output must include:

- Visual strategy summary
- Unified style rules
- Cover prompt
- Body image prompts
- Manual drawing instructions
- Optional automatic drawing entry

### 6. Optional Automatic Drawing

If the user chooses automatic drawing:

1. Remind them this step is optional.
2. Ask them to choose OpenAI, Google AI Studio, or an OpenAI-compatible relay.
3. Read `references/api-options.md`.
4. Guide them to set an API key environment variable.
5. Run a dry run before real generation.

Use this built-in script path:

```text
scripts/generate_images.py
```

Default behavior:

- Parse the Markdown prompt file.
- Generate one image for each cover/body prompt section.
- Pass each prompt's target ratio to the provider by default.
- Save final PNG files plus a `manifest.json`.
- Do not require exact pixel dimensions by default. Use optional local pixel normalization only when the user explicitly asks for it.

### 7. After Output

Tell the user:

- The prompt file path, if saved
- Manual drawing option: copy prompts into Doubao, Jimeng, Banana, ChatGPT, or another image model
- Automatic drawing option: optional; use the built-in script with OpenAI, Google AI Studio, or an OpenAI-compatible relay API

Do not require automatic drawing for normal use.
