# git-converge/two-axis-classification

- Skill: `git-converge`
- Feature: Each source has one merge status (with precedence) and separate delete blockers
- Result: **PASS**

## Expected behavior

- A source in a dirty/locked/owned worktree is still merged; only deletion is blocked.
- Merge status precedence is explicit.

## Contract checks

- PASS `references/commands.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
