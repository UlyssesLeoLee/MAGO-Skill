# git-converge/refname-safety

- Skill: `git-converge`
- Feature: Branches resolve through full refnames and recorded SHAs
- Result: **PASS**

## Expected behavior

- Merges use the recorded SHA, never a bare name that a tag could shadow.
- The target is matched exactly against refs/heads.

## Contract checks

- PASS `references/commands.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
