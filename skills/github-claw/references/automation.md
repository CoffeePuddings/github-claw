# Automation Reference

GitHub Actions workflow templates for the Claw agent system.

---

## Workflow 1: Copilot Issue Auto-Assignment

Automatically assigns issues with specific labels to GitHub Copilot for processing.

```yaml
# .github/workflows/copilot-autofix.yml
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
      - name: Assign to Copilot
        uses: actions/github-script@v7
        with:
          script: |
            // Add an auto-reply acknowledging receipt
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '🦞 **Claw received this issue.** I will analyze and work on it. Check back for updates.'
            });

            // Assign to copilot if available
            try {
              await github.rest.issues.addAssignees({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.issue.number,
                assignees: ['copilot[bot]']
              });
            } catch (e) {
              console.log('Could not assign copilot bot:', e.message);
            }
```

---

## Workflow 2: PR Auto-Review

Triggers Copilot review on new pull requests.

```yaml
# .github/workflows/copilot-review.yml
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

      - name: PR Info Comment
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
              body: `🦞 **Claw reviewing this PR.**\n\n**Files changed (${files.length}):**\n${fileList}\n\nI'll analyze the changes and provide feedback.`
            });
```

---

## Workflow 3: Scheduled Tasks

Cron-triggered agent tasks for maintenance and monitoring.

```yaml
# .github/workflows/copilot-scheduled.yml
name: Copilot Scheduled Tasks

on:
  schedule:
    # Run daily at 09:00 UTC
    - cron: '0 9 * * *'
  workflow_dispatch:

permissions:
  issues: write
  contents: write
  pull-requests: read

jobs:
  daily-maintenance:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Stale Issue Check
        uses: actions/github-script@v7
        with:
          script: |
            const thirtyDaysAgo = new Date();
            thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

            const { data: issues } = await github.rest.issues.listForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'open',
              since: '2020-01-01T00:00:00Z',
              per_page: 100
            });

            const staleIssues = issues.filter(issue => {
              const updated = new Date(issue.updated_at);
              return updated < thirtyDaysAgo && !issue.pull_request;
            });

            for (const issue of staleIssues) {
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                body: '🦞 This issue has been inactive for 30+ days. Is it still relevant? Adding `stale` label.'
              });

              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                labels: ['stale']
              });
            }
```

---

## Workflow 4: Jekyll / GitHub Pages Deployment

For repositories that generate a website.

```yaml
# .github/workflows/deploy-pages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Build with Jekyll
        uses: actions/jekyll-build-pages@v1
        with:
          source: ./
          destination: ./_site
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v5
```

---

## Installation Notes

- Workflows require appropriate repository permissions to be enabled
- The `copilot[bot]` assignee requires Copilot to be enabled for the repository
- Scheduled workflows only run on the default branch
- For private repos, ensure GitHub Actions minutes are available
