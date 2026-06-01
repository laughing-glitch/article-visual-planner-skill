# Reference Image Style Analysis

Use when the user uploads one or more reference images.

## Similarity Modes

If the user does not specify, ask:

```text
你希望参考图做到哪种程度？
1. 标准参考：提取风格规律，适配到文章内容
2. 高相似度参考：尽量贴近配色、版式节奏、留白、字体气质和图文关系，但替换原图具体文字、Logo、水印和专有元素
```

## Analysis Report Format

### 1. 整体风格定性

- 风格名称
- 1-2 sentence core description

### 2. 配色体系

- 背景色：色值
- 主色调：用途 + 色值
- 辅助色：用途 + 色值
- 文字色：用途 + 色值
- 整体色调感受
- 禁用色：what colors would break this style

### 3. 排版结构

- 画幅比例
- 固定框架元素: sequence label position, title area proportion, signature area, etc.
- 分区方式
- 留白习惯

### 4. 字体风格

- 标题字体特征
- 正文字体特征
- 是否有中英双标注
- 字号层级关系

### 5. 图示与插画风格

- 插图类型: hand-drawn, vector, photo, icon, 3D, collage, etc.
- 线条特征
- 图示与文字的关系

### 6. 特殊设计元素

- Borders, dividers, decorations
- Emphasis boxes, labels, badges
- Signature visual symbols

### 7. 迁移到本文的建议

- Elements to preserve
- Elements to avoid or replace
- Cover image migration method
- Body image migration method
- Unified style rules for all generated prompts

## Boundary

Aim for high practical similarity when the user asks to imitate a reference image. Preserve style, layout rhythm, hierarchy, and design language. Replace protected or identifying details:

- Exact original text
- Logos, watermarks, trademarks
- Identifiable private persons
- IP characters
- Proprietary commercial assets

Do not make the output timid. If the user asks for high similarity, explicitly write prompts that say: "migrate the reference image's visual style, color ratio, spacing rhythm, typography mood, and image-text structure."
