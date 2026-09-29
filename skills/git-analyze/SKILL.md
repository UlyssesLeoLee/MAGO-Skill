---
name: git-analyze
description: "分析目标；/git-analyze TARGET [--remote] [--help]."
license: MIT
metadata:
  short-description: "分析目标；$git-analyze TARGET [--remote] [--help]."
---

# GitAnalyze

Use this skill when the user explicitly invokes `/git-analyze` in Hermes or `$git-analyze` in Codex. Treat any text following the selected skill name as the command arguments.

## Usage

- Hermes: `/git-analyze <branch|worktree> [--remote] [--help]`
- Codex: `$git-analyze <branch|worktree> [--remote] [--help]`
- The target is required. `--help` prints section **2. GitAnalyze** in `../../references/commands.md` and stops without repository inspection. If the target is missing, ask for it; reject unknown options and show the usage.

Resolve these files relative to this file and follow their instructions:

1. `../../SKILL.md` — shared orchestration rules and safety invariants.
2. `../../commands/GitAnalyze.md` — command-specific invocation and safety defaults. Do not interpret Claude template placeholders as literal arguments.
3. `../../references/commands.md` section **2. GitAnalyze** and `../../references/reconnaissance.md` — command contract and repository inspection steps.

Execute the canonical `/GitAnalyze` command with the supplied arguments. Inspect the target's current state, ancestry, unique commits, dependencies, and worktree cleanliness before assessing operations. Keep the analysis read-only; `--remote` only permits refreshing remote-tracking refs. Ask for a target if none is provided.
