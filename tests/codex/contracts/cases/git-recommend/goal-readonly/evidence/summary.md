# git-recommend/goal-readonly

- Skill: `git-recommend`
- Feature: Optional goal scopes advice and never mutates repository state
- Result: **PASS**

## Expected behavior

- Uses fresh repository evidence to rank next actions.
- Does not mutate branches, worktrees, or history.

## Contract checks

- PASS `references/commands.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
