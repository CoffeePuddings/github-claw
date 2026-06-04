#!/usr/bin/env bash
# hello-world skill — 验证技能机制是否正常工作
set -euo pipefail

echo "✅ hello-world skill 运行正常"
echo "技能目录: $(dirname "$0")"
echo "所有已注册技能:"
ls "$(dirname "$0")/.." | grep -v README.md
