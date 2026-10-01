# git-converge/hidden-state

- Skill: `git-converge`
- Feature: In-progress sequences and hidden edits keep a worktree
- Result: **PASS**

## Expected behavior

- A paused sequence counts as in progress.
- Edits hidden from status by index flags make a worktree not clean.

## Contract checks

- PASS `references/commands.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
