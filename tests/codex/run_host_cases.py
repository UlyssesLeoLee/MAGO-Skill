"""cypher
CREATE
  (f:File {name:'run_host_cases.py', type:'file', language:'python'}),
  (g:Function {name:'git', type:'function'}),
  (w:Function {name:'write_json', type:'function'}),
  (s:Function {name:'snapshot', type:'function'}),
  (p:Function {name:'prepare_fixture', type:'function'}),
  (project_skill:Function {name:'provision_codex_skill', type:'function'}),
  (root:Variable {name:'ROOT', type:'variable'}),
  (tool_types:Variable {name:'tool_item_types', type:'variable'}),
  (v:Function {name:'verify_fixture', type:'function'}),
  (c:Function {name:'host_command', type:'function'}),
  (x:Function {name:'extract_response', type:'function'}),
  (i:Function {name:'invoke_host', type:'function'}),
  (e:Function {name:'evaluate', type:'function'}),
  (r:Function {name:'run_case', type:'function'}),
  (m:Function {name:'main', type:'function'}),
  (run:Function {name:'subprocess.run', type:'function'}),
  (dump:Function {name:'json.dumps', type:'function'}),
  (write:Function {name:'Path.write_text', type:'function'}),
  (read:Function {name:'Path.read_text', type:'function'}),
  (mkdir:Function {name:'Path.mkdir', type:'function'}),
  (copytree:Function {name:'shutil.copytree', type:'function'}),
  (rglob:Function {name:'Path.rglob', type:'function'}),
  (read_bytes:Function {name:'Path.read_bytes', type:'function'}),
  (as_posix:Function {name:'Path.as_posix', type:'function'}),
  (sha256:Function {name:'hashlib.sha256', type:'function'}),
  (which:Function {name:'shutil.which', type:'function'}),
  (temp:Function {name:'tempfile.TemporaryDirectory', type:'function'}),
  (f)-[:CONTAINS]->(g), (f)-[:CONTAINS]->(w), (f)-[:CONTAINS]->(s),
  (f)-[:CONTAINS]->(p), (f)-[:CONTAINS]->(project_skill), (f)-[:CONTAINS]->(v), (f)-[:CONTAINS]->(c),
  (f)-[:CONTAINS]->(x), (f)-[:CONTAINS]->(i), (f)-[:CONTAINS]->(e),
  (f)-[:CONTAINS]->(r), (f)-[:CONTAINS]->(m),
  (g)-[:CALLS]->(run), (w)-[:CALLS]->(dump), (w)-[:CALLS]->(write),
  (s)-[:CALLS]->(g), (s)-[:CALLS]->(as_posix), (p)-[:CALLS]->(g), (p)-[:CALLS]->(mkdir),
  (v)-[:CALLS]->(s), (v)-[:CALLS]->(g), (c)-[:CALLS]->(which),
  (x)-[:CALLS]->(read), (i)-[:CALLS]->(run), (e)-[:CALLS]->(g),
  (x)-[:USES]->(tool_types),
  (r)-[:CALLS]->(p), (r)-[:CALLS]->(project_skill), (r)-[:CALLS]->(v), (r)-[:CALLS]->(s),
  (r)-[:CALLS]->(c), (r)-[:CALLS]->(i), (r)-[:CALLS]->(x),
  (r)-[:CALLS]->(e), (r)-[:CALLS]->(w), (r)-[:CALLS]->(temp),
  (m)-[:CALLS]->(read), (m)-[:CALLS]->(r),
  (project_skill)-[:CALLS]->(copytree),
  (project_skill)-[:CALLS]->(rglob), (project_skill)-[:CALLS]->(read_bytes),
  (project_skill)-[:CALLS]->(sha256), (project_skill)-[:CALLS]->(read),
  (project_skill)-[:CALLS]->(write),
  (project_skill)-[:CALLS]->(mkdir),
  (project_skill)-[:USES]->(root), (f)-[:CONTAINS]->(root);
"""

"""Run real Git-skill invocations in disposable fixtures and retain evidence."""

