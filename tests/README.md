# Command Skill Contract Cases

This directory contains one case folder per command behavior. `cases.json` defines each test object, invocation, expected behavior, and source-contract assertions. Running `run_cases.py` materializes each case under `cases/<skill>/<case>/` and stores `input.json`, `result.json`, and `summary.md` in that case's `evidence/` directory.

Run the suite from the repository root:

```powershell
python tests/run_cases.py
```

The cases check that each skill's documented interface, argument hints, help behavior, output contract, and safety gates remain present and consistent. Scenario inputs are retained with each case's evidence so they can also be used for manual evaluation in Claude Code, Hermes, or Codex.

This suite verifies repository contracts; it does not launch any AI host or claim to verify host-specific autocomplete rendering. Claude's `argument-hint` metadata, Hermes descriptions, and Codex short descriptions are checked as source data only.
