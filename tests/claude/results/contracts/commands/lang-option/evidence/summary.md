# commands/lang-option

- Skill: `git-converge`
- Feature: Every command accepts --lang <language>; the reply is Chinese when it is absent
- Result: **PASS**

## Expected behavior

- All six Claude wrappers list --lang in the argument hint, the usage line, the options, and the execution step.
- All six adapters list --lang in both host usage lines and in the execution section.
- The canonical contract defines the option once and every command's argument table repeats it.

## Contract checks

- PASS `commands/GitRecon.md`
- PASS `commands/GitAnalyze.md`
- PASS `commands/GitRecommend.md`
- PASS `commands/GitIntegrate.md`
- PASS `commands/GitCleanup.md`
- PASS `commands/GitConverge.md`
- PASS `skills/git-recon/SKILL.md`
- PASS `skills/git-analyze/SKILL.md`
- PASS `skills/git-recommend/SKILL.md`
- PASS `skills/git-integrate/SKILL.md`
- PASS `skills/git-cleanup/SKILL.md`
- PASS `skills/git-converge/SKILL.md`
- PASS `references/commands.md`
- PASS `SKILL.md`
- PASS `references/pressure-tests.md`

Evidence scope: source-contract check; no AI host CLI is invoked.
