# git-converge/package-wiring

- Skill: `git-converge`
- Feature: The sync script, docs, and pressure tests all know about the sixth command
- Result: **PASS**

## Expected behavior

- sync_hosts.py installs commands/GitConverge.md for Claude.
- Docs list /GitConverge, /git-converge, and $git-converge.
- Pressure tests describe the GitConverge scenarios.

## Contract checks

- PASS `scripts/sync_hosts.py`
- PASS `README.md`
- PASS `references/installation.md`
- PASS `references/pressure-tests.md`
- PASS `SKILL.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
