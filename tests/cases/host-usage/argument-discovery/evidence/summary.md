# host-usage/argument-discovery

- Skill: `all`
- Feature: Each host exposes the best available parameter hint
- Result: **PASS**

## Expected behavior

- Claude command metadata includes argument hints.
- Hermes skill descriptions include concise invocation syntax.
- Codex short descriptions include invocation syntax and --help.
- Full option explanations are available through --help.

## Contract checks

- PASS `commands/GitAnalyze.md`
- PASS `skills/git-analyze/SKILL.md`
- PASS `skills/git-analyze/agents/openai.yaml`
- PASS `README.md`
- PASS `skills/git-recon/SKILL.md`
- PASS `skills/git-analyze/SKILL.md`
- PASS `skills/git-recommend/SKILL.md`
- PASS `skills/git-integrate/SKILL.md`
- PASS `skills/git-cleanup/SKILL.md`
- PASS `skills/git-recon/agents/openai.yaml`
- PASS `skills/git-analyze/agents/openai.yaml`
- PASS `skills/git-recommend/agents/openai.yaml`
- PASS `skills/git-integrate/agents/openai.yaml`
- PASS `skills/git-cleanup/agents/openai.yaml`

Evidence scope: source-contract check; this case does not invoke Claude Code, Hermes, or Codex.
