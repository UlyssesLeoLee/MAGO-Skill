---
name: git-recon
description: "查看仓库状态；/git-recon [--remote] [--help]."
license: MIT
metadata:
  short-description: "查看仓库状态；$git-recon [--remote] [--help]."
---

# GitRecon

Use this skill when the user explicitly invokes `/git-recon` in Hermes or `$git-recon` in Codex. Treat any text following the selected skill name as the command arguments.

## Usage

- Hermes: `/git-recon [--remote] [--help]`
- Codex: `$git-recon [--remote] [--help]`
- `--remote`: Refresh remote-tracking refs before classifying the repository; it does not change branches, worktrees, or commit history.
- `--help`: Show this inline usage and argument description, then stop without inspecting the repository.
- Default: Read-only snapshot using existing local refs; no remote refresh.

Examples: `/git-recon --remote`, `$git-recon --remote`, `$git-recon --help`.

If `--help` is present, even with other arguments, answer from the inline Usage section above and stop before any tool call, file read, or repository inspection. For an unknown option, explain the error, show the same help, and stop. Read the linked files below only for a normal invocation.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitRecon.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **1. GitRecon** and `../../references/reconnaissance.md` — command contract and repository inspection steps.

Execute the canonical `/GitRecon` command with the supplied arguments. Inspect the current repository before reporting state-dependent findings. Default to read-only; `--remote` only permits refreshing remote-tracking refs.
