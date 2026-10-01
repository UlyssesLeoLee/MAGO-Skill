# ```cypher
# CREATE
#   (file:File {name: "gitlab.py", type: "file", language: "python"}),
#   (v_FIXED_DATE:Variable {name: "FIXED_DATE", type: "variable"}),
#   (v_GIT_ENV:Variable {name: "GIT_ENV", type: "variable"}),
#   (v_TRACE:Variable {name: "TRACE", type: "variable"}),
#   (f_git:Function {name: "git", type: "function", signature: "git(cwd: Path | str, *args: str, check: bool=False) -> subprocess.CompletedProcess"}),
#   (f_out:Function {name: "out", type: "function", signature: "out(cwd: Path | str, *args: str) -> str"}),
#   (f_init_repo:Function {name: "init_repo", type: "function", signature: "init_repo(path: Path, branch: str='main') -> Path"}),
#   (f_commit:Function {name: "commit", type: "function", signature: "commit(repo: Path | str, name: str, text: str, message: str, append: bool=False) -> str"}),
#   (f_branch:Function {name: "branch", type: "function", signature: "branch(repo: Path | str, name: str, base: str='HEAD') -> None"}),
#   (f_refs:Function {name: "refs", type: "function", signature: "refs(repo: Path | str) -> dict[str, str]"}),
#   (f_worktrees:Function {name: "worktrees", type: "function", signature: "worktrees(repo: Path | str) -> list[dict]"}),
#   (f_same_path:Function {name: "same_path", type: "function", signature: "same_path(left: Path | str, right: Path | str) -> bool"}),
#   (f_is_ancestor:Function {name: "is_ancestor", type: "function", signature: "is_ancestor(repo: Path | str, ancestor: str, descendant: str) -> bool"}),
#   (f_git_paths:Function {name: "git_paths", type: "function", signature: "git_paths(worktree: Path | str, names: tuple[str, ...]) -> dict[str, Path]"}),
#   (f_init_bare:Function {name: "init_bare", type: "function", signature: "init_bare(path: Path) -> Path"}),
#   (f_untraced:Function {name: "untraced", type: "function", signature: "untraced() -> Iterator[None]"}),
#   (f_force_remove:Function {name: "force_remove", type: "function", signature: "force_remove(function, path, _error) -> None"}),
#   (f_rmtree:Function {name: "rmtree", type: "function", signature: "rmtree(path: Path | str) -> None"}),
#   (f_fixture_root:Function {name: "fixture_root", type: "function", signature: "fixture_root(base: Path | str | None=None) -> Iterator[Path]"}),
#   (file)-[:CONTAINS]->(v_FIXED_DATE),
#   (file)-[:CONTAINS]->(v_GIT_ENV),
#   (file)-[:CONTAINS]->(v_TRACE),
#   (file)-[:CONTAINS]->(f_git),
#   (file)-[:CONTAINS]->(f_out),
#   (file)-[:CONTAINS]->(f_init_repo),
#   (file)-[:CONTAINS]->(f_commit),
#   (file)-[:CONTAINS]->(f_branch),
#   (file)-[:CONTAINS]->(f_refs),
#   (file)-[:CONTAINS]->(f_worktrees),
#   (file)-[:CONTAINS]->(f_same_path),
#   (file)-[:CONTAINS]->(f_is_ancestor),
#   (file)-[:CONTAINS]->(f_git_paths),
#   (file)-[:CONTAINS]->(f_init_bare),
#   (file)-[:CONTAINS]->(f_untraced),
#   (file)-[:CONTAINS]->(f_force_remove),
#   (file)-[:CONTAINS]->(f_rmtree),
#   (file)-[:CONTAINS]->(f_fixture_root),
#   (f_branch)-[:CALLS]->(f_git),
#   (f_commit)-[:CALLS]->(f_git),
#   (f_commit)-[:CALLS]->(f_out),
#   (f_fixture_root)-[:CALLS]->(f_rmtree),
#   (f_git)-[:USES]->(v_GIT_ENV),
#   (f_git)-[:USES]->(v_TRACE),
#   (f_git_paths)-[:CALLS]->(f_out),
#   (f_init_bare)-[:CALLS]->(f_git),
#   (f_init_bare)-[:USES]->(v_GIT_ENV),
#   (f_init_repo)-[:CALLS]->(f_commit),
#   (f_init_repo)-[:CALLS]->(f_git),
#   (f_init_repo)-[:USES]->(v_GIT_ENV),
#   (f_is_ancestor)-[:CALLS]->(f_git),
#   (f_out)-[:CALLS]->(f_git),
#   (f_refs)-[:CALLS]->(f_out),
#   (f_untraced)-[:USES]->(v_TRACE),
#   (f_worktrees)-[:CALLS]->(f_out);
# ```
"""Shared git helpers for the GitConverge tests: run git, build disposable repositories, read refs and worktrees.

Every function targets a repository the caller created under a fixture root. Nothing here touches the MAGOS checkout.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from typing import Iterator


FIXED_DATE = "2026-01-01T00:00:00+00:00"
GIT_ENV = {**os.environ, "LC_ALL": "C", "LANG": "C", "GIT_TERMINAL_PROMPT": "0", "GIT_EDITOR": "true",
           "GIT_MERGE_AUTOEDIT": "no", "GIT_AUTHOR_NAME": "magos-test", "GIT_AUTHOR_EMAIL": "magos-test@example.invalid",
           "GIT_COMMITTER_NAME": "magos-test", "GIT_COMMITTER_EMAIL": "magos-test@example.invalid",
           "GIT_AUTHOR_DATE": FIXED_DATE, "GIT_COMMITTER_DATE": FIXED_DATE}


TRACE: list[list[str]] | None = None


def git(cwd: Path | str, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    """Run `git -C <cwd> <args>` with a stable English locale; raise only when check=True. Records args in TRACE."""
    if TRACE is not None:
        TRACE.append(list(args))
    proc = subprocess.run(["git", "-C", str(cwd), *args], text=True, encoding="utf-8", errors="replace",
                          capture_output=True, env=GIT_ENV, timeout=120, check=False)
    if check and proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed in {cwd} (rc={proc.returncode}): {proc.stderr.strip()}")
    return proc


def out(cwd: Path | str, *args: str) -> str:
    """Stripped stdout of a git command that must succeed."""
    return git(cwd, *args, check=True).stdout.strip()


def init_repo(path: Path, branch: str = "main") -> Path:
    """Create a repository with one base commit and deterministic local config."""
    path.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", branch, str(path)], check=True, env=GIT_ENV, capture_output=True)
    for key, value in (("user.name", "magos-test"), ("user.email", "magos-test@example.invalid"),
                       ("core.autocrlf", "false"), ("commit.gpgsign", "false"), ("core.longpaths", "true")):
        git(path, "config", key, value, check=True)
    commit(path, "README.md", "base\n", "base")
    return path


def commit(repo: Path | str, name: str, text: str, message: str, append: bool = False) -> str:
    """Write `text` to `name`, commit only that path, and return the new commit SHA."""
    target = Path(repo) / name
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "a" if append else "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    git(repo, "add", "-f", "--", name, check=True)
    git(repo, "commit", "-q", "-m", message, "--", name, check=True)
    return out(repo, "rev-parse", "HEAD")


def branch(repo: Path | str, name: str, base: str = "HEAD") -> None:
    """Create a branch at `base` without switching to it."""
    git(repo, "branch", name, base, check=True)


def refs(repo: Path | str) -> dict[str, str]:
    """Local branch name -> commit SHA, read with an exact full-refname listing."""
    listing = out(repo, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads")
    return {line.split(" ")[0].removeprefix("refs/heads/"): line.split(" ")[1] for line in listing.splitlines()}


def worktrees(repo: Path | str) -> list[dict]:
    """Parse `git worktree list --porcelain` into dicts with path, head, branch, detached, locked, prunable."""
    items: list[dict] = []
    current: dict | None = None
    for line in [*out(repo, "worktree", "list", "--porcelain").splitlines(), ""]:
        if not line:
            if current:
                items.append(current)
            current = None
            continue
        key, _, value = line.partition(" ")
        if key == "worktree":
            current = {"path": value, "head": None, "branch": None, "detached": False, "locked": None,
                       "prunable": None, "bare": False}
        elif current is not None:
            if key == "HEAD":
                current["head"] = value
            elif key == "branch":
                current["branch"] = value.removeprefix("refs/heads/")
            elif key == "detached":
                current["detached"] = True
            elif key == "locked":
                current["locked"] = value or True
            elif key == "prunable":
                current["prunable"] = value or True
            elif key == "bare":
                current["bare"] = True
    return items


def same_path(left: Path | str, right: Path | str) -> bool:
    """Path equality that ignores slash style and case rules of the platform."""
    return os.path.normcase(os.path.realpath(str(left))) == os.path.normcase(os.path.realpath(str(right)))


def is_ancestor(repo: Path | str, ancestor: str, descendant: str) -> bool:
    """True when `ancestor` is reachable from `descendant`; any other Git error raises instead of reading as False."""
    proc = git(repo, "merge-base", "--is-ancestor", ancestor, descendant)
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"merge-base --is-ancestor {ancestor} {descendant} failed in {repo}: {proc.stderr.strip()}")
    return proc.returncode == 0


def git_paths(worktree: Path | str, names: tuple[str, ...]) -> dict[str, Path]:
    """Absolute locations of per-worktree Git files, resolved with one `rev-parse --git-path ...` call."""
    args = [item for name in names for item in ("--git-path", name)]
    lines = out(worktree, "rev-parse", *args).splitlines()
    located = {}
    for name, line in zip(names, lines):
        candidate = Path(line)
        located[name] = candidate if candidate.is_absolute() else Path(worktree) / candidate
    return located


def init_bare(path: Path) -> Path:
    """A bare repository with long-path support (receive-pack quarantine paths exceed MAX_PATH on Windows)."""
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(path)], check=True, env=GIT_ENV, capture_output=True)
    git(path, "config", "core.longpaths", "true", check=True)
    return path


@contextmanager
def untraced() -> Iterator[None]:
    """Suspend TRACE so harness-side git calls (test hooks, validators) are not attributed to the executor."""
    global TRACE
    saved, TRACE = TRACE, None
    try:
        yield
    finally:
        TRACE = saved


def force_remove(function, path, _error) -> None:
    """rmtree error hook: clear the read-only bit Git sets on object files, then retry."""
    os.chmod(path, stat.S_IWRITE)
    function(path)


def rmtree(path: Path | str) -> None:
    """Delete a fixture tree, including read-only Git objects on Windows."""
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=force_remove)
    else:
        shutil.rmtree(path, onerror=force_remove)


@contextmanager
def fixture_root(base: Path | str | None = None) -> Iterator[Path]:
    """A throwaway directory that is removed afterwards; `base` keeps paths short on Windows."""
    if base is not None:
        Path(base).mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="mgc-", dir=str(base) if base else None))
    try:
        yield root
    finally:
        rmtree(root)
