# git-converge/acceptance-and-freshness

- Skill: `git-converge`
- Feature: --apply accepts exactly the printed plan; a stale preview stops
- Result: **PASS**

## Expected behavior

- The acceptance covers only the listed tips and never permits writing main or another branch.
- A changed tip after an earlier preview stops the command; new branches are left alone.

## Contract checks

- PASS `SKILL.md`
- PASS `references/commands.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
