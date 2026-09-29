---
description: 基于当前仓库真实状态给出下一步 Git / 多 Agent 编排建议
argument-hint: "[<goal>] [--remote] [--help]"
---

Run the Multi-Agent Git Orchestrator command `/GitRecommend $ARGUMENTS`.

If `--help` is present, print the usage, argument descriptions, and examples from section **3. GitRecommend** in `references/commands.md`, then stop without loading the orchestrator skill or inspecting the repository. Treat a standalone `--remote` token as an option and preserve other trailing text as the optional goal. If an unknown option is supplied, explain the error and show the help.

1. Load the orchestrator skill with the Skill tool. Use whichever name the skill listing shows: `MAGO-Skill` (GitHub clone directory) or `multi-agent-git-orchestrator` (frontmatter name). If neither is listed, tell the user the skill is not installed, then continue read-only only: report observations, but do not mutate branches, worktrees, refs, or history.
2. Execute `/GitRecommend` exactly as defined in the skill's **Explicit Command Interface** and `references/commands.md`.
   Arguments (may be empty): $ARGUMENTS
3. Inspect the current repository before giving any state-dependent advice.

Safety default (applies even if the skill fails to load): advisory only. Run or reuse a fresh reconnaissance snapshot first; never mutate branches, worktrees, or history.
