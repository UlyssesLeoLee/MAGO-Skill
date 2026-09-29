---
name: git-integrate
description: "集成目标；/git-integrate TARGET [--strategy] [--help]."
license: MIT
metadata:
  short-description: "集成目标；$git-integrate TARGET [--strategy] [--help]."
---

# GitIntegrate

Use this skill when the user explicitly invokes `/git-integrate` in Hermes or `$git-integrate` in Codex. Treat any text following the selected skill name as the command arguments.

## Usage

- Hermes: `/git-integrate <lane|branch> [--strategy auto|merge|squash|cherry-pick] [--help]`
- Codex: `$git-integrate <lane|branch> [--strategy auto|merge|squash|cherry-pick] [--help]`
- The source target is required; `--strategy` defaults to `auto`. `--help` prints section **4. GitIntegrate** in `../../references/commands.md` and stops without repository inspection. If the target or strategy value is missing or invalid, show the usage and do not integrate.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitIntegrate.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **4. GitIntegrate**, `../../references/reconnaissance.md`, and `../../references/decision-matrix.md` — command contract and integration gates.

Execute the canonical `/GitIntegrate` command only when the user explicitly invoked this command skill. A semantic match or automatic skill selection is not authorization to write. Check review, dependency, freshness, target protection, and repository policy before integration; stop if any gate fails. Never force-push or rewrite shared history. Ask for a target if none is provided.
