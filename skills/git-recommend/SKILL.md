---
name: git-recommend
description: "基于仓库真实状态推荐 Git 操作与多 Agent 下一步。"
version: 1.0.0
author: Multi-Agent Git Orchestrator
license: MIT
---

# GitRecommend

Use this skill when the user explicitly invokes `/git-recommend` in Hermes or `$git-recommend` in Codex. Treat any text following the selected skill name as the command arguments.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitRecommend.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **3. GitRecommend** and `../../references/reconnaissance.md` — command contract and repository inspection steps.

Execute the canonical `/GitRecommend` command with the supplied arguments. Inspect the current repository first, and run or reuse a fresh reconnaissance snapshot before recommending. Recommendations are advisory and must not mutate repository topology.
