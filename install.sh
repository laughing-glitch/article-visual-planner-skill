#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="article-visual-planner"
INSTALL_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
if [ -n "${BASH_SOURCE:-}" ]; then
  SCRIPT_PATH="$BASH_SOURCE"
else
  SCRIPT_PATH="$0"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" 2>/dev/null && pwd || pwd)"
SOURCE_DIR="$SCRIPT_DIR/skills/$SKILL_NAME"
TARGET_DIR="$INSTALL_DIR/$SKILL_NAME"
REPO_TARBALL_URL="${REPO_TARBALL_URL:-https://github.com/laughing-glitch/article-visual-planner-skill/archive/refs/heads/main.tar.gz}"

TMP_DIR=""

cleanup() {
  if [ -n "$TMP_DIR" ] && [ -d "$TMP_DIR" ]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT

if [ ! -d "$SOURCE_DIR" ]; then
  TMP_DIR="$(mktemp -d)"
  echo "正在下载 Skill..."
  curl -fsSL "$REPO_TARBALL_URL" | tar -xz -C "$TMP_DIR"
  SOURCE_DIR="$(find "$TMP_DIR" -type d -path "*/skills/$SKILL_NAME" | head -n 1)"
  if [ -z "$SOURCE_DIR" ] || [ ! -d "$SOURCE_DIR" ]; then
    echo "未找到 Skill 目录。请检查下载地址：$REPO_TARBALL_URL"
    exit 1
  fi
fi

mkdir -p "$INSTALL_DIR"
rm -rf "$TARGET_DIR"
cp -R "$SOURCE_DIR" "$TARGET_DIR"

echo "安装完成：$TARGET_DIR"
echo
echo "新建对话后可以这样调用："
echo "使用 article-visual-planner，帮我根据这篇公众号文章生成封面和正文配图提示词。"
