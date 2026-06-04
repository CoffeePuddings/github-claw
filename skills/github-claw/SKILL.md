---
name: github-claw
description: Transform any GitHub repository into an OpenClaw-style AI agent workspace powered by GitHub Copilot. Use this skill whenever a user wants to set up an autonomous AI agent in their repo, create an AI-powered crayfish/claw system, configure Copilot as a persistent agent with memory and personality, automate issues/PRs/workflows with Copilot, or mentions "小龙虾", "OpenClaw", "github-claw", or "AI workspace". Also trigger when the user wants to add agent identity, file-based memory, skill management, scheduled automation, issue auto-reply, PR review automation, or coding/deployment pipelines to their GitHub Copilot setup.
---

# GitHub Claw 🦞

Transform GitHub Copilot into an autonomous, persistent AI agent (codenamed "Claw") that lives in your repository — with its own identity, memory, skills, and automation capabilities.

## What This Skill Does

This skill bootstraps a complete "AI workspace" in any GitHub repository, turning GitHub Copilot from a passive assistant into an active, long-running agent with:

1. **Persona & Identity** — A defined character, working principles, and behavioral rules
2. **File-based Memory** — Persistent long-term context that survives across sessions
3. **Skill Discovery & Management** — Install, organize, and invoke reusable skill modules
4. **Scheduled Automation** — GitHub Actions workflows for cron-triggered agent tasks
5. **Issue Auto-reply & Assignment** — Automatically respond to and assign issues to Copilot
6. **PR Review & Workflow Automation** — Automated code review and merge pipelines
7. **Coding, Deployment & Project Management** — End-to-end development workflow support

## Quick Start

When a user asks to set up github-claw, run the install script:

```bash
bash skills/github-claw/scripts/install.sh
```

Or, for a step-by-step guided setup, follow the sections below.

---

## Installation Flow

### Step 1: Initialize Agent Identity

Create `AGENTS.md` at the repository root. This defines who the agent is and how it behaves.

Read `references/persona.md` for the full persona template and customization options.

Key elements:
- Agent codename and personality traits
- Working principles (file-first, small commits, memory management)
- Interaction style and language preferences

### Step 2: Set Up Memory System

Create the memory infrastructure for cross-session persistence.

Read `references/memory-system.md` for the complete memory architecture.

Files to create:
- `MEMORY.md` — Long-term memory (preferences, decisions, project context)
- `memory/log/` — Session logs and work-in-progress notes
- `memory/skills.md` — Discovered tools and patterns

### Step 3: Configure Skill Management

Set up the skill loading and discovery system so the agent can use modular capabilities.

Key directories:
- `.github/prompts/` — Copilot custom prompt files
- `skills/` — Reusable skill modules (like this one)

The agent should scan for available skills at session start and load them as needed.

### Step 4: Set Up GitHub Actions Automation

Read `references/automation.md` for workflow templates.

Install automated workflows for:
- **Scheduled tasks** — Cron-triggered agent actions (daily summaries, stale issue cleanup)
- **Issue auto-assignment** — Route new issues to Copilot for triage
- **PR automation** — Auto-review, label, and manage pull requests
- **Deployment** — GitHub Pages or other deployment pipelines

### Step 5: Configure Issue & PR Workflows

Read `references/issue-pr-workflows.md` for detailed configuration.

Set up:
- Issue auto-reply with context-aware responses
- Automatic Copilot assignment for labeled issues
- PR review triggers and automated feedback
- Branch protection and merge policies

### Step 6: Verify & Activate

After installation:
1. Commit all generated files
2. Verify GitHub Actions workflows are enabled
3. Test by creating a sample issue
4. Confirm the agent reads MEMORY.md in new sessions

---

## Customization

### Persona Variants

The default persona is "Claw" (务实、直接、善于组织), but users can customize:
- Name, personality traits, and communication style
- Language (Chinese, English, or bilingual)
- Formality level and emoji usage

### Automation Intensity

Three presets:
- **Minimal** — Memory + persona only, no automation
- **Standard** — Memory + persona + issue/PR workflows
- **Full** — Everything including scheduled tasks and deployment

### Repository Type Adaptations

The skill adapts to:
- **Personal projects** — Lighter automation, focus on memory and coding
- **Team repos** — Heavier PR review, issue triage, documentation
- **Open source** — Community-facing auto-reply, contributor guidance

---

## File Map

After full installation, the repository will contain:

```
repo-root/
├── AGENTS.md                          # Agent identity & rules
├── MEMORY.md                          # Long-term memory
├── memory/
│   ├── log/                           # Session logs
│   └── skills.md                      # Known tools & patterns
├── .github/
│   ├── workflows/
│   │   ├── copilot-autofix.yml        # Issue auto-assignment
│   │   ├── copilot-review.yml         # PR auto-review
│   │   └── copilot-scheduled.yml      # Cron tasks
│   ├── copilot-instructions.md        # Global Copilot instructions
│   └── prompts/                       # Custom prompt modules
└── skills/                            # Skill modules
    └── github-claw/                   # This skill
```

---

## Operating Principles

These principles are embedded into the agent's behavior:

1. **File is truth** — Important information lives in committed files, never only in chat
2. **Small commits** — Commit after each meaningful unit of work
3. **Memory-first** — Read MEMORY.md at session start, update before session end
4. **Graceful degradation** — If automation fails, fall back to manual steps
5. **No secrets in code** — Use GitHub Secrets for sensitive values
6. **Incremental enhancement** — Start minimal, add capabilities over time

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Workflows not triggering | Check Actions permissions in repo Settings |
| Copilot not assigned to issues | Verify `copilot` is added as collaborator |
| Memory not persisting | Ensure MEMORY.md is committed, not in .gitignore |
| Skills not loading | Check `.github/prompts/` structure |

---

## References

- `references/persona.md` — Full persona template and customization guide
- `references/memory-system.md` — Memory architecture and management rules
- `references/automation.md` — GitHub Actions workflow templates
- `references/issue-pr-workflows.md` — Issue/PR automation configuration
