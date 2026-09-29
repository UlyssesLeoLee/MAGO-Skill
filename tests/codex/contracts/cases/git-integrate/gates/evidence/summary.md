# git-integrate/gates

- Skill: `git-integrate`
- Feature: Integration stops when review, freshness, dependency, or policy gates fail
- Result: **PASS**

## Expected behavior

- No merge, squash, or cherry-pick occurs without required acceptance and current state.

## Contract checks

- PASS `references/commands.md`
- PASS `skills/git-integrate/SKILL.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
