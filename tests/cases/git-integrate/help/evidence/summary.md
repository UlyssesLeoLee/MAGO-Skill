# git-integrate/help

- Skill: `git-integrate`
- Feature: Help lists strategy choices and never performs integration
- Result: **PASS**

## Expected behavior

- Lists required source target, allowed strategies, default, and safety gates without repository inspection.

## Contract checks

- PASS `commands/GitIntegrate.md`
- PASS `references/commands.md`

Evidence scope: source-contract check; this case does not invoke Claude Code, Hermes, or Codex.
