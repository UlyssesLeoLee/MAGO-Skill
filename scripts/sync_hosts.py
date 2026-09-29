# ```cypher
# CREATE
#   (file:File {name: 'sync_hosts.py', type: 'file', language: 'python'}),
#   (module:Module {name: 'sync_hosts', type: 'module', language: 'python'}),
#   (command_names:Variable {name: 'COMMAND_NAMES', type: 'variable'}),
#   (skill_names:Variable {name: 'SKILL_NAMES', type: 'variable'}),
#   (command_paths:Variable {name: 'COMMAND_PATHS', type: 'variable'}),
#   (paths:Variable {name: 'SYNC_PATHS', type: 'variable'}),
#   (build:Function {name: 'build_targets', type: 'function'}),
#   (hash:Function {name: 'file_sha256', type: 'function'}),
#   (inspect:Function {name: 'inspect', type: 'function'}),
#   (copy:Function {name: 'copy_file', type: 'function'}),
#   (render:Function {name: 'render', type: 'function'}),
#   (main:Function {name: 'main', type: 'function'}),
#   (selected_hosts:Variable {name: 'selected_hosts', type: 'variable'}),
#   (file)-[:CONTAINS]->(module),
#   (module)-[:CONTAINS]->(command_names),
#   (module)-[:CONTAINS]->(skill_names),
#   (module)-[:CONTAINS]->(command_paths),
#   (module)-[:CONTAINS]->(paths),
#   (module)-[:CONTAINS]->(build),
#   (module)-[:CONTAINS]->(hash),
#   (module)-[:CONTAINS]->(inspect),
#   (module)-[:CONTAINS]->(copy),
#   (module)-[:CONTAINS]->(render),
#   (module)-[:CONTAINS]->(main),
#   (build)-[:USES]->(command_paths),
#   (build)-[:USES]->(paths),
#   (inspect)-[:CALLS]->(build),
#   (inspect)-[:CALLS]->(hash),
#   (inspect)-[:USES]->(paths),
#   (main)-[:CALLS]->(inspect),
#   (main)-[:CALLS]->(build),
#   (main)-[:CALLS]->(copy),
#   (main)-[:CALLS]->(render),
#   (main)-[:USES]->(selected_hosts),
#   (build)-[:USES]->(selected_hosts),
#   (inspect)-[:USES]->(selected_hosts);
# ```
"""Compare or synchronize MAGOS adapters in existing user-level installs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile


COMMAND_NAMES = ("GitRecon", "GitAnalyze", "GitRecommend", "GitIntegrate", "GitCleanup")
SKILL_NAMES = ("git-recon", "git-analyze", "git-recommend", "git-integrate", "git-cleanup")
COMMAND_PATHS = tuple(f"commands/{name}.md" for name in COMMAND_NAMES)
SYNC_PATHS = (
    "references/commands.md",
    *COMMAND_PATHS,
    *(f"skills/{name}/SKILL.md" for name in SKILL_NAMES),
    *(f"skills/{name}/agents/openai.yaml" for name in SKILL_NAMES),
)


def build_targets(home: Path, selected_hosts: tuple[str, ...]) -> tuple[tuple[str, Path, Path, tuple[str, ...]], ...]:
    """Return host, target root, required installed directory, and relative files."""
    claude = home / ".claude"
    codex = home / ".codex" / "skills" / "MAGOS"
    hermes = home / ".hermes" / "skills" / "multi-agent-git-orchestrator"
    targets = (
        ("claude", claude, claude / "commands", COMMAND_PATHS),
        ("codex", codex, codex, SYNC_PATHS),
        ("hermes", hermes, hermes, SYNC_PATHS),
    )
    return tuple(target for target in targets if target[0] in selected_hosts)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect(repo: Path, home: Path, selected_hosts: tuple[str, ...]) -> dict[str, object]:
    """Inventory source and installed bytes without changing either tree."""
    source_hashes: dict[str, str] = {}
    source_errors: list[str] = []
    for relative in SYNC_PATHS:
        source = repo / relative
        if not source.is_file() or source.is_symlink():
            source_errors.append(f"Missing or unsafe repository source: {source}")
        else:
            source_hashes[relative] = file_sha256(source)

    hosts: list[dict[str, str]] = []
    files: list[dict[str, str | None]] = []
    for host, root, required, relatives in build_targets(home, selected_hosts):
        if not required.is_dir():
            hosts.append({
                "host": host,
                "status": "missing-root",
                "required_directory": str(required),
            })
            continue
        hosts.append({"host": host, "status": "ready", "required_directory": str(required)})
        resolved_root = root.resolve()
        for relative in relatives:
            destination = root / relative
            record: dict[str, str | None] = {
                "host": host,
                "relative_path": relative,
                "destination": str(destination),
                "source_sha256": source_hashes.get(relative),
                "installed_sha256": None,
            }
            if relative not in source_hashes:
                record["status"] = "blocked"
                record["reason"] = "repository source is unavailable"
            elif not destination.resolve().is_relative_to(resolved_root):
                record["status"] = "blocked"
                record["reason"] = "destination escapes the installed root"
            elif destination.is_symlink() or (destination.exists() and not destination.is_file()):
                record["status"] = "blocked"
                record["reason"] = "destination is a symlink or is not a regular file"
            elif not destination.exists():
                record["status"] = "missing"
            else:
                record["installed_sha256"] = file_sha256(destination)
                record["status"] = (
                    "matched" if record["installed_sha256"] == record["source_sha256"] else "different"
                )
            files.append(record)

    counts = {status: sum(record["status"] == status for record in files)
              for status in ("matched", "missing", "different", "blocked")}
    counts["missing_roots"] = sum(host["status"] == "missing-root" for host in hosts)
    counts["source_errors"] = len(source_errors)
    return {"home": str(home), "selected_hosts": list(selected_hosts), "hosts": hosts, "files": files,
            "source_errors": source_errors, "summary": counts}


def copy_file(source: Path, destination: Path, root: Path, expected_sha256: str) -> None:
    """Atomically replace one adapter after checking its source and destination."""
    content = source.read_bytes()
    if hashlib.sha256(content).hexdigest() != expected_sha256:
        raise RuntimeError(f"Repository source changed during sync: {source}")
    if destination.is_symlink() or not destination.resolve().is_relative_to(root.resolve()):
        raise RuntimeError(f"Destination became unsafe during sync: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_handle, temporary_name = tempfile.mkstemp(prefix=".magos-sync-", dir=destination.parent)
    try:
        with os.fdopen(file_handle, "wb") as stream:
            stream.write(content)
        os.replace(temporary_name, destination)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def render(report: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print(f"MAGOS adapter {report['mode']}: {report['home']}")
    for error in report["source_errors"]:
        print(f"SOURCE ERROR {error}")
    for host in report["hosts"]:
        print(f"{host['host']}: {host['status']} ({host['required_directory']})")
    for item in report["files"]:
        source_hash = item["source_sha256"] or "-"
        installed_hash = item["installed_sha256"] or "-"
        print(f"  {item['host']} {item['status']} {item['relative_path']} "
              f"source={source_hash} installed={installed_hash}")
        if item.get("reason"):
            print(f"    {item['reason']}")
    if report.get("written"):
        print(f"Written: {len(report['written'])}")
    if report.get("error"):
        print(f"ERROR {report['error']}")
    print(f"Summary: {report['summary']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home(),
                        help="User home containing existing .claude, .codex and .hermes installs")
    parser.add_argument("--host", choices=("claude", "codex", "hermes"), action="append",
                        help="Limit inspection or synchronization to this host; repeat to select multiple hosts")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--verify", action="store_true", help="Exit nonzero if any adapter differs")
    mode.add_argument("--apply", action="store_true", help="Copy missing or different adapters")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable report")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    home = args.home.expanduser().resolve()
    selected_hosts = tuple(args.host or ("claude", "codex", "hermes"))
    report = inspect(repo, home, selected_hosts)
    report["mode"] = "apply" if args.apply else "verify" if args.verify else "plan"
    counts = report["summary"]
    if counts["missing_roots"] or counts["source_errors"] or counts["blocked"]:
        report["error"] = "Preflight failed; create the listed installed roots or fix blocked paths. No files were written."
        render(report, args.json)
        return 2

    if args.apply:
        roots = {host: root for host, root, _, _ in build_targets(home, selected_hosts)}
        written: list[str] = []
        try:
            for item in report["files"]:
                if item["status"] not in ("missing", "different"):
                    continue
                relative = item["relative_path"]
                copy_file(repo / relative, Path(item["destination"]), roots[item["host"]],
                          item["source_sha256"])
                written.append(f"{item['host']}:{relative}")
        except (OSError, RuntimeError) as exc:
            report["written"] = written
            report["error"] = f"Sync stopped after a write error: {exc}. Rerun --verify or --apply."
            render(report, args.json)
            return 2
        report = inspect(repo, home, selected_hosts)
        report["mode"] = "apply"
        report["written"] = written
        if any(report["summary"][status] for status in
               ("missing", "different", "blocked", "missing_roots", "source_errors")):
            report["error"] = "Some adapters did not match after writing."
            render(report, args.json)
            return 2

    render(report, args.json)
    if args.verify and (counts["missing"] or counts["different"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
