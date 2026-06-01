# Output Format

The final prompt file must be Markdown and parseable by humans. Keep the structure stable.

## File Template

```markdown
# [文章标题] 配图提示词方案

**文章类型：[类型] | 共[X]张 | 封面图比例：2.35:1 | 正文图比例：[比例]**

---

## 视觉策划说明

文章判断：
[一句话]

目标读者：
[一句话]

读者状态：
[一句话]

视觉目标：
[一句话]

统一风格：
[风格名称 + 核心特征]

---

## 全局风格规范

- 画面气质：
- 配色：
- 字体：
- 图示：
- 留白：
- 禁止：

---

## 封面图 - [主题名称]

[完整提示词]

---

## 正文配图1 - [主题名称]

[完整提示词]

---

## 正文配图2 - [主题名称]

[完整提示词]

---

## 使用方式

手动绘图：
复制每张图的提示词，到豆包、即梦、Banana、ChatGPT 等工具中生成。

自动绘图：
这是可选步骤。如需自动绘图，请继续选择 API Key 方式：OpenAI、Google AI Studio 或中转站。
```

## Prompt Requirements For Each Image

Each image prompt must include:

1. Opening line: `【重要说明】请独立生成1张[风格定性]图片`
2. Canvas ratio
3. Visual role: cover, explanation, comparison, summary, scene, workflow, etc.
4. Color rules with exact hex values
5. Typography rules
6. Page structure from top to bottom or foreground to background
7. Text to display, locked with backticks
8. Illustration/icon/photo guidance bound to the text block it supports
9. Negative constraints

## Text Locking Rule

All visible text that should appear in the image must be wrapped in backticks.

Good:

```text
主标题使用 `普通人做AI账号，先别急着学工具`
```

Bad:

```text
主标题写普通人做AI账号，先别急着学工具
```

## Ratio Rules

- Cover image: always use `2.35:1`
- Body images default: use `16:9`
- Use `4:3` when a正文配图 needs more vertical space for frameworks, checklists, or process diagrams
- Keep all正文配图 images the same ratio unless the user asks otherwise
- Avoid writing fixed pixel dimensions in prompts unless the user explicitly asks for a specific platform export size

## Structure Rules

- Do not say only "put it on the left"; specify container, area, proportion, and relationship.
- Bind illustration and text: "[text] with a small illustration of [specific visual] beside/above/inside the same card."
- Use clear sectioning for information-heavy images.
- Keep正文配图 text concise; each block should normally be under 20 Chinese characters.
