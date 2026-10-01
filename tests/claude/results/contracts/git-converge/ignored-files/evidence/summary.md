# git-converge/ignored-files

- Skill: `git-converge`
- Feature: Ignored files are never destroyed silently
- Result: **PASS**

## Expected behavior

- A merge that would overwrite an ignored file stops the command.
- A worktree holding ignored files is kept unless --discard-ignored is given.

## Contract checks

- PASS `references/commands.md`
- PASS `commands/GitConverge.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
