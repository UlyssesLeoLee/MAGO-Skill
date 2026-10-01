# git-converge/preview-default

- Skill: `git-converge`
- Feature: Without --apply the command changes nothing
- Result: **PASS**

## Expected behavior

- Reports gates, merge order, classifications, expected final branches, and what is not touched.
- Does not merge, switch, delete, prune, or fetch.

## Contract checks

- PASS `references/commands.md`
- PASS `SKILL.md`
- PASS `commands/GitConverge.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
