---
name: git-recon
description: "调查当前仓库的分支与 worktree 状态并生成风险快照。"
version: 1.0.0
author: Multi-Agent Git Orchestrator
license: MIT
---

# GitRecon

Use this skill when the user explicitly invokes `/git-recon` in Hermes or `$git-recon` in Codex. Treat any text following the selected skill name as the command arguments.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitRecon.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **1. GitRecon** and `../../references/reconnaissance.md` — command contract and repository inspection steps.

Execute the canonical `/GitRecon` command with the supplied arguments. Inspect the current repository before reporting state-dependent findings. Default to read-only; `--remote` only permits refreshing remote-tracking refs.
