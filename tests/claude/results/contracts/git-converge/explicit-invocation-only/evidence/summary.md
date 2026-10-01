# git-converge/explicit-invocation-only

- Skill: `git-converge`
- Feature: No host writes unless the user explicitly invoked the command
- Result: **PASS**

## Expected behavior

- Claude and Codex disable automatic selection; Hermes refuses by instruction.
- A missing skill or shared file leaves only a preview.

## Contract checks

- PASS `commands/GitConverge.md`
- PASS `skills/git-converge/agents/openai.yaml`
- PASS `skills/git-converge/SKILL.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
