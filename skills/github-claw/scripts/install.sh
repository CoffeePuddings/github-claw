#!/usr/bin/env bash
# github-claw installer
# Usage: bash skills/github-claw/scripts/install.sh [--preset minimal|standard|full]
#
# Bootstraps the Claw agent system in the current repository.

set -euo pipefail

PRESET="${1:-standard}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() { echo -e "${GREEN}[claw]${NC} $1"; }
warn() { echo -e "${YELLOW}[claw]${NC} $1"; }

# Parse --preset flag
if [[ "$PRESET" == "--preset" ]]; then
  PRESET="${2:-standard}"
fi

info "🦞 Installing github-claw (preset: $PRESET)"
info "Repository root: $REPO_ROOT"
echo ""

# --- Step 1: AGENTS.md ---
if [[ ! -f "$REPO_ROOT/AGENTS.md" ]]; then
  info "Creating AGENTS.md..."
  cat > "$REPO_ROOT/AGENTS.md" << 'EOF'
# AGENTS.md

## 我是谁

我是这个仓库的长期 AI 助手，代号 **Claw**。
我不只回答问题——我持续做事、积累记忆、维护角色，并让这个仓库成为可长期演化的个人 AI 空间。

- **性格**：务实、直接、善于组织、记性好
- **定位**：你的个人 AI 代理，在 GitHub Copilot 中长期驻留
- **原则**：用文件说话，不把重要信息只留在对话里

---

## 工作方式

- **仓库即工作空间**：所有重要文件、记忆、任务都保存在仓库中，通过 Git 版本化
- **文件是真实来源**：重要信息必须写入文件并提交，不依赖对话上下文
- **每次新对话先读记忆**：开始任务前先读 `MEMORY.md`，了解已有上下文和用户偏好
- **小步提交**：完成有意义的工作单元后立即提交，保持进度可见
- **临时文件不提交**：实验性或中间产物放 `/tmp/`，不进入仓库

---

## 记忆管理

| 文件 / 目录 | 用途 |
|-------------|------|
| `MEMORY.md` | **长期记忆**：用户偏好、重要决策、项目背景、已知事项 |
| `memory/log/YYYY-MM-DD.md` | **临时记录**：进行中的任务、实验笔记（可定期清理） |
| `memory/skills.md` | **技能清单**：已掌握的工具、常用命令、惯用模式 |

**操作规则：**
1. 对话中发现值得长期记住的信息 → 写入 `MEMORY.md` 对应章节
2. 多步骤任务或调研过程 → 可在 `memory/log/` 写阶段笔记
3. 每次任务结束前，检查是否有新内容需要持久化
4. `MEMORY.md` 保持简洁，定期归并或清理过时条目

---

## 收尾动作

1. **更新记忆**：将新的用户偏好、重要决策或上下文写入 `MEMORY.md`
2. **提交变更**：提交所有改动，附上简洁的提交信息
3. **清理临时文件**：确认 `/tmp/` 中的内容未被提交
4. **简要总结**：说明完成了什么、还有什么待做
EOF
else
  warn "AGENTS.md already exists, skipping."
fi

# --- Step 2: MEMORY.md ---
if [[ ! -f "$REPO_ROOT/MEMORY.md" ]]; then
  info "Creating MEMORY.md..."
  cat > "$REPO_ROOT/MEMORY.md" << EOF
# MEMORY.md — 长期记忆

> Claw 的长期记忆文件。
> **每次新对话开始前读取此文件；对话结束前将新的重要信息写入对应章节。**

---

## 用户偏好

_（待积累）_

---

## 项目背景

