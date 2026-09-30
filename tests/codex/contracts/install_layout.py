"""Install the Codex and Hermes packages into a temporary home and verify the installed layout.

The discovery checks are replicas of the host rules, not the hosts themselves:
- Codex: codex-rs/ext/skills/src/loader (recursive scan, MAX_SCAN_DEPTH = 6, hidden directories skipped).
- Hermes: agent/skill_utils.py (rglob; a SKILL.md below a parent skill's support directory is not a skill).
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_SKILLS = {"multi-agent-git-orchestrator", "git-recon", "git-analyze", "git-recommend",
                   "git-integrate", "git-cleanup"}
CODEX_MAX_SCAN_DEPTH = 6
HERMES_SUPPORT_DIRS = {"references", "templates", "assets", "scripts"}
HERMES_SKIP_PARTS = {".git", ".github", ".hub", ".archive", ".locks"}
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
ADAPTER_REFERENCE = re.compile(r"`((?:\.\./)+[A-Za-z0-9_./-]+\.(?:md|yaml))`")
ROOT_REFERENCE = re.compile(r"`(references/[A-Za-z0-9_.-]+\.md)`")


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    block = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fields = {}
    if block:
        for key in ("name", "description"):
            match = re.search(rf"^{key}:\s*(.+?)\s*$", block.group(1), re.M)
            if match:
                fields[key] = match.group(1).strip().strip('"')
    return fields


def codex_discovery(skills_root: Path) -> list[str]:
    names = []
    for path in skills_root.rglob("SKILL.md"):
        parts = path.relative_to(skills_root).parts
        if any(part.startswith(".") for part in parts[:-1]) or len(parts) - 1 > CODEX_MAX_SCAN_DEPTH:
            continue
        names.append(frontmatter(path).get("name") or path.parent.name)
    return names


def hermes_discovery(skills_root: Path) -> list[str]:
    names = []
    for path in skills_root.rglob("SKILL.md"):
        parts = path.relative_to(skills_root).parts
        if any(part in HERMES_SKIP_PARTS for part in parts):
            continue
        if any(part in HERMES_SUPPORT_DIRS and (skills_root.joinpath(*parts[:index]) / "SKILL.md").exists()
               for index, part in enumerate(parts[:-1])):
            continue
        names.append(frontmatter(path).get("name") or path.parent.name)
    return names


def check_package(host: str, package_root: Path, skills_root: Path, discover) -> list[dict]:
    results = []
    missing = []
    commands_links = []
    for adapter in sorted(package_root.glob("skills/*/SKILL.md")):
        text = adapter.read_text(encoding="utf-8")
        label = adapter.relative_to(package_root).as_posix()
        for reference in ADAPTER_REFERENCE.findall(text):
            if reference.startswith("../../commands/"):
                commands_links.append(f"{label} -> {reference}")
            elif not (adapter.parent / reference).resolve().is_file():
                missing.append(f"{label} -> {reference}")
    root_skill = package_root / "SKILL.md"
    if not root_skill.is_file():
        missing.append("SKILL.md")
    else:
        for reference in ROOT_REFERENCE.findall(root_skill.read_text(encoding="utf-8")):
            if not (package_root / reference).is_file():
                missing.append(f"SKILL.md -> {reference}")
    results.append({"file": f"install:{host} relative references resolve", "passed": not missing,
                    "missing": missing})
    results.append({"file": f"install:{host} adapters do not route through commands/",
                    "passed": not commands_links, "missing": commands_links})

    policy_missing = [path.relative_to(package_root).as_posix()
                      for path in sorted(package_root.glob("skills/*/agents/openai.yaml"))
                      if not re.search(r"^policy:\n  allow_implicit_invocation: false$",
                                       path.read_text(encoding="utf-8"), re.M)]
    if len(list(package_root.glob("skills/*/agents/openai.yaml"))) != 5:
        policy_missing.append("expected 5 agents/openai.yaml files")
    results.append({"file": f"install:{host} adapters disable implicit invocation",
                    "passed": not policy_missing, "missing": policy_missing})

    names = discover(skills_root)
    problems = []
    if sorted(names) != sorted(EXPECTED_SKILLS):
        problems.append(f"discovered {sorted(names)}; expected {sorted(EXPECTED_SKILLS)}")
    for skill_file in [root_skill, *package_root.glob("skills/*/SKILL.md")]:
        fields = frontmatter(skill_file) if skill_file.is_file() else {}
        if not 0 < len(fields.get("name", "")) <= MAX_NAME_LENGTH:
            problems.append(f"{skill_file.relative_to(package_root).as_posix()}: invalid name")
        if not 0 < len(fields.get("description", "")) <= MAX_DESCRIPTION_LENGTH:
            problems.append(f"{skill_file.relative_to(package_root).as_posix()}: invalid description length")
    results.append({"file": f"install:{host} discovery replica finds each skill once",
                    "passed": not problems, "missing": problems})
    return results


def check(repo: Path) -> list[dict]:
    with tempfile.TemporaryDirectory(prefix="magos-layout-") as temporary:
        home = Path(temporary)
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", str(repo / "scripts" / "sync_hosts.py"), "--home", str(home),
             "--host", "codex", "--host", "hermes", "--apply", "--create-roots", "--json"],
            text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=120, check=False)
        results = [{"file": "install:sync_hosts.py --apply --create-roots", "passed": completed.returncode == 0,
                    "missing": [] if completed.returncode == 0 else [completed.stdout[-400:] + completed.stderr[-400:]]}]
        if completed.returncode:
            return results
        report = json.loads(completed.stdout)
        roots = {host["host"]: Path(host["required_directory"]) for host in report["hosts"]}
        outside = [f"{host}: install root is outside the temporary home" for host, root in roots.items()
                   if not root.resolve().is_relative_to(home.resolve())]
        results.append({"file": "install:roots stay inside the temporary home", "passed": not outside,
                        "missing": outside})
        if outside:
            return results
        results += check_package("codex", roots["codex"], roots["codex"].parent, codex_discovery)
        results += check_package("hermes", roots["hermes"], roots["hermes"].parent, hermes_discovery)
        return results
