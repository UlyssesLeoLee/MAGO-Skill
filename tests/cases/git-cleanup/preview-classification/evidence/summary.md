# git-cleanup/preview-classification

- Skill: `git-cleanup`
- Feature: Preview classifies safe and blocked candidates without changes
- Result: **PASS**

## Expected behavior

- Shows evidence for each candidate and its block reason.
- Leaves all refs and worktrees unchanged in preview mode.

## Contract checks

- PASS `references/commands.md`
- PASS `skills/git-cleanup/SKILL.md`

Evidence scope: source-contract check; this case does not invoke Claude Code, Hermes, or Codex.
