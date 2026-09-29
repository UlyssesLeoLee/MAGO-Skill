---
name: git-recommend
description: "给出 Git 建议；/git-recommend [goal] [--remote] [--help]."
license: MIT
metadata:
  short-description: "Git 建议；$git-recommend [goal] [--remote] [--help]."
---

# GitRecommend

Use this skill when the user explicitly invokes `/git-recommend` in Hermes or `$git-recommend` in Codex. Treat any text following the selected skill name as the command arguments.

## Usage

- Hermes: `/git-recommend [goal] [--remote] [--help]`
- Codex: `$git-recommend [goal] [--remote] [--help]`
- `[goal]`: Optional natural-language question or desired outcome; omit it for general next-step recommendations.
- `--remote`: Refresh remote-tracking refs before recommending; it does not change branches, worktrees, or commit history.
- `--help`: Show this inline usage and argument description, then stop without inspecting the repository.
- Default: Advisory recommendations using a fresh local reconnaissance snapshot; no remote refresh.

Examples: `/git-recommend`, `$git-recommend 哪些分支应该先合并 --remote`, `$git-recommend --help`.

If `--help` is present, even with other arguments, answer from the inline Usage section above and stop before any tool call, file read, or repository inspection. Treat `--remote` as an option only when it is a standalone argument; for an unknown option, explain the error, show this help, and stop. Read the linked files below only for a normal invocation.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitRecommend.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **3. GitRecommend** and `../../references/reconnaissance.md` — command contract and repository inspection steps.

Execute the canonical `/GitRecommend` command with the supplied arguments. Inspect the current repository first, and run or reuse a fresh reconnaissance snapshot before recommending. Recommendations are advisory and must not mutate repository topology.