import argparse
import copy
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parents[1]
CASES = TESTS / "host_cases"
MANIFEST = TESTS / "host_cases.json"
HOST_NAME = {
    "git-recon": "$git-recon",
    "git-analyze": "$git-analyze",
    "git-recommend": "$git-recommend",
    "git-integrate": "$git-integrate",
    "git-cleanup": "$git-cleanup",
}
RUNTIME_ERROR = re.compile(
    r"(?i)(insufficient.?(?:credit|balance)|usage limit|rate limit|quota|"
    r"authentication|not logged in|login required|api.?key|billing|"
    r"CreateProcessAsUserW|sandbox.*(?:denied|failed)|permission denied|"
    r"access is denied|interrupted.update|auto.recover.*install|"
    r"could not.*(?:connect|resolve)|model.*unavailable|provider.*error)"
)


def git(directory: Path, *args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", "-C", str(directory), *args],
        text=True, encoding="utf-8", errors="replace", capture_output=True,
        timeout=30, check=False,
    )
    if check and completed.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {completed.stderr.strip()}")
    return completed.stdout.strip()


def is_ancestor(directory: Path, ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(directory), "merge-base", "--is-ancestor", ancestor, descendant],
        text=True, encoding="utf-8", errors="replace", capture_output=True,
        timeout=30, check=False,
    )
    if completed.returncode not in (0, 1):
        raise RuntimeError(f"git merge-base failed: {completed.stderr.strip()}")
    return completed.returncode == 0


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def snapshot(fixture: dict) -> dict:
    root = fixture["cwd"]
    if fixture["kind"] == "empty":
        files = {}
        for path in root.rglob("*"):
            if path.is_file() and ".git" not in path.relative_to(root).parts:
                files[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        return {"files": files, "git_repository": (root / ".git").exists()}
    refs = {}
    for line in git(root, "for-each-ref", "--format=%(refname) %(objectname)").splitlines():
        ref, sha = line.split(" ", 1)
        refs[ref] = sha
    worktree_text = git(root, "worktree", "list", "--porcelain")
    worktrees = {}
    for line in worktree_text.splitlines():
        if line.startswith("worktree "):
            worktree_path = Path(line[9:])
            worktrees[str(worktree_path)] = {
                "head": git(worktree_path, "rev-parse", "HEAD"),
                "branch": git(worktree_path, "branch", "--show-current"),
                "status": git(worktree_path, "status", "--porcelain=v1", "--untracked-files=all"),
            }
    files = {}
    for worktree_path in worktrees:
        base = Path(worktree_path)
        for path in base.rglob("*"):
            if path.is_file() and ".git" not in path.relative_to(base).parts:
                files[f"{base.name}/{path.relative_to(base).as_posix()}"] = hashlib.sha256(path.read_bytes()).hexdigest()
    bare_refs = {}
    if fixture.get("remote"):
        for line in git(fixture["remote"], "for-each-ref", "--format=%(refname) %(objectname)").splitlines():
            ref, sha = line.split(" ", 1)
            bare_refs[ref] = sha
    return {"git_repository": True, "refs": refs, "worktrees": worktrees,
            "files": files, "bare_refs": bare_refs}


def prepare_fixture(base: Path, kind: str) -> dict:
    if kind == "empty":
        cwd = base / "empty"
        cwd.mkdir()
        git(cwd, "init", "-b", "main")
        return {"kind": kind, "cwd": cwd, "base": base}
    repo = base / "repo"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    remote = repo / ".git" / "acceptance-origin.git"
    remote.mkdir()
    git(remote, "init", "--bare", "--initial-branch=main")
    git(repo, "config", "user.name", "MAGOS Acceptance")
    git(repo, "config", "user.email", "acceptance@example.invalid")
    (repo / "README.md").write_text("fixture\n", encoding="utf-8")
    git(repo, "add", "README.md")
    git(repo, "commit", "-m", "initial")
    git(repo, "remote", "add", "origin", str(remote))
    git(repo, "push", "-u", "origin", "main")
    fixture = {"kind": kind, "cwd": repo, "base": base, "remote": remote}
    if kind in {"branch", "remote", "integrate"}:
        git(repo, "switch", "-c", "agent/auth")
        (repo / "feature.txt").write_text("accepted feature\n", encoding="utf-8")
        git(repo, "add", "feature.txt")
        git(repo, "commit", "-m", "agent auth feature")
        fixture["lane_head"] = git(repo, "rev-parse", "HEAD")
        git(repo, "switch", "main")
        if kind in {"branch", "remote"}:
            worktree = base / "auth-worktree"
            git(repo, "worktree", "add", str(worktree), "agent/auth")
            (worktree / "feature.txt").write_text("accepted feature\ndirty edit\n", encoding="utf-8")
            fixture["worktree"] = worktree
        if kind == "remote":
            publisher = base / "publisher"
            git(base, "clone", str(remote), str(publisher))
            git(publisher, "config", "user.name", "MAGOS Publisher")
            git(publisher, "config", "user.email", "publisher@example.invalid")
            (publisher / "remote.txt").write_text("remote advance\n", encoding="utf-8")
            git(publisher, "add", "remote.txt")
            git(publisher, "commit", "-m", "advance origin main")
            git(publisher, "push", "origin", "main")
            fixture["remote_head"] = git(publisher, "rev-parse", "HEAD")
    elif kind == "cleanup":
        git(repo, "switch", "-c", "agent/done")
        (repo / "done.txt").write_text("merged work\n", encoding="utf-8")
        git(repo, "add", "done.txt")
        git(repo, "commit", "-m", "completed work")
        git(repo, "switch", "main")
        git(repo, "merge", "--no-ff", "--no-edit", "agent/done")
        git(repo, "switch", "-c", "agent/unique")
        (repo / "unique.txt").write_text("unmerged work\n", encoding="utf-8")
        git(repo, "add", "unique.txt")
        git(repo, "commit", "-m", "unique work")
        git(repo, "switch", "-c", "agent/dependent")
        (repo / "dependent.txt").write_text("depends on unique\n", encoding="utf-8")
        git(repo, "add", "dependent.txt")
        git(repo, "commit", "-m", "dependent work")
        git(repo, "switch", "main")
        git(repo, "branch", "agent/dirty")
        worktree = base / "dirty-worktree"
        git(repo, "worktree", "add", str(worktree), "agent/dirty")
        (worktree / "README.md").write_text("fixture\ndirty edit\n", encoding="utf-8")
        fixture["worktree"] = worktree
    return fixture


def verify_fixture(fixture: dict, state: dict) -> list[dict]:
    kind = fixture["kind"]
    checks = []
    if kind == "empty":
        checks.append({"name": "empty Git repository", "passed": state["git_repository"]})
        if fixture.get("skill"):
            skill_file = f".agents/skills/{fixture['skill']}/SKILL.md"
            checks.append({"name": "project-local Codex skill is present",
                           "passed": skill_file in state["files"]})
            checks.append({"name": "workspace contains only the skill scaffold",
                           "passed": all(path.startswith(".agents/") for path in state["files"])})
        else:
            checks.append({"name": "workspace is empty", "passed": not state["files"]})
    else:
        refs = state["refs"]
        checks.append({"name": "main and local origin exist",
                       "passed": "refs/heads/main" in refs and "refs/remotes/origin/main" in refs})
        checks.append({"name": "bare origin exists", "passed": bool(state["bare_refs"])})
        if kind in {"branch", "remote", "integrate"}:
            checks.append({"name": "unmerged lane exists", "passed":
            "refs/heads/agent/auth" in refs and not is_ancestor(fixture["cwd"], "agent/auth", "main")})
        if kind in {"branch", "remote"}:
            checks.append({"name": "dirty lane worktree exists", "passed":
                           str(fixture["worktree"]) in state["worktrees"] and
                           bool(state["worktrees"][str(fixture["worktree"])]["status"])})
        if kind == "remote":
            checks.append({"name": "remote tracking ref is stale", "passed":
                           refs["refs/remotes/origin/main"] != fixture["remote_head"] and
                           state["bare_refs"]["refs/heads/main"] == fixture["remote_head"]})
        if kind == "cleanup":
            checks.append({"name": "safe, dirty, unique, dependent candidates exist",
                           "passed": all(f"refs/heads/agent/{name}" in refs for name in
                                         ("done", "dirty", "unique", "dependent"))})
            checks.append({"name": "done is merged and unique is not", "passed":
                           is_ancestor(fixture["cwd"], "agent/done", "main") and
                           not is_ancestor(fixture["cwd"], "agent/unique", "main") and
                           bool(state["worktrees"][str(fixture["worktree"])]["status"])})
    return checks


def provision_codex_skill(fixture: dict, skill: str) -> None:
    """Expose the exact checkout skill through Codex's project-local discovery path."""
    if skill not in HOST_NAME:
        raise ValueError(f"Unknown Codex skill fixture: {skill}")
    workspace = fixture["cwd"]
    agents = workspace / ".agents"
    skill_target = agents / "skills" / skill
    agents.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "skills" / skill, skill_target)
    shutil.copytree(ROOT / "references", agents / "references")
    fixture["skill"] = skill
    fixture["skill_path"] = str(skill_target / "SKILL.md")
    copied_files = sorted(path for path in agents.rglob("*") if path.is_file())
    fixture["skill_source_sha256"] = hashlib.sha256("\n".join(
        f"{path.relative_to(agents).as_posix()}:{hashlib.sha256(path.read_bytes()).hexdigest()}"
        for path in copied_files
    ).encode("utf-8")).hexdigest()
    git_directory = workspace / ".git"
    if git_directory.is_dir():
        exclude = git_directory / "info" / "exclude"
        existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
        if "/.agents/" not in existing.splitlines():
            exclude.write_text(existing.rstrip() + "\n/.agents/\n", encoding="utf-8")


