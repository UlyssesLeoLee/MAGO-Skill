# git-cleanup/apply-safe-only

- Skill: `git-cleanup`
- Feature: Apply rechecks and removes only safe local candidates
- Result: **PASS**

## Expected behavior

- Rechecks candidate state immediately before mutation.
- Leaves dirty, unique-work, dependent, and remote branches untouched.

## Contract checks

- PASS `references/commands.md`
- PASS `skills/git-cleanup/SKILL.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
