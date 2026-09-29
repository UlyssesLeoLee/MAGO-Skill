---
name: git-cleanup
description: "预览清理；/git-cleanup [--apply] [--help]."
license: MIT
metadata:
  short-description: "预览清理；$git-cleanup [--apply] [--help]."
---

# GitCleanup

Use this skill when the user explicitly invokes `/git-cleanup` in Hermes or `$git-cleanup` in Codex. Treat any text following the selected skill name as the command arguments.

## Usage

- Hermes: `/git-cleanup [--apply] [--help]`
- Codex: `$git-cleanup [--apply] [--help]`
- `--apply`: Recheck each safe local candidate, then apply cleanup only where every safety condition still holds. It does not permit deleting remote branches.
- `--help`: Show this inline usage and argument description, then stop without inspecting or changing the repository.
- Default: Preview cleanup candidates only; no deletion.

Examples: `/git-cleanup`, `$git-cleanup --apply`, `$git-cleanup --help`.

If `--help` is present, even with other arguments, answer from the inline Usage section above and stop before any tool call, file read, or repository inspection. For an unknown option, explain the error, show this help, and stop. Read the linked files below only for a normal invocation.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitCleanup.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **5. GitCleanup**, `../../references/reconnaissance.md`, and `../../references/decision-matrix.md` — command contract and cleanup criteria.

Execute the canonical `/GitCleanup` command only when the user explicitly invoked this command skill. A semantic match or automatic skill selection is not authorization to write. Preview candidates by default; delete only when the explicit command includes `--apply` and every safety condition still passes. Never delete remote branches unless explicitly asked.
