---
description: 调查可安全清理的 branch / worktree；默认仅预览，--apply 才执行
argument-hint: "[--apply] [--help]"
disable-model-invocation: true
---

Run the Multi-Agent Git Orchestrator command `/GitCleanup $ARGUMENTS`.

If `--help` is present, print the usage, argument descriptions, and examples from section **5. GitCleanup** in `references/commands.md`, then stop without loading the orchestrator skill or inspecting the repository. If an unknown option is supplied, explain the error and show the same help.

1. Load the orchestrator skill with the Skill tool. Use whichever name the skill listing shows: `MAGO-Skill` (GitHub clone directory) or `multi-agent-git-orchestrator` (frontmatter name). If neither is listed, tell the user the skill is not installed, then continue read-only only: report observations, but do not mutate branches, worktrees, refs, or history.
2. Execute `/GitCleanup` exactly as defined in the skill's **Explicit Command Interface** and `references/commands.md`.
   Arguments (may be empty): $ARGUMENTS
3. Inspect the current repository before giving any state-dependent advice.

Safety default (applies even if the skill fails to load): preview only unless `--apply` is present. With `--apply`, delete only candidates that still meet every safety condition at apply time; never delete remote branches unless explicitly asked.
