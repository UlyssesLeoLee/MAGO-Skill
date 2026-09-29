---
description: 调查可安全清理的 branch / worktree；默认仅预览，--apply 才执行
argument-hint: "[--apply] [--help]"
disable-model-invocation: true
---

Handle `--help` first, even if other arguments are present. Answer solely from the inline help below, then stop before any tool call, file read, skill load, or repository inspection. For an unknown option, explain the error, show this help, and stop.

## Inline help

Usage: `/GitCleanup [--apply] [--help]`

- `--apply`: Recheck each safe local candidate, then apply cleanup only where every safety condition still holds. It does not permit deleting remote branches.
- `--help`: Show this help and stop without inspecting or changing the repository.
- Default: Preview cleanup candidates only; no deletion.

Examples: `/GitCleanup`, `/GitCleanup --apply`, `/GitCleanup --help`.

For a normal invocation, run the Multi-Agent Git Orchestrator command `/GitCleanup $ARGUMENTS`.

1. Load the orchestrator skill with the Skill tool. Use whichever name the skill listing shows: `MAGO-Skill` (GitHub clone directory) or `multi-agent-git-orchestrator` (frontmatter name). If neither is listed, tell the user the skill is not installed, then continue read-only only: report observations, but do not mutate branches, worktrees, refs, or history.
2. Execute `/GitCleanup` exactly as defined in the skill's **Explicit Command Interface** and `references/commands.md`.
   Arguments (may be empty): $ARGUMENTS
3. Inspect the current repository before giving any state-dependent advice.

Safety default (applies even if the skill fails to load): preview only unless `--apply` is present. With `--apply`, delete only candidates that still meet every safety condition at apply time; never delete remote branches unless explicitly asked.