def host_command(cwd: Path, prompt: str, options: argparse.Namespace) -> list[str] | None:
    executable = shutil.which("codex.cmd") or shutil.which("codex")
    if not executable:
        return None
    command = [executable, "exec", "--json", "--ephemeral",
               "-C", str(cwd), "-s", options.codex_sandbox,
               "-c", 'model_reasoning_effort="low"']
    if options.model:
        command += ["-m", options.model]
    return command + [prompt]


def extract_response(stdout: str) -> tuple[str, list[str], bool]:
    messages = []
    tool_calls = []
    tool_item_types = {
        "command_execution", "file_change", "mcp_tool_call", "collab_tool_call",
        "web_search", "function_call", "tool_call",
    }
    parsed_any = False
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        parsed_any = True
        item = event.get("item", {})
        if isinstance(item, dict):
            if item.get("type") == "agent_message" and item.get("text"):
                messages.append(str(item["text"]))
            if item.get("type") in tool_item_types:
                tool_calls.append(json.dumps(item, ensure_ascii=False))
        message = event.get("message", {})
        if isinstance(message, dict):
            for block in message.get("content", []):
                if isinstance(block, dict) and block.get("type") == "text":
                    messages.append(str(block.get("text", "")))
                elif isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_calls.append(json.dumps(block.get("input", {}), ensure_ascii=False))
        if event.get("type") == "result" and isinstance(event.get("result"), str):
            messages.append(event["result"])
    return "\n".join(messages).strip(), tool_calls, parsed_any


