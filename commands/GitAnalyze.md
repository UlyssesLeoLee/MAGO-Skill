---
description: 深入分析指定分支或 worktree，评估 merge / rebase / cherry-pick / delete 是否安全
argument-hint: "<branch|worktree> [--remote] [--help]"
---

Handle `--help` first, even if other arguments are present. Answer solely from the inline help below, then stop before any tool call, file read, skill load, or repository inspection. If the target is missing, ask for it and show this help. For an unknown option, explain the error, show this help, and stop.

## Inline help

Usage: `/GitAnalyze <branch|worktree-path> [--remote] [--help]`

- `<branch|worktree-path>`: Required branch name or worktree path to analyze.
- `--remote`: Refresh remote-tracking refs before analysis. It does not change branches, worktrees, or commit history.
- `--help`: Show this help and stop without inspecting the repository.
- Default: Read-only analysis using existing local refs; no remote refresh.

Examples: `/GitAnalyze feature/auth`, `/GitAnalyze feature/auth --remote`, `/GitAnalyze --help`.

For a normal invocation, run the Multi-Agent Git Orchestrator command `/GitAnalyze $ARGUMENTS`.

1. Load the orchestrator skill with the Skill tool. Use whichever name the skill listing shows: `MAGO-Skill` (GitHub clone directory) or `multi-agent-git-orchestrator` (frontmatter name). If neither is listed, tell the user the skill is not installed, then continue read-only only: report observations, but do not mutate branches, worktrees, refs, or history.
2. Execute `/GitAnalyze` exactly as defined in the skill's **Explicit Command Interface** and `references/commands.md`.
   Arguments (may be empty): $ARGUMENTS
3. Inspect the current repository before giving any state-dependent advice.

Safety default (applies even if the skill fails to load): read-only. `--remote` only permits refreshing remote-tracking refs; never mutate branches, worktrees, or history. If no target is given, ask for one.
