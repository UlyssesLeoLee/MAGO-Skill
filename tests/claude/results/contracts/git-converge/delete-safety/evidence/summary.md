# git-converge/delete-safety

- Skill: `git-converge`
- Feature: Deletion rechecks, scoped worktree removal, and never a forced delete
- Result: **PASS**

## Expected behavior

- Each deletion is rechecked immediately before it happens.
- Worktrees are removed by path without --force; no repository-wide prune; no branch -D.

## Contract checks

- PASS `references/commands.md`
- PASS `commands/GitConverge.md`
- PASS `skills/git-converge/SKILL.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
