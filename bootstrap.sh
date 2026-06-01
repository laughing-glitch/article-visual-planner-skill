#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="article-visual-planner"
INSTALL_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
TARGET_DIR="$INSTALL_DIR/$SKILL_NAME"
REPO_TARBALL_URL="${REPO_TARBALL_URL:-https://github.com/laughing-glitch/article-visual-planner-skill/archive/refs/heads/main.tar.gz}"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

echo "正在下载 Skill..."
curl -fsSL "$REPO_TARBALL_URL" | tar -xz -C "$TMP_DIR"
SOURCE_DIR="$(find "$TMP_DIR" -type d -path "*/skills/$SKILL_NAME" | head -n 1)"

if [ -z "$SOURCE_DIR" ] || [ ! -d "$SOURCE_DIR" ]; then
  echo "未找到 Skill 目录。请检查下载地址：$REPO_TARBALL_URL"
  exit 1
fi

mkdir -p "$INSTALL_DIR"
rm -rf "$TARGET_DIR"
cp -R "$SOURCE_DIR" "$TARGET_DIR"

echo "安装完成：$TARGET_DIR"
echo
echo "新建对话后可以这样调用："
echo "使用 article-visual-planner，帮我根据这篇公众号文章生成封面和正文配图提示词。"
