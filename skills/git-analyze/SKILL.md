---
name: git-analyze
description: "深入分析指定分支或 worktree，并评估集成与历史改写风险。"
version: 1.0.0
author: Multi-Agent Git Orchestrator
license: MIT
---

# GitAnalyze

Use this skill when the user explicitly invokes `/git-analyze` in Hermes or `$git-analyze` in Codex. Treat any text following the selected skill name as the command arguments.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitAnalyze.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **2. GitAnalyze** and `../../references/reconnaissance.md` — command contract and repository inspection steps.

Execute the canonical `/GitAnalyze` command with the supplied arguments. Inspect the target's current state, ancestry, unique commits, dependencies, and worktree cleanliness before assessing operations. Keep the analysis read-only; `--remote` only permits refreshing remote-tracking refs. Ask for a target if none is provided.
