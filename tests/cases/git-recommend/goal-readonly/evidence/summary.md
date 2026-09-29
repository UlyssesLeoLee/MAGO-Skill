# git-recommend/goal-readonly

- Skill: `git-recommend`
- Feature: Optional goal scopes advice and never mutates repository state
- Result: **PASS**

## Expected behavior

- Uses fresh repository evidence to rank next actions.
- Does not mutate branches, worktrees, or history.

## Contract checks

- PASS `commands/GitRecommend.md`
- PASS `references/commands.md`

Evidence scope: source-contract check; this case does not invoke Claude Code, Hermes, or Codex.
