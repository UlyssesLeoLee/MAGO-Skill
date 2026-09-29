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
- `--help` prints the usage and examples from section **1. GitRecon** in `../../references/commands.md`, then stops without inspecting the repository. Reject unknown options and show the same help.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitRecon.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **1. GitRecon** and `../../references/reconnaissance.md` — command contract and repository inspection steps.

Execute the canonical `/GitRecon` command with the supplied arguments. Inspect the current repository before reporting state-dependent findings. Default to read-only; `--remote` only permits refreshing remote-tracking refs.
