---
description: 基于当前仓库真实状态给出下一步 Git / 多 Agent 编排建议
argument-hint: "[<goal>] [--remote] [--help]"
---

Handle `--help` first, even if other arguments are present. Answer solely from the inline help below, then stop before any tool call, file read, skill load, or repository inspection. Treat a standalone `--remote` token as an option and preserve other trailing text as the optional goal. For an unknown option, explain the error, show this help, and stop.

## Inline help

Usage: `/GitRecommend [goal] [--remote] [--help]`

- `[goal]`: Optional natural-language question or desired outcome; omit it for general next-step recommendations.
- `--remote`: Refresh remote-tracking refs before recommending. It does not change branches, worktrees, or commit history.
- `--help`: Show this help and stop without inspecting the repository.
- Default: Advisory recommendations using a fresh local reconnaissance snapshot; no remote refresh.

Examples: `/GitRecommend`, `/GitRecommend 哪些分支应该先合并 --remote`, `/GitRecommend --help`.

For a normal invocation, run the Multi-Agent Git Orchestrator command `/GitRecommend $ARGUMENTS`.

1. Load the orchestrator skill with the Skill tool. It may be listed as `MAGOS` (install directory), `multi-agent-git-orchestrator` (frontmatter name), or `MAGO-Skill` (older clone directory); any listed skill described as the Multi-Agent Git Orchestrator is the same skill. If none is listed but `~/.claude/skills/MAGOS/SKILL.md` exists, read that file instead. Only if the skill cannot be loaded at all, tell the user, then continue read-only only: report observations, but do not mutate branches, worktrees, refs, or history.
2. Execute `/GitRecommend` exactly as defined in the skill's **Explicit Command Interface** and `references/commands.md`.
   Arguments (may be empty): $ARGUMENTS
3. Inspect the current repository before giving any state-dependent advice.

Safety default (applies even if the skill fails to load): advisory only. Run or reuse a fresh reconnaissance snapshot first; never mutate branches, worktrees, or history.