def invoke_host(command: list[str], cwd: Path, base: Path, timeout: int) -> dict:
    started = datetime.now(timezone.utc).isoformat()
    environment = os.environ.copy()
    environment["GIT_CEILING_DIRECTORIES"] = str(base)
    try:
        completed = subprocess.run(command, cwd=cwd, env=environment, text=True,
                                   encoding="utf-8", errors="replace", capture_output=True,
                                   timeout=timeout, check=False)
        return {"started_utc": started, "returncode": completed.returncode,
                "stdout": completed.stdout, "stderr": completed.stderr, "timed_out": False}
    except subprocess.TimeoutExpired as error:
        return {"started_utc": started, "returncode": None,
                "stdout": str(error.stdout or ""), "stderr": str(error.stderr or ""),
                "timed_out": True}
    except OSError as error:
        return {"started_utc": started, "returncode": None,
                "stdout": "", "stderr": repr(error), "timed_out": False}


def evaluate(spec: dict, fixture: dict, before: dict, after: dict,
             answer: str, tool_calls: list[str], trace: bool,
             preview: str = "", mutated: dict | None = None) -> list[dict]:
    assertion = spec["assertion"]
    text = answer.casefold()
    def add(name: str, passed: bool) -> None:
        checks.append({"name": name, "passed": bool(passed)})
    def unchanged(allow_remote: bool = False) -> bool:
        first, second = copy.deepcopy(before), copy.deepcopy(after)
        if allow_remote:
            for item in (first, second):
                item["refs"] = {k: v for k, v in item["refs"].items()
                                if not k.startswith("refs/remotes/")}
        return first == second
    def has_any(*words: str) -> bool:
        return any(word.casefold() in text for word in words)
    checks = []
    if assertion == "help":
        add("usage includes --help", "--help" in text)
        option = {"git-recon": "--remote", "git-analyze": "--remote",
                  "git-recommend": "--remote", "git-integrate": "--strategy",
                  "git-cleanup": "--apply"}[spec["id"].split("/")[0]]
        add("usage describes command option", option in text)
        add("repository state remains unchanged", before == after)
        add("structured trace permits inspection check", trace)
        add("no tool call", not tool_calls)
    elif assertion == "recon":
        add("reports main and agent/auth", "main" in text and "agent/auth" in text)
        add("reports dirty state", has_any("dirty", "未提交", "脏", "修改"))
        add("read-only Git state", unchanged())
    elif assertion in {"remote", "remote-recommend"}:
        add("origin/main refreshed", after["refs"].get("refs/remotes/origin/main") == fixture["remote_head"])
        add("branches, worktrees and files unchanged", unchanged(allow_remote=True))
        add("reports remote refresh", has_any("remote", "远端", "远程", "fetch"))
        if assertion == "remote-recommend":
            add("mentions requested lane", "agent/auth" in text)
    elif assertion in {"analyze", "analyze-worktree", "operation-matrix"}:
        add("identifies requested lane", "agent/auth" in text or
            (assertion == "analyze-worktree" and "auth-worktree" in text))
        add("compares with main", "main" in text)
        add("read-only Git state", unchanged())
        if assertion == "analyze-worktree":
            add("identifies dirty worktree", has_any("dirty", "未提交", "脏", "修改"))
        if assertion == "operation-matrix":
            for operation in ("merge", "rebase", "cherry-pick", "squash", "cleanup"):
                add(f"assesses {operation}", operation in text or
                    (operation == "cleanup" and has_any("delete", "清理", "删除")))
    elif assertion == "missing-target":
        add("requests target", has_any("target", "branch", "worktree", "目标", "分支"))
        add("read-only Git state", unchanged())
    elif assertion == "recommend":
        add("mentions candidate", "agent/auth" in text)
        add("read-only Git state", unchanged())
    elif assertion == "integration-gate":
        add("review gate reported", has_any("review", "acceptance", "评审", "审核", "验收"))
        add("no integration performed", unchanged())
    elif assertion == "invalid-strategy":
        add("invalid strategy reported", has_any("invalid", "unsupported", "strategy", "无效", "不支持", "策略"))
        add("no integration performed", unchanged())
    elif assertion.startswith("integration-"):
        main_before = before["refs"]["refs/heads/main"]
        main_after = after["refs"]["refs/heads/main"]
        add("main advanced", main_before != main_after)
        add("source branch retained", after["refs"].get("refs/heads/agent/auth") == fixture["lane_head"])
        add("feature content in main", git(fixture["cwd"], "show", "main:feature.txt", check=False) == "accepted feature")
        add("worktrees clean", all(not tree["status"] for tree in after["worktrees"].values()))
        add("remote unchanged", before["bare_refs"] == after["bare_refs"])
        ancestry = is_ancestor(fixture["cwd"], fixture["lane_head"], "main")
        if assertion == "integration-merge":
            add("source is ancestor of main", ancestry)
        elif assertion in {"integration-squash", "integration-cherry-pick"}:
            add("source SHA not imported", not ancestry)
        add("reports post-validation", has_any("validat", "verif", "验证", "检查", "确认"))
    elif assertion == "cleanup-preview":
        add("classifies merged candidate", "agent/done" in text)
        add("identifies dirty or unique work", "agent/dirty" in text or "agent/unique" in text)
        add("preview leaves Git state unchanged", unchanged())
    elif assertion == "cleanup-apply":
        refs = after["refs"]
        add("merged safe branch removed", "refs/heads/agent/done" not in refs)
        add("dirty, unique and dependent branches retained", all(
            f"refs/heads/agent/{name}" in refs for name in ("dirty", "unique", "dependent")))
        add("main and remote unchanged", before["refs"]["refs/heads/main"] == refs["refs/heads/main"] and
            before["bare_refs"] == after["bare_refs"])
        add("dirty worktree preserved", str(fixture["worktree"]) in after["worktrees"] and
            bool(after["worktrees"][str(fixture["worktree"])]["status"]))
    elif assertion == "cleanup-stale":
        add("preview names safe candidate", "agent/done" in preview.casefold() and
            any(word in preview.casefold() for word in ("safe", "安全", "可清理")))
        add("candidate changed between calls", bool(mutated) and
            before["refs"]["refs/heads/agent/done"] != mutated["refs"]["refs/heads/agent/done"])
        add("stale candidate retained", after["refs"].get("refs/heads/agent/done") ==
            (mutated or {}).get("refs", {}).get("refs/heads/agent/done"))
        add("apply leaves mutated state unchanged", after == mutated)
        add("recheck reason reported", has_any("changed", "unique", "not integrated", "unmerged", "变更", "未合并", "重新检查"))
    return checks


