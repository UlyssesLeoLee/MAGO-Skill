# ```cypher
# CREATE
#   (file:File {name: "git_behavior_probes.py", type: "file", language: "python"}),
#   (v_RESULTS_DIR:Variable {name: "RESULTS_DIR", type: "variable"}),
#   (v_PROBES:Variable {name: "PROBES", type: "variable"}),
#   (f_probe_upstream_behind:Function {name: "probe_upstream_behind", type: "function", signature: "probe_upstream_behind(root: Path) -> dict"}),
#   (f_probe_upstream_read:Function {name: "probe_upstream_read", type: "function", signature: "probe_upstream_read(root: Path) -> dict"}),
#   (f_probe_worktree_remove:Function {name: "probe_worktree_remove", type: "function", signature: "probe_worktree_remove(root: Path) -> dict"}),
#   (f_probe_prune_scope:Function {name: "probe_prune_scope", type: "function", signature: "probe_prune_scope(root: Path) -> dict"}),
#   (f_probe_merge_mechanics:Function {name: "probe_merge_mechanics", type: "function", signature: "probe_merge_mechanics(root: Path) -> dict"}),
#   (f_probe_ignored_overwrite:Function {name: "probe_ignored_overwrite", type: "function", signature: "probe_ignored_overwrite(root: Path) -> dict"}),
#   (f_probe_tag_shadow:Function {name: "probe_tag_shadow", type: "function", signature: "probe_tag_shadow(root: Path) -> dict"}),
#   (f_probe_case_refs:Function {name: "probe_case_refs", type: "function", signature: "probe_case_refs(root: Path) -> dict"}),
#   (f_probe_rebase_in_progress:Function {name: "probe_rebase_in_progress", type: "function", signature: "probe_rebase_in_progress(root: Path) -> dict"}),
#   (f_probe_untracked_hidden:Function {name: "probe_untracked_hidden", type: "function", signature: "probe_untracked_hidden(root: Path) -> dict"}),
#   (f_probe_merge_tree:Function {name: "probe_merge_tree", type: "function", signature: "probe_merge_tree(root: Path) -> dict"}),
#   (f_probe_worktree_flags:Function {name: "probe_worktree_flags", type: "function", signature: "probe_worktree_flags(root: Path) -> dict"}),
#   (f_probe_remove_current:Function {name: "probe_remove_current", type: "function", signature: "probe_remove_current(root: Path) -> dict"}),
#   (f_probe_sequencer_paused:Function {name: "probe_sequencer_paused", type: "function", signature: "probe_sequencer_paused(root: Path) -> dict"}),
#   (f_probe_skip_worktree_hidden:Function {name: "probe_skip_worktree_hidden", type: "function", signature: "probe_skip_worktree_hidden(root: Path) -> dict"}),
#   (f_probe_target_tag_shadow:Function {name: "probe_target_tag_shadow", type: "function", signature: "probe_target_tag_shadow(root: Path) -> dict"}),
#   (f_label:Function {name: "label", type: "function", signature: "label(result: dict) -> str"}),
#   (f_tally:Function {name: "tally", type: "function", signature: "tally(results: list[dict]) -> tuple[int, int, int]"}),
#   (f_run_probe:Function {name: "run_probe", type: "function", signature: "run_probe(probe, base: str | None) -> dict"}),
#   (f_render:Function {name: "render", type: "function", signature: "render(results: list[dict], version: str) -> str"}),
#   (f_main:Function {name: "main", type: "function", signature: "main() -> int"}),
#   (file)-[:CONTAINS]->(v_RESULTS_DIR),
#   (file)-[:CONTAINS]->(v_PROBES),
#   (file)-[:CONTAINS]->(f_probe_upstream_behind),
#   (file)-[:CONTAINS]->(f_probe_upstream_read),
#   (file)-[:CONTAINS]->(f_probe_worktree_remove),
#   (file)-[:CONTAINS]->(f_probe_prune_scope),
#   (file)-[:CONTAINS]->(f_probe_merge_mechanics),
#   (file)-[:CONTAINS]->(f_probe_ignored_overwrite),
#   (file)-[:CONTAINS]->(f_probe_tag_shadow),
#   (file)-[:CONTAINS]->(f_probe_case_refs),
#   (file)-[:CONTAINS]->(f_probe_rebase_in_progress),
#   (file)-[:CONTAINS]->(f_probe_untracked_hidden),
#   (file)-[:CONTAINS]->(f_probe_merge_tree),
#   (file)-[:CONTAINS]->(f_probe_worktree_flags),
#   (file)-[:CONTAINS]->(f_probe_remove_current),
#   (file)-[:CONTAINS]->(f_probe_sequencer_paused),
#   (file)-[:CONTAINS]->(f_probe_skip_worktree_hidden),
#   (file)-[:CONTAINS]->(f_probe_target_tag_shadow),
#   (file)-[:CONTAINS]->(f_label),
#   (file)-[:CONTAINS]->(f_tally),
#   (file)-[:CONTAINS]->(f_run_probe),
#   (file)-[:CONTAINS]->(f_render),
#   (file)-[:CONTAINS]->(f_main),
#   (f_main)-[:CALLS]->(f_label),
#   (f_main)-[:CALLS]->(f_render),
#   (f_main)-[:CALLS]->(f_run_probe),
#   (f_main)-[:CALLS]->(f_tally),
#   (f_main)-[:USES]->(v_PROBES),
#   (f_main)-[:USES]->(v_RESULTS_DIR),
#   (f_render)-[:CALLS]->(f_label),
#   (f_render)-[:CALLS]->(f_tally),
#   (file)-[:CALLS]->(f_main);
# ```
"""Probe the Git behaviors the GitConverge contract relies on, against the installed Git.

Each probe builds a disposable repository, runs the exact Git commands the contract uses, and records what Git
did. A probe FAILS when Git does not behave as the contract assumes. Results go to tests/claude/results/git-probes/.
Run: python -X utf8 tests/claude/scripts/git_behavior_probes.py [--fixture-root <short path>]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gitlab  # noqa: E402
from gitlab import commit, git, init_repo, out  # noqa: E402

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results" / "git-probes"


def probe_upstream_behind(root: Path) -> dict:
    """`branch -d` judges an upstream-tracking branch against its upstream, so the contract unsets the upstream first."""
    bare = gitlab.init_bare(root / "origin.git")
    repo = init_repo(root / "repo")
    git(repo, "remote", "add", "origin", str(bare), check=True)
    git(repo, "push", "-q", "-u", "origin", "main", check=True)
    git(repo, "switch", "-qc", "target", check=True)
    git(repo, "switch", "-qc", "feat", "main", check=True)
    commit(repo, "f.txt", "1\n", "feat1")
    git(repo, "push", "-q", "-u", "origin", "feat", check=True)
    feat_sha = commit(repo, "f.txt", "2\n", "feat2")
    git(repo, "switch", "-q", "target", check=True)
    git(repo, "merge", "--no-ff", "--no-edit", feat_sha, check=True)
    contained = gitlab.is_ancestor(repo, feat_sha, "target")
    plain = git(repo, "branch", "-d", "feat")
    saved = out(repo, "rev-parse", "--symbolic-full-name", "feat@{upstream}")
    unset = git(repo, "branch", "--unset-upstream", "feat")
    after = git(repo, "branch", "-d", "feat")
    observed = {"contained_in_target": contained, "plain_d_rc": plain.returncode, "saved_upstream": saved,
                "unset_rc": unset.returncode, "d_after_unset_rc": after.returncode}
    passed = contained and plain.returncode != 0 and unset.returncode == 0 and after.returncode == 0
    return {"passed": passed, "observed": observed,
            "note": "plain -d refuses although the branch is contained in HEAD; --unset-upstream then -d succeeds"}


def probe_upstream_read(root: Path) -> dict:
    """The upstream is read with for-each-ref (a full-refname @{upstream} fails) and restored with --set-upstream-to."""
    bare = gitlab.init_bare(root / "origin.git")
    repo = init_repo(root / "repo")
    git(repo, "remote", "add", "origin", str(bare), check=True)
    git(repo, "push", "-q", "-u", "origin", "main", check=True)
    git(repo, "switch", "-qc", "feat", check=True)
    commit(repo, "f.txt", "f\n", "feat")
    git(repo, "push", "-q", "-u", "origin", "feat", check=True)
    git(repo, "branch", "plain", "main", check=True)
    fmt = "--format=%(upstream)|%(upstream:short)"
    full_form = git(repo, "rev-parse", "--symbolic-full-name", "refs/heads/feat@{upstream}")
    read = out(repo, "for-each-ref", fmt, "refs/heads/feat")
    none = out(repo, "for-each-ref", fmt, "refs/heads/plain")
    git(repo, "tag", "feat", "main", check=True)
    with_tag = out(repo, "for-each-ref", fmt, "refs/heads/feat")
    git(repo, "branch", "--unset-upstream", "feat", check=True)
    unset = out(repo, "for-each-ref", fmt, "refs/heads/feat")
    restore = git(repo, "branch", "--set-upstream-to=origin/feat", "feat")
    restored = out(repo, "for-each-ref", fmt, "refs/heads/feat")
    observed = {"full_refname_form_rc": full_form.returncode, "read": read, "no_upstream": none, "with_same_named_tag": with_tag,
                "after_unset": unset, "restore_rc": restore.returncode, "after_restore": restored}
    passed = (full_form.returncode != 0 and read == "refs/remotes/origin/feat|origin/feat" and none == "|"
              and with_tag == read and unset == "|" and restore.returncode == 0 and restored == read)
    return {"passed": passed, "observed": observed,
            "note": "the contract records `%(upstream)|%(upstream:short)` and restores with the short name"}


def probe_worktree_remove(root: Path) -> dict:
    """`worktree remove` refuses dirty, untracked-only and locked worktrees but silently deletes ignored files."""
    repo = init_repo(root / "repo")
    commit(repo, ".gitignore", "*.log\n", "ignore logs")
    for name in ("clean", "dirty", "untracked", "locked", "ignored"):
        gitlab.branch(repo, name)
        git(repo, "worktree", "add", "-q", str(root / f"wt-{name}"), name, check=True)
    (root / "wt-dirty" / "README.md").write_text("changed\n", encoding="utf-8")
    (root / "wt-untracked" / "new.txt").write_text("u\n", encoding="utf-8")
    (root / "wt-ignored" / "keep.log").write_text("precious\n", encoding="utf-8")
    git(repo, "worktree", "lock", "--reason", "agent busy", str(root / "wt-locked"), check=True)
    rc = {name: git(repo, "worktree", "remove", str(root / f"wt-{name}")).returncode
          for name in ("clean", "dirty", "untracked", "locked", "ignored")}
    main_rc = git(repo, "worktree", "remove", str(repo)).returncode
    status_ignored = out(root / "wt-dirty", "status", "--porcelain=v1")
    observed = {"remove_rc": rc, "remove_main_rc": main_rc, "dirty_status": status_ignored,
                "ignored_dir_exists_after": (root / "wt-ignored").exists()}
    passed = (rc["clean"] == 0 and rc["dirty"] != 0 and rc["untracked"] != 0 and rc["locked"] != 0
              and rc["ignored"] == 0 and not observed["ignored_dir_exists_after"] and main_rc != 0)
    return {"passed": passed, "observed": observed,
            "note": "ignored files are deleted with rc=0, so the contract must gate them itself"}


def probe_prune_scope(root: Path) -> dict:
    """`worktree prune` is repository-wide; `worktree remove <path>` on a missing directory touches one entry."""
    repo = init_repo(root / "repo")
    gitlab.branch(repo, "feat")
    git(repo, "worktree", "add", "-q", "--detach", str(root / "det"), "main", check=True)
    detached_sha = commit(root / "det", "det.txt", "only here\n", "detached work")
    git(repo, "worktree", "add", "-q", str(root / "wfeat"), "feat", check=True)
    gitlab.rmtree(root / "det")
    gitlab.rmtree(root / "wfeat")
    before = [(Path(item["path"]).name, bool(item["prunable"])) for item in gitlab.worktrees(repo)]
    blocked = git(repo, "branch", "-d", "feat")
    remove = git(repo, "worktree", "remove", str(root / "wfeat"))
    detached_still_listed = any(item["head"] == detached_sha for item in gitlab.worktrees(repo))
    delete = git(repo, "branch", "-d", "feat")
    git(repo, "worktree", "prune")
    reachable = out(repo, "branch", "-a", "--contains", detached_sha)
    observed = {"listed_before": before, "branch_d_while_entry_exists_rc": blocked.returncode,
                "scoped_remove_rc": remove.returncode, "detached_still_listed_after_scoped_remove": detached_still_listed,
                "branch_d_after_scoped_remove_rc": delete.returncode,
                "detached_commit_reachable_after_global_prune": bool(reachable)}
    passed = (blocked.returncode != 0 and remove.returncode == 0 and detached_still_listed
              and delete.returncode == 0 and not reachable)
    return {"passed": passed, "observed": observed,
            "note": "global prune orphans commits held only by a detached worktree; scoped remove does not"}


def probe_merge_mechanics(root: Path) -> dict:
    """--no-ff always records a merge; a conflict aborts cleanly; unrelated histories are refused, not merged."""
    repo = init_repo(root / "repo")
    gitlab.branch(repo, "target")
    main_sha = commit(repo, "m.txt", "m\n", "main work")
    git(repo, "switch", "-qc", "c1", "target", check=True)
    commit(repo, "README.md", "one\n", "c1")
    git(repo, "switch", "-qc", "c2", "target", check=True)
    commit(repo, "README.md", "two\n", "c2")
    git(repo, "switch", "-q", "target", check=True)
    merge_main = git(repo, "merge", "--no-ff", "--no-edit", main_sha)
    parents = len(out(repo, "rev-list", "--parents", "-n", "1", "HEAD").split()) - 1
    merge_c1 = git(repo, "merge", "--no-ff", "--no-edit", "c1")
    before_conflict = out(repo, "rev-parse", "HEAD")
    merge_c2 = git(repo, "merge", "--no-ff", "--no-edit", "c2")
    merge_head = out(repo, "rev-parse", "-q", "--verify", "MERGE_HEAD") if merge_c2.returncode else ""
    abort = git(repo, "merge", "--abort")
    restored = out(repo, "rev-parse", "HEAD") == before_conflict
    git(repo, "switch", "-q", "--orphan", "orphan", check=True)
    commit(repo, "site.txt", "site\n", "orphan root")
    git(repo, "switch", "-q", "target", check=True)
    unrelated_base = git(repo, "merge-base", "refs/heads/target", "refs/heads/orphan")
    unrelated_merge = git(repo, "merge", "--no-ff", "--no-edit", "refs/heads/orphan")
    observed = {"merge_main_rc": merge_main.returncode, "merge_commit_parents": parents,
                "merge_c1_rc": merge_c1.returncode, "conflict_rc": merge_c2.returncode,
                "merge_head_present": bool(merge_head), "abort_rc": abort.returncode, "head_restored": restored,
                "unrelated_merge_base_rc": unrelated_base.returncode, "unrelated_merge_rc": unrelated_merge.returncode,
                "unrelated_message": unrelated_merge.stderr.strip()}
    passed = (merge_main.returncode == 0 and parents == 2 and merge_c1.returncode == 0 and merge_c2.returncode == 1
              and bool(merge_head) and abort.returncode == 0 and restored and unrelated_base.returncode == 1
              and unrelated_merge.returncode != 0 and "unrelated histories" in unrelated_merge.stderr)
    return {"passed": passed, "observed": observed, "note": "target that is an ancestor of main still gets a merge commit"}


def probe_ignored_overwrite(root: Path) -> dict:
    """A merge overwrites an ignored local file silently; `switch --no-overwrite-ignore` refuses; status hides it."""
    repo = init_repo(root / "repo")
    commit(repo, ".gitignore", ".env\n", "ignore env")
    gitlab.branch(repo, "target")
    git(repo, "switch", "-qc", "src", "main", check=True)
    commit(repo, ".env", "FROM_SRC\n", "force-add env")
    git(repo, "switch", "-q", "target", check=True)
    (repo / ".env").write_text("LOCAL_SECRET\n", encoding="utf-8")
    status = out(repo, "status", "--porcelain=v1", "--untracked-files=all")
    guarded = git(repo, "switch", "--no-overwrite-ignore", "src")
    base = out(repo, "merge-base", "refs/heads/target", "refs/heads/src")
    overlap = set(out(repo, "diff", "--name-only", base, "refs/heads/src").splitlines()) & \
        set(out(repo, "ls-files", "--others", "--ignored", "--exclude-standard").splitlines())
    merge = git(repo, "merge", "--no-ff", "--no-edit", "src")
    content = (repo / ".env").read_text(encoding="utf-8").strip()
    observed = {"status_shows_ignored": bool(status), "switch_no_overwrite_rc": guarded.returncode,
                "overlap_before_merge": sorted(overlap), "merge_rc": merge.returncode, "env_after_merge": content}
    passed = (not status and guarded.returncode != 0 and overlap == {".env"} and merge.returncode == 0
              and content == "FROM_SRC")
    return {"passed": passed, "observed": observed,
            "note": "'clean' cannot see ignored files, so the contract compares source paths with ignored files itself"}


def probe_tag_shadow(root: Path) -> dict:
    """A tag named like a branch wins a bare-name lookup, so the contract uses refs/heads/<name> and SHAs."""
    repo = init_repo(root / "repo")
    git(repo, "switch", "-qc", "feat", check=True)
    branch_sha = commit(repo, "f.txt", "f\n", "on branch")
    git(repo, "switch", "-q", "main", check=True)
    git(repo, "tag", "feat", "main")
    bare = git(repo, "rev-parse", "feat")
    full = out(repo, "rev-parse", "--verify", "refs/heads/feat")
    observed = {"bare_name_sha": bare.stdout.strip(), "branch_sha": full, "warning": bare.stderr.strip()[:120]}
    return {"passed": bare.stdout.strip() != branch_sha and full == branch_sha, "observed": observed,
            "note": "bare name resolves to the tag; refs/heads/feat resolves to the branch"}


def probe_case_refs(root: Path) -> dict:
    """On case-insensitive filesystems a differently-cased name may resolve; the exact listing never lists it."""
    repo = init_repo(root / "repo")
    gitlab.branch(repo, "target")
    resolves = git(repo, "rev-parse", "--verify", "-q", "refs/heads/Target").returncode == 0
    exact = "Target" in gitlab.refs(repo)
    observed = {"case_variant_resolves": resolves, "case_variant_in_exact_listing": exact}
    return {"passed": not exact, "observed": observed,
            "note": "match <branch> against the exact for-each-ref listing; a rev-parse success proves nothing"}


def probe_rebase_in_progress(root: Path) -> dict:
    """A branch mid-rebase shows as a detached worktree; its name lives in rebase-merge/head-name."""
    repo = init_repo(root / "repo")
    commit(repo, "a.txt", "base\n", "a")
    gitlab.branch(repo, "topic")
    commit(repo, "a.txt", "main side\n", "main edit")
    git(repo, "worktree", "add", "-q", str(root / "wt-topic"), "topic", check=True)
    commit(root / "wt-topic", "a.txt", "topic side\n", "topic edit")
    rebase = git(root / "wt-topic", "rebase", "main")
    entry = next(item for item in gitlab.worktrees(repo) if gitlab.same_path(item["path"], root / "wt-topic"))
    head_name_path = gitlab.git_paths(root / "wt-topic", ("rebase-merge/head-name",))["rebase-merge/head-name"]
    head_name = head_name_path.read_text(encoding="utf-8").strip() if head_name_path.exists() else ""
    in_refs = "topic" in gitlab.refs(repo)
    delete = git(repo, "branch", "-d", "topic")
    observed = {"rebase_rc": rebase.returncode, "worktree_detached": entry["detached"], "worktree_branch": entry["branch"],
                "head_name": head_name, "branch_still_listed": in_refs, "branch_d_rc": delete.returncode}
    passed = rebase.returncode != 0 and entry["detached"] and head_name == "refs/heads/topic" and in_refs \
        and delete.returncode != 0
    return {"passed": passed, "observed": observed,
            "note": "the worktree list shows no branch; only rebase-merge/head-name maps the rebase back to topic"}


def probe_untracked_hidden(root: Path) -> dict:
    """status.showUntrackedFiles=no hides untracked files from plain status; --untracked-files=all still shows them."""
    repo = init_repo(root / "repo")
    git(repo, "config", "status.showUntrackedFiles", "no", check=True)
    (repo / "stray.txt").write_text("x\n", encoding="utf-8")
    plain = out(repo, "status", "--porcelain=v1")
    explicit = out(repo, "status", "--porcelain=v1", "--untracked-files=all")
    observed = {"plain": plain, "explicit": explicit}
    return {"passed": plain == "" and explicit.startswith("??"), "observed": observed,
            "note": "the contract always passes --untracked-files=all when it tests for a clean workspace"}


def probe_merge_tree(root: Path) -> dict:
    """`merge-tree --write-tree` predicts conflicts (rc 1) and leaves refs, index and worktree untouched."""
    repo = init_repo(root / "repo")
    gitlab.branch(repo, "target")
    git(repo, "switch", "-qc", "clean", "target", check=True)
    commit(repo, "new.txt", "n\n", "clean")
    git(repo, "switch", "-qc", "clash", "target", check=True)
    commit(repo, "README.md", "a\n", "clash a")
    git(repo, "switch", "-q", "target", check=True)
    commit(repo, "README.md", "b\n", "target edit")
    before = (gitlab.refs(repo), out(repo, "status", "--porcelain=v1"))
    clean = git(repo, "merge-tree", "--write-tree", "--no-messages", "refs/heads/target", "refs/heads/clean")
    clash = git(repo, "merge-tree", "--write-tree", "--no-messages", "refs/heads/target", "refs/heads/clash")
    after = (gitlab.refs(repo), out(repo, "status", "--porcelain=v1"))
    observed = {"clean_rc": clean.returncode, "clash_rc": clash.returncode, "state_unchanged": before == after}
    return {"passed": clean.returncode == 0 and clash.returncode == 1 and before == after, "observed": observed,
            "note": "needs Git >= 2.38; the preview treats it as best-effort prediction"}


def probe_worktree_flags(root: Path) -> dict:
    """Porcelain reports detached, locked (with reason) and prunable (missing directory) entries."""
    repo = init_repo(root / "repo")
    gitlab.branch(repo, "a")
    gitlab.branch(repo, "b")
    git(repo, "worktree", "add", "-q", "--detach", str(root / "det"), check=True)
    git(repo, "worktree", "add", "-q", str(root / "wa"), "a", check=True)
    git(repo, "worktree", "add", "-q", str(root / "wb"), "b", check=True)
    git(repo, "worktree", "lock", "--reason", "agent busy", str(root / "wa"), check=True)
    gitlab.rmtree(root / "wb")
    flags = {Path(item["path"]).name: {"detached": item["detached"], "locked": item["locked"],
                                        "prunable": bool(item["prunable"]), "branch": item["branch"]}
             for item in gitlab.worktrees(repo)}
    passed = (flags["det"]["detached"] and flags["wa"]["locked"] == "agent busy" and flags["wb"]["prunable"]
              and flags["wb"]["branch"] == "b")
    return {"passed": passed, "observed": flags,
            "note": "a prunable entry still names its branch, so git still treats that branch as checked out"}


def probe_remove_current(root: Path) -> dict:
    """Removing the worktree a process is standing in is platform dependent; record it so the contract refuses it."""
    repo = init_repo(root / "repo")
    gitlab.branch(repo, "inner")
    git(repo, "worktree", "add", "-q", str(root / "wt-inner"), "inner", check=True)
    remove = git(root / "wt-inner", "worktree", "remove", ".")
    listed = any(gitlab.same_path(item["path"], root / "wt-inner") for item in gitlab.worktrees(repo))
    observed = {"remove_rc": remove.returncode, "entry_still_listed": listed, "directory_exists": (root / "wt-inner").exists(),
                "partial_state": remove.returncode != 0 and not listed, "stderr": remove.stderr.strip()[:160]}
    return {"passed": None, "observed": observed,
            "note": "observation only (not counted): on Windows this can exit non-zero AFTER dropping the metadata"}


def probe_sequencer_paused(root: Path) -> dict:
    """A cherry-pick sequence paused after a resolved step leaves only sequencer/, which status-based checks miss."""
    repo = init_repo(root / "repo")
    gitlab.branch(repo, "donor")
    git(repo, "switch", "-q", "donor", check=True)
    commit(repo, "README.md", "donor\n", "d1")
    d2 = commit(repo, "d2.txt", "second\n", "d2")
    git(repo, "switch", "-q", "main", check=True)
    commit(repo, "README.md", "main\n", "main edit")
    picked = git(repo, "cherry-pick", f"{d2}~1", d2)
    (repo / "README.md").write_text("resolved\n", encoding="utf-8")
    git(repo, "add", "README.md", check=True)
    git(repo, "commit", "-q", "--no-edit", check=True)
    located = gitlab.git_paths(repo, ("CHERRY_PICK_HEAD", "sequencer"))
    status = out(repo, "status", "--porcelain=v1", "--untracked-files=all")
    observed = {"cherry_pick_rc": picked.returncode, "cherry_pick_head": located["CHERRY_PICK_HEAD"].exists(),
                "sequencer": located["sequencer"].is_dir(), "porcelain_status": status}
    passed = picked.returncode != 0 and not observed["cherry_pick_head"] and observed["sequencer"] and status == ""
    return {"passed": passed, "observed": observed, "note": "the contract lists sequencer/ as an in-progress marker"}


def probe_skip_worktree_hidden(root: Path) -> dict:
    """Edits to a skip-worktree file are invisible to status, and `worktree remove` deletes them with rc=0."""
    repo = init_repo(root / "repo")
    commit(repo, "conf.txt", "default\n", "conf")
    gitlab.branch(repo, "cfg")
    git(repo, "worktree", "add", "-q", str(root / "wt-cfg"), "cfg", check=True)
    git(root / "wt-cfg", "update-index", "--skip-worktree", "conf.txt", check=True)
    (root / "wt-cfg" / "conf.txt").write_text("local override\n", encoding="utf-8")
    status = out(root / "wt-cfg", "status", "--porcelain=v1", "--untracked-files=all")
    tags = out(root / "wt-cfg", "ls-files", "-v")
    removal = git(repo, "worktree", "remove", str(root / "wt-cfg"))
    observed = {"porcelain_status": status, "ls_files_v": tags, "remove_rc": removal.returncode,
                "directory_after": (root / "wt-cfg").exists()}
    passed = status == "" and "S conf.txt" in tags and removal.returncode == 0 and not observed["directory_after"]
    return {"passed": passed, "observed": observed, "note": "the contract adds an `ls-files -v` check to 'clean'"}


def probe_target_tag_shadow(root: Path) -> dict:
    """A tag named like the target makes bare-name containment checks lie; full refnames do not."""
    repo = init_repo(root / "repo")
    gitlab.branch(repo, "rel")
    git(repo, "switch", "-q", "-c", "feat", check=True)
    feat = commit(repo, "f.txt", "f\n", "feat")
    git(repo, "switch", "-q", "rel", check=True)
    git(repo, "tag", "rel", feat, check=True)
    bare = git(repo, "merge-base", "--is-ancestor", "feat", "rel")
    full = git(repo, "merge-base", "--is-ancestor", "refs/heads/feat", "refs/heads/rel")
    count_bare = out(repo, "rev-list", "--count", "rel..feat")
    count_full = out(repo, "rev-list", "--count", "refs/heads/rel..refs/heads/feat")
    observed = {"bare_is_ancestor_rc": bare.returncode, "bare_warning": bare.stderr.strip()[:80],
                "full_is_ancestor_rc": full.returncode, "bare_count": count_bare, "full_count": count_full}
    passed = bare.returncode == 0 and full.returncode == 1 and count_bare == "0" and count_full == "1"
    return {"passed": passed, "observed": observed, "note": "every revision argument in the contract uses refs/heads/<name>"}


PROBES = [probe_upstream_behind, probe_upstream_read, probe_worktree_remove, probe_prune_scope, probe_merge_mechanics,
          probe_ignored_overwrite, probe_tag_shadow, probe_case_refs, probe_rebase_in_progress,
          probe_untracked_hidden, probe_merge_tree, probe_worktree_flags, probe_sequencer_paused,
          probe_skip_worktree_hidden, probe_target_tag_shadow, probe_remove_current]


def label(result: dict) -> str:
    """PASS / FAIL for assertions, OBS for observation-only probes."""
    return "OBS" if result["passed"] is None else ("PASS" if result["passed"] else "FAIL")


def tally(results: list[dict]) -> tuple[int, int, int]:
    """(passed assertions, total assertions, observations)."""
    asserted = [r for r in results if r["passed"] is not None]
    return sum(r["passed"] for r in asserted), len(asserted), len(results) - len(asserted)


def run_probe(probe, base: str | None) -> dict:
    """Run one probe in its own fixture root; an exception becomes a failed result with the error text."""
    with gitlab.fixture_root(base) as root:
        try:
            result = probe(root)
        except Exception as error:  # noqa: BLE001 - a probe crash is a result, not a harness crash
            result = {"passed": False, "observed": {"error": f"{type(error).__name__}: {error}"}, "note": ""}
    return {"probe": probe.__name__.removeprefix("probe_"), "claim": (probe.__doc__ or "").strip(), **result}


def render(results: list[dict], version: str) -> str:
    """Markdown summary of a probe run."""
    passed, total, observed = tally(results)
    lines = ["# Git behavior probes", "", f"- Git: `{version}`",
             f"- Result: **{passed}/{total} assertions passed**, {observed} observation(s) recorded", ""]
    for result in results:
        lines += [f"## {label(result)} `{result['probe']}`", "", result["claim"], "",
                  f"Note: {result['note']}", "", "```json", json.dumps(result["observed"], ensure_ascii=False, indent=2),
                  "```", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture-root", help="short directory for fixtures (Windows path length)")
    options = parser.parse_args()
    version = subprocess.run(["git", "--version"], text=True, capture_output=True, check=True).stdout.strip()
    results = [run_probe(probe, options.fixture_root) for probe in PROBES]
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "result.json").write_text(json.dumps({"git": version, "results": results}, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8")
    (RESULTS_DIR / "summary.md").write_text(render(results, version), encoding="utf-8")
    for result in results:
        print(f"{label(result):4} {result['probe']}")
    passed, total, observed = tally(results)
    print(f"{passed}/{total} probe assertions passed, {observed} observation(s) ({version})")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
