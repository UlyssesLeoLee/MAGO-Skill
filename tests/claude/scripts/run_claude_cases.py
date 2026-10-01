# ```cypher
# CREATE
#   (file:File {name: "run_claude_cases.py", type: "file", language: "python"}),
#   (v_REPO_ROOT:Variable {name: "REPO_ROOT", type: "variable"}),
#   (v_RESULTS_DIR:Variable {name: "RESULTS_DIR", type: "variable"}),
#   (v_CORE:Variable {name: "CORE", type: "variable"}),
#   (v_ALLOWED_TOOLS:Variable {name: "ALLOWED_TOOLS", type: "variable"}),
#   (v_UNAVAILABLE:Variable {name: "UNAVAILABLE", type: "variable"}),
#   (v_PLAN_MIN_CHARS:Variable {name: "PLAN_MIN_CHARS", type: "variable"}),
#   (v_CLI_INTERNAL_MARKERS:Variable {name: "CLI_INTERNAL_MARKERS", type: "variable"}),
#   (f_trace_env:Function {name: "trace_env", type: "function", signature: "trace_env(root: Path) -> tuple[dict, Path]"}),
#   (f_provision:Function {name: "provision", type: "function", signature: "provision(ctx: dict) -> None"}),
#   (f_prompt_for:Function {name: "prompt_for", type: "function", signature: "prompt_for(scen: dict, ctx: dict) -> str"}),
#   (f_read_log:Function {name: "read_log", type: "function", signature: "read_log(path: Path) -> list[list[str]]"}),
#   (f_cli_internal:Function {name: "cli_internal", type: "function", signature: "cli_internal(args: list[str]) -> bool"}),
#   (f_decoded:Function {name: "decoded", type: "function", signature: "decoded(value) -> str"}),
#   (f_invoke:Function {name: "invoke", type: "function", signature: "invoke(command: list[str], cwd: Path, env: dict, timeout: int) -> dict"}),
#   (f_stream_events:Function {name: "stream_events", type: "function", signature: "stream_events(stdout: str) -> list[dict]"}),
#   (f_result_event:Function {name: "result_event", type: "function", signature: "result_event(stdout: str) -> dict | None"}),
#   (f_transcript_events:Function {name: "transcript_events", type: "function", signature: "transcript_events(stdout: str) -> list[tuple[str, str]]"}),
#   (f_plan_before_write:Function {name: "plan_before_write", type: "function", signature: "plan_before_write(stdout: str, branches: list[str]) -> tuple[bool | None, str]"}),
#   (f_unverified_reason:Function {name: "unverified_reason", type: "function", signature: "unverified_reason(run: dict, result: dict | None, events: list[tuple[str, str]]) -> str | None"}),
#   (f_claude_bin:Function {name: "claude_bin", type: "function", signature: "claude_bin(explicit: str | None) -> str"}),
#   (f_git_bash:Function {name: "git_bash", type: "function", signature: "git_bash() -> Path | None"}),
#   (f_fixture_checks:Function {name: "fixture_checks", type: "function", signature: "fixture_checks(ctx: dict, trace: dict, log: Path, before: dict) -> dict"}),
#   (f_run_case:Function {name: "run_case", type: "function", signature: "run_case(scen: dict, options: argparse.Namespace) -> dict"}),
#   (f_write_evidence:Function {name: "write_evidence", type: "function", signature: "write_evidence(record: dict, folder_root: Path) -> None"}),
#   (f_main:Function {name: "main", type: "function", signature: "main() -> int"}),
#   (file)-[:CONTAINS]->(v_REPO_ROOT),
#   (file)-[:CONTAINS]->(v_RESULTS_DIR),
#   (file)-[:CONTAINS]->(v_CORE),
#   (file)-[:CONTAINS]->(v_ALLOWED_TOOLS),
#   (file)-[:CONTAINS]->(v_UNAVAILABLE),
#   (file)-[:CONTAINS]->(v_PLAN_MIN_CHARS),
#   (file)-[:CONTAINS]->(v_CLI_INTERNAL_MARKERS),
#   (file)-[:CONTAINS]->(f_trace_env),
#   (file)-[:CONTAINS]->(f_provision),
#   (file)-[:CONTAINS]->(f_prompt_for),
#   (file)-[:CONTAINS]->(f_read_log),
#   (file)-[:CONTAINS]->(f_cli_internal),
#   (file)-[:CONTAINS]->(f_decoded),
#   (file)-[:CONTAINS]->(f_invoke),
#   (file)-[:CONTAINS]->(f_stream_events),
#   (file)-[:CONTAINS]->(f_result_event),
#   (file)-[:CONTAINS]->(f_transcript_events),
#   (file)-[:CONTAINS]->(f_plan_before_write),
#   (file)-[:CONTAINS]->(f_unverified_reason),
#   (file)-[:CONTAINS]->(f_claude_bin),
#   (file)-[:CONTAINS]->(f_git_bash),
#   (file)-[:CONTAINS]->(f_fixture_checks),
#   (file)-[:CONTAINS]->(f_run_case),
#   (file)-[:CONTAINS]->(f_write_evidence),
#   (file)-[:CONTAINS]->(f_main),
#   (f_cli_internal)-[:USES]->(v_CLI_INTERNAL_MARKERS),
#   (f_fixture_checks)-[:CALLS]->(f_git_bash),
#   (f_fixture_checks)-[:CALLS]->(f_read_log),
#   (f_invoke)-[:CALLS]->(f_decoded),
#   (f_main)-[:CALLS]->(f_run_case),
#   (f_main)-[:CALLS]->(f_write_evidence),
#   (f_main)-[:USES]->(v_CORE),
#   (f_main)-[:USES]->(v_RESULTS_DIR),
#   (f_plan_before_write)-[:CALLS]->(f_transcript_events),
#   (f_plan_before_write)-[:USES]->(v_PLAN_MIN_CHARS),
#   (f_provision)-[:USES]->(v_REPO_ROOT),
#   (f_result_event)-[:CALLS]->(f_stream_events),
#   (f_run_case)-[:CALLS]->(f_claude_bin),
#   (f_run_case)-[:CALLS]->(f_cli_internal),
#   (f_run_case)-[:CALLS]->(f_fixture_checks),
#   (f_run_case)-[:CALLS]->(f_invoke),
#   (f_run_case)-[:CALLS]->(f_plan_before_write),
#   (f_run_case)-[:CALLS]->(f_prompt_for),
#   (f_run_case)-[:CALLS]->(f_provision),
#   (f_run_case)-[:CALLS]->(f_read_log),
#   (f_run_case)-[:CALLS]->(f_result_event),
#   (f_run_case)-[:CALLS]->(f_trace_env),
#   (f_run_case)-[:CALLS]->(f_transcript_events),
#   (f_run_case)-[:CALLS]->(f_unverified_reason),
#   (f_run_case)-[:USES]->(v_ALLOWED_TOOLS),
#   (f_transcript_events)-[:CALLS]->(f_stream_events),
#   (f_unverified_reason)-[:USES]->(v_UNAVAILABLE),
#   (file)-[:CALLS]->(f_main);
# ```
"""Run GitConverge scenarios through the real Claude Code CLI (`claude -p "/GitConverge ..."`).

Each case builds the scenario's disposable repository, installs commands/GitConverge.md and the orchestrator skill into the
fixture's own `.claude/` (kept out of Git through .git/info/exclude), asks Git to log every process with GIT_TRACE2_EVENT, runs the
slash command headlessly, and judges the result with the scenario oracle plus the command policy on Git's own command trace.

Results are PASS, FAIL, or UNVERIFIED. A run that could not start (session/usage limit, authentication, timeout) or
never looked at the repository is UNVERIFIED, never a pass.
Run: python -X utf8 tests/claude/scripts/run_claude_cases.py [--fixture-check] [--case 'glob'] [--model M]
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import command_policy  # noqa: E402
import gitlab  # noqa: E402
import run_reference_cases  # noqa: E402
import scenarios  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = Path(__file__).resolve().parents[1] / "results" / "claude"
CORE = ["preview-readonly", "happy-path", "conflict-stops", "unrelated-history", "dirty-source-worktree",
        "ignored-overwrite-merge", "tag-shadow", "case-variant-target"]
ALLOWED_TOOLS = ["Bash(git:*)", "Bash(ls:*)", "Bash(cat:*)", "Bash(test:*)", "Bash(pwd)", "Read", "Glob", "Grep", "Skill"]
UNAVAILABLE = re.compile(r"session limit|usage limit|rate limit|limit reached|resets \d|not logged in|/login|authentication|"
                         r"invalid api key|credit balance|overloaded|ECONNRESET|ENOTFOUND", re.I)
PLAN_MIN_CHARS = 300
# Claude Code runs its own housekeeping git calls with this fixed -c prefix; they are not the agent's commands.
CLI_INTERNAL_MARKERS = ("protocol.ext.allow=never", "core.hooksPath=")


def trace_env(root: Path) -> tuple[dict, Path]:
    """Environment that makes Git log every git process (any caller, any PATH) as trace2 JSON events, and the log path."""
    log = root / "git-trace2.jsonl"
    log.write_text("", encoding="utf-8")
    return {"GIT_TRACE2_EVENT": str(log), "GIT_CEILING_DIRECTORIES": str(root)}, log


def provision(ctx: dict) -> None:
    """Install the slash command and the skill into the fixture's .claude/, hidden from Git."""
    repo = Path(ctx["repo"])
    exclude = gitlab.git_paths(repo, ("info/exclude",))["info/exclude"]
    exclude.parent.mkdir(parents=True, exist_ok=True)
    with open(exclude, "a", encoding="utf-8") as handle:
        handle.write(".claude/\n")
    commands = repo / ".claude" / "commands"
    skill = repo / ".claude" / "skills" / "MAGOS"
    commands.mkdir(parents=True, exist_ok=True)
    (skill / "references").mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO_ROOT / "commands" / "GitConverge.md", commands / "GitConverge.md")
    shutil.copy2(REPO_ROOT / "SKILL.md", skill / "SKILL.md")
    for reference in (REPO_ROOT / "references").glob("*.md"):
        shutil.copy2(reference, skill / "references" / reference.name)