- **仓库**：\`$(basename "$REPO_ROOT")\`
- **定位**：AI 工作空间
- **初始化时间**：$(date +%Y-%m-%d)
- **核心文件**：\`AGENTS.md\`（规则）、\`MEMORY.md\`（本文件）

---

## 重要决策

_（待积累）_

---

## 已知事项

_（待积累）_

---

## 当前任务

_（无）_
EOF
else
  warn "MEMORY.md already exists, skipping."
fi

# --- Step 3: Memory directories ---
info "Creating memory directories..."
mkdir -p "$REPO_ROOT/memory/log"
if [[ ! -f "$REPO_ROOT/memory/skills.md" ]]; then
  cat > "$REPO_ROOT/memory/skills.md" << 'EOF'
# Skills & Tools Registry

> Agent 已掌握的工具、常用命令和惯用模式。

---

## 常用命令

_（待积累）_

## 已安装技能

- github-claw — 核心 Agent 系统

## 惯用模式

_（待积累）_
EOF
fi
touch "$REPO_ROOT/memory/log/.gitkeep"

# --- Step 4: Copilot instructions ---
info "Setting up Copilot instructions..."
mkdir -p "$REPO_ROOT/.github"

if [[ ! -f "$REPO_ROOT/.github/copilot-instructions.md" ]]; then
  cat > "$REPO_ROOT/.github/copilot-instructions.md" << 'EOF'
# Copilot Instructions

Always read `AGENTS.md` first to understand your role and working rules.
Always read `MEMORY.md` at the start of each session for long-term context.
Follow the memory management protocol defined in `AGENTS.md`.

When starting a new task:
1. Read MEMORY.md for context
2. Plan before acting
3. Make small, incremental commits
4. Update MEMORY.md before finishing
EOF
else
  warn ".github/copilot-instructions.md already exists, skipping."
fi

# --- Step 5: Workflows (standard and full presets) ---
if [[ "$PRESET" == "standard" || "$PRESET" == "full" ]]; then
  info "Installing GitHub Actions workflows..."
  mkdir -p "$REPO_ROOT/.github/workflows"

  # Issue auto-assignment workflow
  if [[ ! -f "$REPO_ROOT/.github/workflows/copilot-autofix.yml" ]]; then
    cat > "$REPO_ROOT/.github/workflows/copilot-autofix.yml" << 'EOF'
name: Copilot Auto-Assignment

on:
  issues:
    types: [opened, labeled]

permissions:
  issues: write
  contents: read

jobs:
  auto-assign:
    runs-on: ubuntu-latest
    if: contains(github.event.issue.labels.*.name, 'copilot') || contains(github.event.issue.labels.*.name, 'claw')
    steps:
      - name: Auto-reply and assign
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '🦞 **Claw received this issue.** I will analyze and work on it. Check back for updates.'
            });
EOF
  fi

  # PR review workflow
  if [[ ! -f "$REPO_ROOT/.github/workflows/copilot-review.yml" ]]; then
    cat > "$REPO_ROOT/.github/workflows/copilot-review.yml" << 'EOF'
name: Copilot PR Review

on:
  pull_request:
    types: [opened, synchronize, ready_for_review]

permissions:
  contents: read
  pull-requests: write

jobs:
  review:
    runs-on: ubuntu-latest
    if: "!github.event.pull_request.draft"
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: PR Summary Comment
        uses: actions/github-script@v7
        with:
          script: |
            const { data: files } = await github.rest.pulls.listFiles({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number
            });
            const fileList = files.map(f => `- \`${f.filename}\` (+${f.additions}/-${f.deletions})`).join('\n');
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `🦞 **Claw reviewing this PR.**\n\n**Files changed (${files.length}):**\n${fileList}`
            });
EOF
  fi
fi

# --- Step 6: Scheduled tasks (full preset only) ---
if [[ "$PRESET" == "full" ]]; then
  info "Installing scheduled task workflows..."

  if [[ ! -f "$REPO_ROOT/.github/workflows/copilot-scheduled.yml" ]]; then
    cat > "$REPO_ROOT/.github/workflows/copilot-scheduled.yml" << 'EOF'
name: Copilot Scheduled Tasks

on:
  schedule:
    - cron: '0 9 * * *'
  workflow_dispatch:

permissions:
  issues: write
  contents: read

jobs:
  stale-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check for stale issues
        uses: actions/github-script@v7
        with:
          script: |
            const thirtyDaysAgo = new Date();
            thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
            const { data: issues } = await github.rest.issues.listForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'open',
              per_page: 100
            });
            const stale = issues.filter(i => {
              return new Date(i.updated_at) < thirtyDaysAgo && !i.pull_request;
            });
            for (const issue of stale) {
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                body: '🦞 This issue has been inactive for 30+ days. Is it still relevant?'
              });
              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                labels: ['stale']
              });
            }
EOF
  fi
fi

# --- Done ---
echo ""
info "✅ github-claw installation complete!"
info ""
info "Installed components:"
info "  ✓ AGENTS.md (agent identity)"
info "  ✓ MEMORY.md (long-term memory)"
info "  ✓ memory/ (session logs & skills registry)"
info "  ✓ .github/copilot-instructions.md"
if [[ "$PRESET" == "standard" || "$PRESET" == "full" ]]; then
  info "  ✓ .github/workflows/copilot-autofix.yml"
  info "  ✓ .github/workflows/copilot-review.yml"
fi
if [[ "$PRESET" == "full" ]]; then
  info "  ✓ .github/workflows/copilot-scheduled.yml"
fi
echo ""
info "Next steps:"
info "  1. Review and customize AGENTS.md"
info "  2. Commit all changes: git add -A && git commit -m 'feat: install github-claw agent system'"
info "  3. Push to enable workflows: git push"
info "  4. Create an issue with label 'copilot' to test auto-assignment"
