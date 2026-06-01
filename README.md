# Article Visual Planner Skill

一个面向公众号文章的视觉策划 Skill。

它可以根据文章内容，先给出视觉方案，再生成：

- 公众号封面图提示词，默认比例 `2.35:1`
- 多张正文配图提示词，默认比例 `16:9`
- 可选参考图风格分析
- 可选 API 自动画图

核心不是随便生成几张图，而是先判断文章应该如何被点击、理解、信任和记住。

## 一键安装

打开终端，运行：

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/article-visual-planner-skill/main/install.sh | bash
```

安装完成后，新建对话，直接说：

```text
使用 article-visual-planner，帮我根据这篇公众号文章生成封面和正文配图提示词。
```

然后粘贴文章内容即可。

## 手动安装

如果你是下载 ZIP 包：

```bash
bash install.sh
```

它会把 Skill 安装到：

```text
~/.codex/skills/article-visual-planner
```

## 参考图模式

如果你有想模仿的图片，可以这样说：

```text
使用 article-visual-planner，我会上传一张参考图。请先做风格分析，再按这个风格给文章生成配图提示词。
```

Skill 会引导你选择：

- 标准参考：提取风格规律，适配到文章内容
- 高相似度参考：尽量贴近配色、版式节奏、留白、字体气质和图文关系

## 自动画图

自动画图是可选步骤。没有 API Key 也可以正常使用提示词生成功能。

如果你要自动画图，Skill 会引导你选择：

- OpenAI API Key
- Google AI Studio API Key
- 中转站 API Key

第一次建议先让 AI 引导你测试，不需要自己记命令：

```text
使用 article-visual-planner，我想测试自动画图。请你一步步引导我，不要一次性给我太多命令。
```

## 更新

重新运行安装命令即可覆盖旧版本。