def prompt_for(scen: dict, ctx: dict) -> str:
    """The slash command line the user would type."""
    return (f"/GitConverge {ctx['arg']}" + (" --apply" if scen["mode"] == "apply" else "")
            + (" --discard-ignored" if scen["discard"] else ""))


def read_log(path: Path) -> list[list[str]]:
    """Argument lists of top-level git processes from a trace2 event log (nested child processes are skipped)."""
    commands = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("event") == "start" and "/" not in event.get("sid", ""):
            commands.append(list(event["argv"][1:]))
    return commands


def cli_internal(args: list[str]) -> bool:
    """True for Claude Code's own housekeeping git calls (fixed -c prefix), which the agent did not run."""
    return all(any(marker in arg for arg in args) for marker in CLI_INTERNAL_MARKERS)


def decoded(value) -> str:
    """TimeoutExpired carries bytes on POSIX even with text=True; normalize to str."""
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return value or ""


def invoke(command: list[str], cwd: Path, env: dict, timeout: int) -> dict:
    """Run the CLI; a timeout or a CLI that cannot start is reported, not raised."""
    try:
        proc = subprocess.run(command, cwd=str(cwd), env=env, text=True, encoding="utf-8", errors="replace",
                              stdin=subprocess.DEVNULL, capture_output=True, timeout=timeout, check=False)
        return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr, "timed_out": False}
    except subprocess.TimeoutExpired as error:
        return {"returncode": None, "stdout": decoded(error.stdout), "stderr": decoded(error.stderr), "timed_out": True}
    except OSError as error:
        return {"returncode": None, "stdout": "", "stderr": f"could not start the CLI: {error!r}", "timed_out": False}


