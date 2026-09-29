---
name: git-cleanup
description: "检查可安全清理的 branch 与 worktree，默认只预览候选。"
version: 1.0.0
author: Multi-Agent Git Orchestrator
license: MIT
---

# GitCleanup

Use this skill when the user explicitly invokes `/git-cleanup` in Hermes or `$git-cleanup` in Codex. Treat any text following the selected skill name as the command arguments.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitCleanup.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **5. GitCleanup**, `../../references/reconnaissance.md`, and `../../references/decision-matrix.md` — command contract and cleanup criteria.

Execute the canonical `/GitCleanup` command only when the user explicitly invoked this command skill. A semantic match or automatic skill selection is not authorization to write. Preview candidates by default; delete only when the explicit command includes `--apply` and every safety condition still passes. Never delete remote branches unless explicitly asked.
