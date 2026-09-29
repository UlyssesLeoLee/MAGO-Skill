---
name: git-integrate
description: "检查门禁后集成指定 Agent lane 或分支。"
version: 1.0.0
author: Multi-Agent Git Orchestrator
license: MIT
---

# GitIntegrate

Use this skill when the user explicitly invokes `/git-integrate` in Hermes or `$git-integrate` in Codex. Treat any text following the selected skill name as the command arguments.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitIntegrate.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **4. GitIntegrate**, `../../references/reconnaissance.md`, and `../../references/decision-matrix.md` — command contract and integration gates.

Execute the canonical `/GitIntegrate` command only when the user explicitly invoked this command skill. A semantic match or automatic skill selection is not authorization to write. Check review, dependency, freshness, target protection, and repository policy before integration; stop if any gate fails. Never force-push or rewrite shared history. Ask for a target if none is provided.
