# git-converge/target-required

- Skill: `git-converge`
- Feature: A missing or unsupported branch argument is reported, not guessed
- Result: **PASS**

## Expected behavior

- Asks for a branch when none is given.
- Rejects main, a missing branch, and a case-only mismatch without writing.

## Contract checks

- PASS `commands/GitConverge.md`
- PASS `skills/git-converge/SKILL.md`
- PASS `references/commands.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
