# Memory System Reference

This document describes the file-based memory architecture that gives the agent persistent context across sessions.

---

## Architecture Overview

```
repo-root/
├── MEMORY.md              # Primary long-term memory
├── memory/
│   ├── log/               # Date-stamped session logs
│   │   ├── 2026-06-01.md
│   │   └── 2026-06-02.md
│   └── skills.md          # Discovered tools & patterns
```

---

## MEMORY.md Template

```markdown
# MEMORY.md — 长期记忆

> [AGENT_NAME] 的长期记忆文件。
> **每次新对话开始前读取此文件；对话结束前将新的重要信息写入对应章节。**

---

## 用户偏好

- 语言偏好：[中文 / English / 双语]
- 代码风格：[preferences]
- 提交信息格式：[conventional commits / 自由格式]

---

## 项目背景

- **仓库**：`[owner/repo]`
- **定位**：[project description]
- **初始化时间**：[date]
- **核心文件**：`AGENTS.md`（规则）、`MEMORY.md`（本文件）

---

## 重要决策

- [date]: [decision description]

---

## 已知事项

- [important context that persists across sessions]

---

## 当前任务

- [ ] [active task 1]
- [ ] [active task 2]
```

---

## Memory Operations Protocol

### Session Start

```
1. Read MEMORY.md
2. Read memory/log/ for recent entries (last 3 days)
3. Load relevant context into working memory
4. Acknowledge current tasks and user preferences
```

### During Session

```
1. When user states a preference → note for MEMORY.md update
2. When a decision is made → note for MEMORY.md update
3. For multi-step work → write to memory/log/YYYY-MM-DD.md
4. When discovering tools/patterns → note for memory/skills.md
```

### Session End

```
1. Update MEMORY.md with new preferences, decisions, context
2. Update memory/log/ if there's work in progress
3. Update memory/skills.md if new tools were discovered
4. Commit all memory updates
```

---

## Memory Hygiene Rules

1. **MEMORY.md stays concise** — Target under 100 lines. Archive old entries.
2. **Logs are ephemeral** — Delete logs older than 30 days unless referenced.
3. **No secrets in memory** — Never write tokens, passwords, or keys.
4. **Deduplication** — Before adding, check if the info already exists.
5. **Structured entries** — Use consistent date formats and categorization.

---

## Memory Categories

| Category | What Goes Here | Example |
|----------|---------------|---------|
| 用户偏好 | Communication and code style preferences | "Prefers conventional commits" |
| 项目背景 | Repo purpose, tech stack, deployment info | "Next.js app deployed on Vercel" |
| 重要决策 | Architecture choices, tool selections | "Chose PostgreSQL over MongoDB" |
| 已知事项 | Recurring issues, environment quirks | "CI fails on Node 18, use 20" |
| 当前任务 | Active work items and their status | "Refactoring auth module - 60% done" |

---

## Integration with GitHub Copilot Memory

This file-based system complements (not replaces) GitHub Copilot's built-in memory system:

- **Copilot Memory** → Short facts, preferences (auto-managed by platform)
- **MEMORY.md** → Rich context, task state, decision history (user-controlled)
- **memory/log/** → Detailed session traces for complex multi-day work

Use both systems together for maximum context retention.
