# ```cypher
# CREATE
#   (file:File {name: "run_reference_cases.py", type: "file", language: "python"}),
#   (v_RESULTS_DIR:Variable {name: "RESULTS_DIR", type: "variable"}),
#   (f_scrub:Function {name: "scrub", type: "function", signature: "scrub(value, root: Path)"}),
#   (f_default_flow:Function {name: "default_flow", type: "function", signature: "default_flow(ctx: dict, scen: dict) -> dict"}),
#   (f_collect_commands:Function {name: "collect_commands", type: "function", signature: "collect_commands(value) -> list[list[str]]"}),
#   (f_run_one:Function {name: "run_one", type: "function", signature: "run_one(scen: dict, fixture_base: str | None) -> dict"}),
#   (f_write_evidence:Function {name: "write_evidence", type: "function", signature: "write_evidence(outcome: dict) -> None"}),
#   (f_write_evidence_lambda_92_11:Function {name: "write_evidence.lambda_92_11", type: "function", signature: "lambda_92_11(name, data)"}),
#   (f_main:Function {name: "main", type: "function", signature: "main() -> int"}),
#   (file)-[:CONTAINS]->(v_RESULTS_DIR),
#   (file)-[:CONTAINS]->(f_scrub),
#   (file)-[:CONTAINS]->(f_default_flow),
#   (file)-[:CONTAINS]->(f_collect_commands),
#   (file)-[:CONTAINS]->(f_run_one),
#   (file)-[:CONTAINS]->(f_write_evidence),
#   (f_write_evidence)-[:CONTAINS]->(f_write_evidence_lambda_92_11),
#   (file)-[:CONTAINS]->(f_main),
#   (f_main)-[:CALLS]->(f_run_one),
#   (f_main)-[:CALLS]->(f_write_evidence),
#   (f_main)-[:USES]->(v_RESULTS_DIR),
#   (f_run_one)-[:CALLS]->(f_collect_commands),
#   (f_run_one)-[:CALLS]->(f_default_flow),
#   (f_run_one)-[:CALLS]->(f_scrub),
#   (f_write_evidence)-[:USES]->(v_RESULTS_DIR),
#   (file)-[:CALLS]->(f_main);
# ```
"""Run the GitConverge scenarios against the reference executor and record evidence.

Each scenario builds a disposable repository, runs the reference executor (preview or apply), snapshots the result, and
judges it with the scenario oracle. Evidence goes to tests/claude/results/reference/<scenario>/.
Run: python -X utf8 tests/claude/scripts/run_reference_cases.py [--case 'glob'] [--fixture-root <short path>]
"""

from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path
import re
import sys
import traceback

sys.path.insert(0, str(Path(__file__).resolve().parent))
import command_policy  # noqa: E402
import converge_ref  # noqa: E402
import gitlab  # noqa: E402
import scenarios  # noqa: E402

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results" / "reference"


