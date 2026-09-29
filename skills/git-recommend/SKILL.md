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
- `goal` is optional natural-language text. `--help` prints section **3. GitRecommend** in `../../references/commands.md` and stops without repository inspection. Treat `--remote` as an option only when it is a standalone argument; reject other unknown options and show the usage.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitRecommend.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **3. GitRecommend** and `../../references/reconnaissance.md` — command contract and repository inspection steps.

Execute the canonical `/GitRecommend` command with the supplied arguments. Inspect the current repository first, and run or reuse a fresh reconnaissance snapshot before recommending. Recommendations are advisory and must not mutate repository topology.