def stream_events(stdout: str) -> list[dict]:
    """Parsed stream-json events; non-JSON lines are skipped."""
    events = []
    for line in stdout.splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            continue
    return events


def result_event(stdout: str) -> dict | None:
    """The final `result` event of a stream-json transcript, if the CLI finished."""
    found = [event for event in stream_events(stdout) if event.get("type") == "result"]
    return found[-1] if found else None


def transcript_events(stdout: str) -> list[tuple[str, str]]:
    """Ordered ('text', message) and ('bash', command) events from a stream-json transcript."""
    events = []
    for event in stream_events(stdout):
        if event.get("type") != "assistant":
            continue
        for block in event["message"].get("content", []):
            if block.get("type") == "text" and block["text"].strip():
                events.append(("text", block["text"]))
            elif block.get("type") == "tool_use" and block.get("name") in ("Bash", "PowerShell"):
                events.append(("bash", block["input"].get("command", "")))
    return events


def plan_before_write(stdout: str, branches: list[str]) -> tuple[bool | None, str]:
    """Did the agent print a plan that names every local branch before its first repository write?

    Returns (None, reason) when no write happened, so the check does not apply.
    """
    events = transcript_events(stdout)
    first = next((i for i, (kind, body) in enumerate(events) if kind == "bash" and command_policy.writes(body)), None)
    if first is None:
        return None, "no repository write happened"
    printed = "\n".join(body for kind, body in events[:first] if kind == "text")
    missing = [name for name in branches if name not in printed]
    if len(printed) < PLAN_MIN_CHARS:
        return False, f"only {len(printed)} characters of text before the first write (need {PLAN_MIN_CHARS})"
    if missing:
        return False, f"the text before the first write never mentions: {missing}"
    return True, f"{len(printed)} characters naming all {len(branches)} branches"


