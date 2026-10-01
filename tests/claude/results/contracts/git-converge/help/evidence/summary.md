# git-converge/help

- Skill: `git-converge`
- Feature: Help returns usage before repository inspection on every host
- Result: **PASS**

## Expected behavior

- Shows syntax, argument descriptions, defaults, and examples.
- Does not inspect or change a repository.

## Contract checks

- PASS `commands/GitConverge.md`
- PASS `skills/git-converge/SKILL.md`
- PASS `references/commands.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
