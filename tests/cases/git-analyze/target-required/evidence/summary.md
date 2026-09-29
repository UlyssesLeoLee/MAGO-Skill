# git-analyze/target-required

- Skill: `git-analyze`
- Feature: Branch and worktree targets are accepted; a missing target is requested
- Result: **PASS**

## Expected behavior

- Resolves the requested target and compares it with the integration target.
- A missing target prompts the user and does not guess.

## Contract checks

- PASS `skills/git-analyze/SKILL.md`
- PASS `references/commands.md`

Evidence scope: source-contract check; this case does not invoke Claude Code, Hermes, or Codex.