def unverified_reason(run: dict, result: dict | None, events: list[tuple[str, str]]) -> str | None:
    """Why a run cannot be judged, or None when it can. Liveness comes from the transcript, not the git trace."""
    text = run["stderr"] + " " + (str(result.get("result", "")) if result else "")
    if run["timed_out"]:
        return "timed out"
    if run["returncode"] is None and not result:
        return run["stderr"][:160] or "the CLI did not start"
    if result is None:
        return "no result event: the CLI did not finish"
    if result.get("is_error") or result.get("subtype") != "success":
        if UNAVAILABLE.search(text):
            return "CLI unavailable (limit/auth)"
        return f"the CLI ended with {result.get('subtype')!r}"
    if not any(kind == "bash" and command_policy.shell_git_calls(body) for kind, body in events):
        return "the agent never inspected the repository"
    return None


def claude_bin(explicit: str | None) -> str:
    """The Claude Code CLI: --claude-bin, then $CLAUDE_BIN, then PATH, then the default install location."""
    for candidate in (explicit, os.environ.get("CLAUDE_BIN"), shutil.which("claude")):
        if candidate:
            return candidate
    for name in ("claude.exe", "claude"):
        default = Path.home() / ".local" / "bin" / name
        if default.is_file():
            return str(default)
    return "claude"


def git_bash() -> Path | None:
    """Git Bash next to the Git install (found from `git --exec-path`, whichever git.exe PATH resolves)."""
    exec_path = subprocess.run(["git", "--exec-path"], text=True, capture_output=True, check=False).stdout.strip()
    for parent in Path(exec_path).parents:
        candidate = parent / "bin" / "bash.exe"
        if candidate.is_file():
            return candidate
    return Path("/bin/bash") if Path("/bin/bash").is_file() else None


def fixture_checks(ctx: dict, trace: dict, log: Path, before: dict) -> dict:
    """Verify the harness without a model: installed files, clean status, and trace2 logging from each shell."""
    env = {**os.environ, **trace}
    repo = Path(ctx["repo"])
    bash = git_bash()
    shells = []
    if bash:
        shells.append(("Git Bash", [str(bash), "-c", "git --version"]))
    if sys.platform == "win32":
        shells.append(("cmd.exe", ["cmd", "/c", "git --version"]))
    outputs = {name: subprocess.run(command, env=env, text=True, capture_output=True, cwd=str(repo), check=False).stdout
               for name, command in shells}
    logged = read_log(log)
    results = [("the command and skill are installed in the fixture",
                (repo / ".claude" / "commands" / "GitConverge.md").is_file() and (repo / ".claude" / "skills" / "MAGOS" / "SKILL.md").is_file()),
               ("the .claude folder appears in no worktree status", all(".claude" not in (w["status"] or "") for w in before["worktrees"]))]
    results += [(f"git still runs under {name}", out.startswith("git version")) for name, out in outputs.items()]
    results.append(("trace2 logged every shell's git call", logged.count(["--version"]) >= len(shells)))
    results.append(("Git Bash was found", bash is not None))
    checks = [{"name": name, "passed": bool(ok)} for name, ok in results]
    return {"status": "PASS" if all(c["passed"] for c in checks) else "FAIL", "checks": checks, "git_calls_seen": len(logged)}


