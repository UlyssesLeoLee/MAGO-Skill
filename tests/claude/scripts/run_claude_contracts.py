# ```cypher
# CREATE
#   (file:File {name: "run_claude_contracts.py", type: "file", language: "python"}),
#   (v_TESTS_CLAUDE:Variable {name: "TESTS_CLAUDE", type: "variable"}),
#   (v_CODEX_CONTRACTS:Variable {name: "CODEX_CONTRACTS", type: "variable"}),
#   (v_MANIFEST:Variable {name: "MANIFEST", type: "variable"}),
#   (v_CASES_DIR:Variable {name: "CASES_DIR", type: "variable"}),
#   (f_load_engine:Function {name: "load_engine", type: "function", signature: "load_engine()"}),
#   (f_main:Function {name: "main", type: "function", signature: "main() -> int"}),
#   (file)-[:CONTAINS]->(v_TESTS_CLAUDE),
#   (file)-[:CONTAINS]->(v_CODEX_CONTRACTS),
#   (file)-[:CONTAINS]->(v_MANIFEST),
#   (file)-[:CONTAINS]->(v_CASES_DIR),
#   (file)-[:CONTAINS]->(f_load_engine),
#   (file)-[:CONTAINS]->(f_main),
#   (f_load_engine)-[:USES]->(v_CASES_DIR),
#   (f_load_engine)-[:USES]->(v_CODEX_CONTRACTS),
#   (f_main)-[:CALLS]->(f_load_engine),
#   (f_main)-[:USES]->(v_MANIFEST),
#   (file)-[:CALLS]->(f_main);
# ```
"""Run the GitConverge source-contract cases (tests/claude/contracts/cases.json).

Reuses the check engine of tests/codex/contracts/run_contract_cases.py so the evidence format is identical; only the
manifest and the evidence folder differ. These checks read files; they do not start any AI host.
Run: python -X utf8 tests/claude/scripts/run_claude_contracts.py
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

TESTS_CLAUDE = Path(__file__).resolve().parents[1]
CODEX_CONTRACTS = TESTS_CLAUDE.parent / "codex" / "contracts"
MANIFEST = TESTS_CLAUDE / "contracts" / "cases.json"
CASES_DIR = TESTS_CLAUDE / "results" / "contracts"


def load_engine():
    """Import the codex contract runner under another module name and point its evidence folder at tests/claude."""
    sys.path.insert(0, str(CODEX_CONTRACTS))
    spec = importlib.util.spec_from_file_location("codex_contract_engine", CODEX_CONTRACTS / "run_contract_cases.py")
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    engine.CASES_DIR = CASES_DIR
    return engine


def main() -> int:
    engine = load_engine()
    specs = json.loads(MANIFEST.read_text(encoding="utf-8"))
    results = [engine.run_case(spec) for spec in specs]
    for result in results:
        print(f"{'PASS' if result['passed'] else 'FAIL'} {result['case']}")
        for check in result["checks"]:
            for missing in check["missing"]:
                print(f"     missing in {check['file']}: {missing}")
    passed = sum(1 for result in results if result["passed"])
    print(f"{passed}/{len(results)} GitConverge source-contract cases passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
