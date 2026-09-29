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
- `<lane|branch>`: Required source lane or branch to integrate.
- `--strategy <value>`: Optional integration strategy. `auto` follows repository policy and reviewed acceptance shape (default); `merge` preserves accepted lane commits; `squash` delivers the lane as one commit when allowed; `cherry-pick` uses only accepted, dependency-safe commits.
- `--help`: Show this inline usage and argument description, then stop without inspecting or changing the repository.
- Default: Strategy `auto`; integration proceeds only after review, dependency, freshness, protection, and repository-policy gates pass.

Examples: `/git-integrate agent/auth`, `$git-integrate agent/auth --strategy squash`, `$git-integrate --help`.

If `--help` is present, even with other arguments, answer from the inline Usage section above and stop before any tool call, file read, or repository inspection. If the source target or strategy value is missing or invalid, show this help and ask for a valid value; for an unknown option, explain the error and show this help. Do not inspect or change the repository in these error cases. Read the linked files below only for a normal invocation.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitIntegrate.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **4. GitIntegrate**, `../../references/reconnaissance.md`, and `../../references/decision-matrix.md` — command contract and integration gates.

Execute the canonical `/GitIntegrate` command only when the user explicitly invoked this command skill. A semantic match or automatic skill selection is not authorization to write. Check review, dependency, freshness, target protection, and repository policy before integration; stop if any gate fails. Never force-push or rewrite shared history. Ask for a target if none is provided.