def run_case(scen: dict, options: argparse.Namespace) -> dict:
    """One scenario through the real CLI."""
    with gitlab.fixture_root(options.fixture_root) as root:
        ctx = scen["build"](root)
        provision(ctx)
        trace, log = trace_env(root)
        before = scenarios.snapshot(ctx)
        prompt = prompt_for(scen, ctx)
        record = {"id": scen["id"], "title": scen["title"], "mode": scen["mode"], "prompt": prompt}
        if options.fixture_check:
            return run_reference_cases.scrub({**record, **fixture_checks(ctx, trace, log, before)}, root)
        command = [claude_bin(options.claude_bin), "-p", prompt, "--output-format", "stream-json", "--verbose", "--no-session-persistence",
                   "--setting-sources", "project,local", "--permission-mode", "default",
                   "--max-budget-usd", str(options.max_budget), "--allowedTools", *ALLOWED_TOOLS]
        if options.model:
            command += ["--model", options.model]
        run = invoke(command, Path(ctx["repo"]), {**os.environ, **trace}, options.timeout)
        after = scenarios.snapshot(ctx)
        commands = [args for args in read_log(log) if not cli_internal(args)]
        result = result_event(run["stdout"])
        events = transcript_events(run["stdout"])
        text = str(result.get("result", "")) if result else run["stdout"][-2000:]
        record["final_answer"] = text[-1500:]
        reason = unverified_reason(run, result, events)
        if reason:
            record.update({"status": "UNVERIFIED", "reason": reason, "checks": []})
        else:
            pairs = list(scen["oracle"](ctx, before, after)) + scenarios.invariants(ctx, before, after)
            words = list(scen["report"]) + (sorted(before["heads"]) if scen["mode"] == "preview" else [])
            pairs += [(f"the final answer mentions {word!r}", word in text) for word in words]
            checks = [{"name": name, "passed": bool(passed)} for name, passed in pairs]
            if scen["mode"] == "apply":
                planned, detail = plan_before_write(run["stdout"], sorted(before["heads"]))
                if planned is not None:
                    checks.append({"name": "the plan is printed before the first write", "passed": planned, "detail": detail})
            breaches = command_policy.violations(commands, scen["mode"])
            checks.append({"name": "command policy: no forbidden git command" + (" and read-only preview" if scen["mode"] == "preview" else ""),
                           "passed": not breaches, **({"detail": breaches} if breaches else {})})
            record.update({"status": "PASS" if all(c["passed"] for c in checks) else "FAIL", "checks": checks})
        record.update({"before": before, "after": after, "git_commands": commands, "claude_returncode": run["returncode"],
                       "result_subtype": result.get("subtype") if result else None})
        record["_raw"] = {"stdout": run["stdout"], "stderr": run["stderr"]}
        return run_reference_cases.scrub(record, root)


def write_evidence(record: dict, folder_root: Path) -> None:
    """case.json, transcript, git command log, snapshots, result.json, summary.md."""
    folder = folder_root / record["id"]
    folder.mkdir(parents=True, exist_ok=True)
    raw = record.pop("_raw", {})
    if raw:
        (folder / "transcript.jsonl").write_text(raw["stdout"], encoding="utf-8")
        (folder / "stderr.txt").write_text(raw["stderr"], encoding="utf-8")
    (folder / "prompt.txt").write_text(record["prompt"] + "\n", encoding="utf-8")
    (folder / "result.json").write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [f"# {record['id']}", "", f"- Prompt: `{record['prompt']}`", f"- Result: **{record['status']}**"]
    if record.get("reason"):
        lines.append(f"- Reason: {record['reason']}")
    lines += ["", "## Checks", ""] + [f"- {'PASS' if c['passed'] else 'FAIL'} {c['name']}" for c in record["checks"]]
    (folder / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", help="scenario id glob; default is the core set")
    parser.add_argument("--fixture-check", action="store_true", help="build and provision fixtures without calling the model")
    parser.add_argument("--fixture-root", help="short directory for fixtures (Windows path length)")
    parser.add_argument("--model", help="model alias or id passed to claude --model")
    parser.add_argument("--claude-bin", help="path to the Claude Code CLI (default: $CLAUDE_BIN, PATH, ~/.local/bin)")
    parser.add_argument("--timeout", type=int, default=900, help="seconds per case")
    parser.add_argument("--max-budget", type=float, default=3.0, help="USD cap per case")
    options = parser.parse_args()
    patterns = options.case or CORE
    # Scenarios with a custom flow need harness steps between invocations; a single `claude -p` cannot reproduce them.
    chosen = [s for s in scenarios.REGISTRY.values()
              if s["claude"] and not s["flow"] and any(fnmatch.fnmatch(s["id"], p) for p in patterns)]
    if not chosen:
        parser.error(f"no Claude runtime scenario matches {patterns}")
    folder_root = RESULTS_DIR / ("fixture-check" if options.fixture_check else "runtime")
    records = []
    for scen in chosen:
        record = run_case(scen, options)
        write_evidence(record, folder_root)
        records.append(record)
        print(f"{record['status']:10} {record['id']}" + (f"  ({record['reason']})" if record.get("reason") else ""))
        for check in record["checks"]:
            if not check["passed"]:
                print(f"            FAIL: {check['name']} {check.get('detail', '')}")
    counts = {status: sum(r["status"] == status for r in records) for status in ("PASS", "FAIL", "UNVERIFIED")}
    print(f"{counts['PASS']}/{len(records)} passed (FAIL={counts['FAIL']} UNVERIFIED={counts['UNVERIFIED']})")
    return 1 if counts["FAIL"] else (2 if counts["UNVERIFIED"] else 0)


if __name__ == "__main__":
    raise SystemExit(main())
