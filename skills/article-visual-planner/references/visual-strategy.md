# Visual Strategy

Use this framework before designing prompts. The goal is to translate article intent into visual decisions.

## Article Type

Classify the article:

- Tutorial: emphasize steps, before/after, tools, workflow
- Opinion: emphasize contrast, tension, memorable metaphor
- Case story: emphasize scene, turning point, result
- List: emphasize grouped cards, icons, consistent rhythm
- Review: emphasize comparison, criteria, verdict
- Personal reflection: emphasize emotion, atmosphere, narrative scene
- Product/service introduction: emphasize pain point, outcome, trust, action path

## Reader State

Infer the reader's likely state:

- Anxious and stuck: lower complexity, warm professional tone
- Curious and exploring: use discovery, light contrast, concrete scenes
- Wants shortcuts: make steps visible and expectations clear
- Rationally evaluating: use structured diagrams, comparison, evidence cues
- Already experienced: use sharper concepts, models, and workflow maps

## Visual Goal

Choose the primary job of images:

- Cover image: increase opening desire and make the article promise visible
- Body image: reduce understanding cost, organize memory, support trust
- Summary image: make the core framework shareable or save-worthy
- Conversion image: clarify service/product path without sounding like an ad

## Planning Rules

- Recommend 2-5正文配图 for normal long-form articles.
- Use fewer images for opinion or story articles; use more for tutorial and framework articles.
- Keep one style system across all images.
- Separate cover and正文配图 roles: the cover attracts; article illustrations explain.
- Avoid overusing cold futuristic tech style for beginner-facing AI content unless the article tone is advanced.
- Prefer visual metaphors that make the user's current difficulty and desired result concrete.

## Decision Output

Before final prompts, output:

```text
文章判断：
目标读者：
读者状态：
视觉目标：
推荐风格：
图片结构：
比例建议：
推荐理由：
```