def run_case(spec: dict, options: argparse.Namespace) -> dict:
    case_dir = CASES / spec["id"]
    evidence = case_dir / "evidence" / ("fixture-check" if options.fixture_check else f"host-{options.host}")
    evidence.mkdir(parents=True, exist_ok=True)
    write_json(case_dir / "host_case.json", spec)
    with tempfile.TemporaryDirectory(prefix=".magos-accept-", dir=TESTS) as temporary:
        fixture = prepare_fixture(Path(temporary), spec["fixture"])
        if not options.fixture_check:
            provision_codex_skill(fixture, spec["id"].split("/")[0])
        before = snapshot(fixture)
        checks = verify_fixture(fixture, before)
        write_json(evidence / "fixture.json", {
            "kind": fixture["kind"], "checks": checks, "initial_state": before,
            "skill": fixture.get("skill"), "skill_path": fixture.get("skill_path"),
            "skill_source_sha256": fixture.get("skill_source_sha256"),
        })
        if not all(item["passed"] for item in checks):
            result = {"case": spec["id"], "status": "FAIL", "scope": "fixture setup",
                      "checks": checks}
            write_json(evidence / "result.json", result)
            return result
        if options.fixture_check:
            result = {"case": spec["id"], "status": "PASS", "scope": "fixture setup only; no AI host invoked",
                      "checks": checks}
            write_json(evidence / "result.json", result)
            return result
        skill = spec["id"].split("/")[0]
        args = spec["args"].format(worktree=fixture.get("worktree", ""))
        invocation = (HOST_NAME[skill] + " " + args).strip()
        context = spec.get("context", "").format(lane_head=fixture.get("lane_head", ""))
        prompt = (f"Invoke the project-local MAGOS skill from this acceptance-test checkout exactly as requested: {invocation}\n"
                  f"The current working directory is a disposable acceptance-test fixture. "
                  f"Operate only in this fixture and its local origin; do not touch other repositories.\n{context}")
        command = host_command(fixture["cwd"], prompt, options)
        write_json(evidence / "invocation.json", {"host": options.host, "cwd": str(fixture["cwd"]),
                                                  "skill_path": fixture["skill_path"],
                                                  "skill_source_sha256": fixture["skill_source_sha256"],
                                                  "command": command, "prompt": prompt,
                                                  "timeout_seconds": options.timeout})
        if not command:
            result = {"case": spec["id"], "status": "UNVERIFIED", "scope": "host runtime",
                      "reason": "host executable unavailable"}
            write_json(evidence / "result.json", result)
            return result
        first = invoke_host(command, fixture["cwd"], fixture["base"], options.timeout)
        write_json(evidence / "first_call.json", {k: v for k, v in first.items() if k not in {"stdout", "stderr"}})
        (evidence / "first_stdout.txt").write_text(first["stdout"], encoding="utf-8")
        (evidence / "first_stderr.txt").write_text(first["stderr"], encoding="utf-8")
        first_answer, first_calls, first_trace = extract_response(first["stdout"])
        preview = ""
        mutated = None
        last = first
        answer, calls, trace = first_answer, first_calls, first_trace
        if spec["assertion"] == "cleanup-stale" and first["returncode"] == 0 and first_answer:
            preview = first_answer
            after_preview = snapshot(fixture)
            write_json(evidence / "after_preview.json", after_preview)
            if after_preview == before:
                repo = fixture["cwd"]
                git(repo, "switch", "agent/done")
                (repo / "late.txt").write_text("new work after preview\n", encoding="utf-8")
                git(repo, "add", "late.txt")
                git(repo, "commit", "-m", "new work after cleanup preview")
                git(repo, "switch", "main")
                mutated = snapshot(fixture)
                write_json(evidence / "between_calls.json", {"operation": "new unique commit on agent/done",
                                                       "state": mutated})
                second_invocation = HOST_NAME[skill] + " " + spec["followup_args"]
                second_prompt = (f"Invoke the project-local MAGOS skill from this acceptance-test checkout exactly as requested: {second_invocation}. "
                                 "A candidate changed after the previous preview. Recheck it before applying cleanup. "
                                 "Operate only in this disposable fixture and its local origin.")
                second_command = host_command(repo, second_prompt, options)
                write_json(evidence / "second_invocation.json", {"command": second_command,
                                                                   "prompt": second_prompt, "cwd": str(repo)})
                last = invoke_host(second_command, repo, fixture["base"], options.timeout)
                (evidence / "second_stdout.txt").write_text(last["stdout"], encoding="utf-8")
                (evidence / "second_stderr.txt").write_text(last["stderr"], encoding="utf-8")
                answer, calls, trace = extract_response(last["stdout"])
                write_json(evidence / "second_call.json", {k: v for k, v in last.items() if k not in {"stdout", "stderr"}})
        after = snapshot(fixture)
        write_json(evidence / "before.json", before)
        write_json(evidence / "after.json", after)
        write_json(evidence / "observed.json", {"answer": answer, "tool_calls": calls,
                                               "structured_trace": trace, "preview_answer": preview})
        error_text = first["stdout"] + "\n" + first["stderr"] + "\n" + last["stdout"] + "\n" + last["stderr"]
        if first["timed_out"] or last["timed_out"] or first["returncode"] != 0 or last["returncode"] != 0 or not answer:
            reason = "host timed out" if first["timed_out"] or last["timed_out"] else (
                "host runtime/auth/model/sandbox error" if RUNTIME_ERROR.search(error_text) else
                "host did not return a usable agent response")
            result = {"case": spec["id"], "status": "UNVERIFIED", "scope": "host runtime", "reason": reason,
                      "returncode": last["returncode"]}
        elif spec["assertion"] == "help" and not trace:
            result = {"case": spec["id"], "status": "UNVERIFIED", "scope": "host runtime",
                      "reason": "structured tool trace unavailable; cannot check no repository inspection"}
        else:
            assertions = evaluate(spec, fixture, before, after, answer, calls, trace, preview, mutated)
            result = {"case": spec["id"], "status": "PASS" if all(x["passed"] for x in assertions) else "FAIL",
                      "scope": "actual host CLI invocation and disposable Git state", "assertions": assertions}
        write_json(evidence / "result.json", result)
        lines = [f"# {spec['id']} — {options.host}", "", f"Status: **{result['status']}**",
                 f"Scope: {result['scope']}", "", f"Reason: {result.get('reason', 'See assertions in result.json')}",
                 "", "Evidence: invocation.json, first_stdout.txt, first_stderr.txt, before.json, after.json, observed.json."]
        (evidence / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Real host CLI acceptance in disposable Git fixtures")
    parser.add_argument("--host", choices=("codex",), default="codex", help="Only Codex is executed")
    parser.add_argument("--case", action="append", default=[], help="glob case ID; repeatable")
    parser.add_argument("--fixture-check", action="store_true", help="verify fixture setup only; no model calls")
    parser.add_argument("--model", help="optional host model override")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--codex-sandbox", choices=("read-only", "workspace-write", "danger-full-access"),
                        default="workspace-write")
    options = parser.parse_args()
    specs = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = [spec for spec in specs if not options.case or
                any(fnmatch.fnmatchcase(spec["id"], pattern) for pattern in options.case)]
    if not selected:
        parser.error("no case matches --case")
    if options.fixture_check:
        fixture_specs = []
        seen_fixtures = set()
        for spec in selected:
            if spec["fixture"] not in seen_fixtures:
                fixture_specs.append(spec)
                seen_fixtures.add(spec["fixture"])
        selected = fixture_specs
    results = [run_case(spec, options) for spec in selected]
    for result in results:
        print(f"{result['status']:10} {result['case']}")
    counts = {status: sum(item["status"] == status for item in results)
              for status in ("PASS", "FAIL", "UNVERIFIED")}
    label = "fixture setups" if options.fixture_check else "Codex host cases"
    print(f"{label}: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIED']} UNVERIFIED")
    return 1 if counts["FAIL"] else (2 if counts["UNVERIFIED"] else 0)


if __name__ == "__main__":
    raise SystemExit(main())
