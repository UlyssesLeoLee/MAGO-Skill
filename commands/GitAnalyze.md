---
description: 深入分析指定分支或 worktree，评估 merge / rebase / cherry-pick / delete 是否安全
argument-hint: "<branch|worktree> [--remote] [--help]"
---

Run the Multi-Agent Git Orchestrator command `/GitAnalyze $ARGUMENTS`.

If `--help` is present, print the usage, argument descriptions, and examples from section **2. GitAnalyze** in `references/commands.md`, then stop without loading the orchestrator skill or inspecting the repository. If the target is missing, ask for it and show the usage. If an unknown option is supplied, explain the error and show the help.

1. Load the orchestrator skill with the Skill tool. Use whichever name the skill listing shows: `MAGO-Skill` (GitHub clone directory) or `multi-agent-git-orchestrator` (frontmatter name). If neither is listed, tell the user the skill is not installed, then continue read-only only: report observations, but do not mutate branches, worktrees, refs, or history.
2. Execute `/GitAnalyze` exactly as defined in the skill's **Explicit Command Interface** and `references/commands.md`.
   Arguments (may be empty): $ARGUMENTS
3. Inspect the current repository before giving any state-dependent advice.

Safety default (applies even if the skill fails to load): read-only. `--remote` only permits refreshing remote-tracking refs; never mutate branches, worktrees, or history. If no target is given, ask for one.
