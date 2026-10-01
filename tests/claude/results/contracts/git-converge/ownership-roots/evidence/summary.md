# git-converge/ownership-roots

- Skill: `git-converge`
- Feature: Claude Code session worktrees are owned; unknown owners are surfaced
- Result: **PASS**

## Expected behavior

- Worktrees under the project-local .claude/worktrees are active owners.
- Removing an unknown-owner worktree is listed in the plan.

## Contract checks

- PASS `references/commands.md`
- PASS `SKILL.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
