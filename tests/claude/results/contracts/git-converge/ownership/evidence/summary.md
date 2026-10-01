# git-converge/ownership

- Skill: `git-converge`
- Feature: Only the invoking worktree is written to; other actors' worktrees are protected
- Result: **PASS**

## Expected behavior

- The command writes only into the invoking worktree.
- Another actor's worktree is never removed or switched; its committed content is still merged.

## Contract checks

- PASS `references/commands.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
