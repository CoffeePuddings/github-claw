# MEMORY.md — 长期记忆

> Claw 的长期记忆文件。  
> **每次新对话开始前读取此文件；对话结束前将新的重要信息写入对应章节。**

---

## 用户偏好

_（待积累）_

---

## 项目背景

- **仓库**：`CoffeePuddings/github-claw`
- **定位**：个人 AI 工作空间，基于 GitHub Copilot 网页版长期使用
- **初始化时间**：2026-06-02
- **核心文件**：`AGENTS.md`（规则）、`MEMORY.md`（本文件，长期记忆）

---

## 重要决策

- **2026-06-04**：创建每日 AI 热点日报工作流（`.github/workflows/daily-ai-digest.yml`）
  - 触发时间：北京时间每天 13:00（UTC 05:00），支持手动触发
  - 数据来源：HackerNews Algolia API（AI 相关热帖）+ GitHub Trending（AI 相关仓库）
  - 输出方式：自动在仓库创建带 `ai-digest` 标签的 GitHub Issue

---

## 已知事项

- `ai-digest` label 需要在仓库中手动创建（或首次运行后报错时创建），否则 Issue 会创建成功但无 label