def scrub(value, root: Path):
    """Replace the fixture root (every spelling) and the random temp name so evidence is stable between runs."""
    spellings = {str(root), root.as_posix(), str(root.resolve()), root.resolve().as_posix(),
                 str(root).replace("\\", "\\\\")}
    if isinstance(value, str):
        for spelling in sorted(spellings, key=len, reverse=True):
            value = value.replace(spelling, "<root>")
        return re.sub(r"mgc-\w+", "mgc-XXXX", value)
    if isinstance(value, dict):
        return {scrub(key, root): scrub(item, root) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [scrub(item, root) for item in value]
    return value


def default_flow(ctx: dict, scen: dict) -> dict:
    """Preview scenarios call survey(); apply scenarios call apply()."""
    if scen["mode"] == "preview":
        return {"plan": converge_ref.survey(ctx["repo"], ctx["arg"], scen["discard"], ctx["harness_roots"])}
    return {"report": converge_ref.apply(ctx["repo"], ctx["arg"], scen["discard"], harness_roots=ctx["harness_roots"])}


def collect_commands(value) -> list[list[str]]:
    """Every recorded git command under any 'commands' key of a result tree."""
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "commands" and isinstance(item, list):
                found.extend(item)
            else:
                found.extend(collect_commands(item))
    return found


def run_one(scen: dict, fixture_base: str | None) -> dict:
    """Run one scenario; returns its verdict, checks, and the evidence payload."""
    if scen["platforms"] and sys.platform not in scen["platforms"]:
        return {"id": scen["id"], "status": "SKIPPED", "checks": [], "note": f"runs only on {scen['platforms']}"}
    with gitlab.fixture_root(fixture_base) as root:
        try:
            ctx = scen["build"](root)
            before = scenarios.snapshot(ctx)
            result = scen["flow"](ctx, converge_ref, scen) if scen["flow"] else default_flow(ctx, scen)
            after = scenarios.snapshot(ctx)
            baseline = ctx.get("baseline") or before
            checks = list(scen["oracle"](ctx, baseline, after)) + scenarios.invariants(ctx, baseline, after)
            if scen["plan_oracle"]:
                checks += list(scen["plan_oracle"](ctx, result))
            rows = [{"name": name, "passed": bool(passed)} for name, passed in checks]
            breaches = command_policy.violations(collect_commands(result), scen["mode"])
            rows.append({"name": "command policy: no forbidden git command" + (" and read-only preview" if scen["mode"] == "preview" else ""),
                         "passed": not breaches, **({"detail": breaches} if breaches else {})})
            status = "PASS" if rows and all(row["passed"] for row in rows) else "FAIL"
            payload = {"before": baseline, "after": after, "result": result}
        except Exception:  # noqa: BLE001 - a crash is reported as ERROR with its traceback
            rows, status, payload = [], "ERROR", {"traceback": traceback.format_exc()}
        return scrub({"id": scen["id"], "title": scen["title"], "mode": scen["mode"], "status": status, "checks": rows,
                      "evidence": payload}, root)


def write_evidence(outcome: dict) -> None:
    """One directory per scenario: case.json, before/after snapshots, result.json, summary.md."""
    folder = RESULTS_DIR / outcome["id"]
    folder.mkdir(parents=True, exist_ok=True)
    evidence = outcome.get("evidence", {})
    dump = lambda name, data: (folder / name).write_text(  # noqa: E731
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    dump("case.json", {"id": outcome["id"], "title": outcome.get("title"), "mode": outcome.get("mode")})
    if "before" in evidence:
        dump("before.json", evidence["before"])
        dump("after.json", evidence["after"])
    dump("result.json", {"status": outcome["status"], "checks": outcome["checks"], "result": evidence.get("result"),
                         "traceback": evidence.get("traceback"), "note": outcome.get("note")})
    lines = [f"# {outcome['id']}", "", f"- Title: {outcome.get('title', '')}", f"- Mode: {outcome.get('mode', '')}",
             f"- Result: **{outcome['status']}**", "", "## Checks", ""]
    lines += [f"- {'PASS' if row['passed'] else 'FAIL'} {row['name']}" for row in outcome["checks"]] or ["- (none)"]
    if evidence.get("traceback"):
        lines += ["", "## Error", "", "```", evidence["traceback"].rstrip(), "```"]
    (folder / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", help="scenario id glob; repeat to select several")
    parser.add_argument("--fixture-root", help="short directory for fixtures (Windows path length)")
    parser.add_argument("--no-evidence", action="store_true", help="do not write evidence files")
    options = parser.parse_args()
    patterns = options.case or ["*"]
    chosen = [scen for scen in scenarios.REGISTRY.values() if any(fnmatch.fnmatch(scen["id"], p) for p in patterns)]
    outcomes = []
    for scen in chosen:
        outcome = run_one(scen, options.fixture_root)
        outcomes.append(outcome)
        if not options.no_evidence:
            write_evidence(outcome)
        print(f"{outcome['status']:7} {outcome['id']}")
        for row in outcome["checks"]:
            if not row["passed"]:
                print(f"          FAIL: {row['name']}")
        if outcome["status"] == "ERROR":
            print(outcome["evidence"]["traceback"])
    counts = {status: sum(o["status"] == status for o in outcomes) for status in ("PASS", "FAIL", "ERROR", "SKIPPED")}
    print(f"{counts['PASS']}/{len(outcomes)} scenarios passed "
          f"(FAIL={counts['FAIL']} ERROR={counts['ERROR']} SKIPPED={counts['SKIPPED']})")
    if not options.no_evidence:
        rows = ["# Reference executor results", "", "| Scenario | Result | Checks |", "|---|---|---|"]
        rows += [f"| `{o['id']}` | {o['status']} | {sum(r['passed'] for r in o['checks'])}/{len(o['checks'])} |"
                 for o in outcomes]
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        (RESULTS_DIR / "summary.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    return 0 if counts["FAIL"] == 0 and counts["ERROR"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
