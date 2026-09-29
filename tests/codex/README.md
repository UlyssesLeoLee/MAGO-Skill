# Codex skill tests

All test cases for this repository are collected here. Runtime tests invoke the installed Codex CLI against disposable Git repositories under the system temporary directory. They never run integration or cleanup against this repository.

For each runtime case, the runner copies that skill and its referenced documents from the active test checkout into the fixture's project-local `.agents/skills` root, records the copied-source hash, and leaves the user's `.codex/develop_codex` worktree untouched.

Run the source-contract checks:

```powershell
python -X utf8 tests/codex/contracts/run_contract_cases.py
```

These checks verify that Codex skill metadata, inline help, command contracts, and safety rules remain present. Their result is labelled `source-contract`; it does not count as a runtime behavior pass.

Validate that the temporary Git fixtures are constructed correctly without using Codex:

```powershell
python -X utf8 tests/codex/run_host_cases.py --fixture-check
```

Run actual Codex behavior cases:

```powershell
python -X utf8 tests/codex/run_host_cases.py
```

The runner calls `$git-*` skills through `codex exec`, records the prompt, CLI transcript, and Git state before and after each invocation, then checks observable output and repository changes. Every case writes evidence under `tests/codex/host_cases/<skill>/<case>/evidence/host-codex/`. Results are `PASS`, `FAIL`, or `UNVERIFIED`; missing CLI access, authentication, quota, sandbox, or timeouts are never reported as passes. Use `--case 'git-integrate/*'` to select cases and `--codex-sandbox workspace-write` to set the child CLI's sandbox. Integration and cleanup write tests only use their disposable fixture.

The case manifest covers every command, required and optional arguments, branch and worktree targets, all integration strategies, acceptance gates, cleanup preview/apply, and stale-state rechecks. Codex CLI tests verify skill selection and behavior; they do not measure the gray hint rendering in the desktop composer.
