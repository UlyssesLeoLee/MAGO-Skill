---
description: 调查当前 Git 仓库整体状态（branch / worktree / HEAD / ahead-behind / dirty / 风险）
argument-hint: "[--remote] [--help]"
---

Handle `--help` first, even if other arguments are present. Answer solely from the inline help below, then stop before any tool call, file read, skill load, or repository inspection. For an unknown option, explain the error, show this help, and stop.

## Inline help

Usage: `/GitRecon [--remote] [--help]`

- `--remote`: Refresh remote-tracking refs before classifying the repository. It does not change branches, worktrees, or commit history.
- `--help`: Show this help and stop without inspecting the repository.
- Default: Read-only snapshot using existing local refs; no remote refresh.

Examples: `/GitRecon`, `/GitRecon --remote`, `/GitRecon --help`.

For a normal invocation, run the Multi-Agent Git Orchestrator command `/GitRecon $ARGUMENTS`.

1. Load the orchestrator skill with the Skill tool. It may be listed as `MAGOS` (install directory), `multi-agent-git-orchestrator` (frontmatter name), or `MAGO-Skill` (older clone directory); any listed skill described as the Multi-Agent Git Orchestrator is the same skill. If none is listed but `~/.claude/skills/MAGOS/SKILL.md` exists, read that file instead. Only if the skill cannot be loaded at all, tell the user, then continue read-only only: report observations, but do not mutate branches, worktrees, refs, or history.
2. Execute `/GitRecon` exactly as defined in the skill's **Explicit Command Interface** and `references/commands.md`.
   Arguments (may be empty): $ARGUMENTS
3. Inspect the current repository before giving any state-dependent advice.

Safety default (applies even if the skill fails to load): read-only. `--remote` only permits refreshing remote-tracking refs (e.g. `git fetch --prune`); never mutate branches, worktrees, or history.
