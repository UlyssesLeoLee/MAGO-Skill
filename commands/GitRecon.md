---
description: 调查当前 Git 仓库整体状态（branch / worktree / HEAD / ahead-behind / dirty / 风险）
argument-hint: "[--remote]"
---

Run the Multi-Agent Git Orchestrator command `/GitRecon $ARGUMENTS`.

1. Load the orchestrator skill with the Skill tool. Use whichever name the skill listing shows: `MAGO-Skill` (GitHub clone directory) or `multi-agent-git-orchestrator` (frontmatter name). If neither is listed, tell the user the skill is not installed, then continue read-only only: report observations, but do not mutate branches, worktrees, refs, or history.
2. Execute `/GitRecon` exactly as defined in the skill's **Explicit Command Interface** and `references/commands.md`.
   Arguments (may be empty): $ARGUMENTS
3. Inspect the current repository before giving any state-dependent advice.

Safety default (applies even if the skill fails to load): read-only. `--remote` only permits refreshing remote-tracking refs (e.g. `git fetch --prune`); never mutate branches, worktrees, or history.
