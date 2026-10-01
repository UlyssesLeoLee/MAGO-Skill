# git-converge/merge-procedure

- Skill: `git-converge`
- Feature: Sources merge in a fixed order with real merge commits and stop on any failure
- Result: **PASS**

## Expected behavior

- main merges first; larger sources before smaller so a contained source needs no second merge.
- A failing merge is aborted, the whole command stops, nothing is deleted, completed merges stay.

## Contract checks

- PASS `references/commands.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
