# Issue & PR Workflow Reference

Detailed configuration for automated issue and pull request management.

---

## Issue Automation

### Auto-Reply Strategy

When a new issue is created, the agent can respond based on issue content:

| Issue Type | Auto-Reply Strategy |
|-----------|-------------------|
| Bug report | Acknowledge, ask for reproduction steps if missing |
| Feature request | Acknowledge, suggest labeling priorities |
| Question | Attempt to answer from memory/docs, or ask for clarification |
| Copilot-labeled | Full assignment and work initiation |

### Label-Based Routing

Configure labels to control automation behavior:

```yaml
# Label definitions for issue routing
labels:
  copilot:
    description: "Assign to Copilot for automated handling"
    color: "7057ff"
  claw:
    description: "Claw agent task"
    color: "e4553d"
  auto-reply:
    description: "Enable auto-reply on this issue"
    color: "0e8a16"
  stale:
    description: "Inactive for 30+ days"
    color: "cccccc"
```

### Issue Response Templates

**Bug Report Response:**
```markdown
🦞 Thanks for reporting this issue!

I'll take a look. To help me investigate faster:
- [ ] Steps to reproduce
- [ ] Expected vs actual behavior
- [ ] Environment details (OS, browser, version)

I'll update this issue once I have findings.
```

**Feature Request Response:**
```markdown
🦞 Interesting idea! I've noted this feature request.

Let me check if this aligns with current project direction and see what implementation would look like.
I'll add my analysis as a follow-up comment.
```

**Copilot Assignment Response:**
```markdown
🦞 **Claw received this task.**

I'm analyzing the requirements now. Here's my plan:
1. Read relevant code and context
2. Propose a solution approach
3. Implement and submit a PR

ETA: I'll update within this session.
```

---

## PR Automation

### Review Checklist

When reviewing a PR, the agent checks:

1. **Code quality** — Clean, readable, follows project conventions
2. **Tests** — New code has appropriate test coverage
3. **Documentation** — Changes are documented where needed
4. **Security** — No secrets, no obvious vulnerabilities
5. **Breaking changes** — Backward compatibility maintained
6. **Commit messages** — Clear, descriptive, follow conventions

### Auto-Label Rules

```yaml
# PR auto-labeling based on file paths
rules:
  - pattern: "docs/**"
    label: "documentation"
  - pattern: "*.test.*"
    label: "tests"
  - pattern: ".github/workflows/**"
    label: "ci/cd"
  - pattern: "src/**"
    label: "code"
  - pattern: "*.md"
    label: "documentation"
```

### PR Review Comment Template

```markdown
🦞 **Claw Code Review**

## Summary
[Brief description of what the PR does]

## Assessment
- **Quality**: [Good/Needs Work]
- **Tests**: [Covered/Missing]
- **Docs**: [Updated/Needed]

## Suggestions
[Specific, actionable feedback]

## Verdict
[Approve / Request Changes / Comment]
```

---

## Copilot Integration Setup

### Enabling Copilot for Issues

1. Go to repository Settings → General → Features
2. Enable "Issues"
3. Go to Settings → Copilot → Policies
4. Enable Copilot for the repository

### Copilot Agent Assignment

For Copilot to be assignable to issues:

1. Navigate to the issue
2. Use `@github-copilot` mention or assign via label-triggered workflow
3. Copilot will process the issue based on AGENTS.md instructions

### Workflow Permissions

Ensure the following permissions in repository Settings → Actions → General:

- **Workflow permissions**: Read and write permissions
- **Allow GitHub Actions to create and approve pull requests**: Enabled

---

## Advanced Patterns

### Chain: Issue → Branch → PR → Review → Merge

```
1. Issue created with `copilot` label
2. Workflow assigns to Copilot
3. Copilot creates feature branch
4. Copilot implements changes
5. Copilot opens PR referencing the issue
6. PR review workflow runs
7. If approved, auto-merge enabled
```

### Escalation Rules

Not everything should be auto-handled. Escalate to human when:

- Issue is labeled `security` or `critical`
- PR touches more than 20 files
- CI fails after 2 retry attempts
- Merge conflicts cannot be auto-resolved
- User explicitly requests human review

### Rate Limiting

To prevent runaway automation:

- Max 10 auto-replies per hour
- Max 5 PR reviews per hour
- Max 3 branch creations per day via automation
- Cool-down period after errors: 30 minutes
