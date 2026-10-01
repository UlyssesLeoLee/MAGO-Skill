# ```cypher
# CREATE
#   (file:File {name: "test_command_policy.py", type: "file", language: "python"}),
#   (v_FORBIDDEN:Variable {name: "FORBIDDEN", type: "variable"}),
#   (v_ALLOWED_APPLY:Variable {name: "ALLOWED_APPLY", type: "variable"}),
#   (v_READ_ONLY:Variable {name: "READ_ONLY", type: "variable"}),
#   (v_NOT_READ_ONLY:Variable {name: "NOT_READ_ONLY", type: "variable"}),
#   (file)-[:CONTAINS]->(v_FORBIDDEN),
#   (file)-[:CONTAINS]->(v_ALLOWED_APPLY),
#   (file)-[:CONTAINS]->(v_READ_ONLY),
#   (file)-[:CONTAINS]->(v_NOT_READ_ONLY);
# ```
"""Unit tests for command_policy: what counts as a forbidden or non-read-only git invocation.

Run: python -X utf8 tests/claude/scripts/test_command_policy.py
"""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import command_policy as policy  # noqa: E402

FORBIDDEN = [
    (["branch", "-D", "x"], "apply"), (["branch", "--delete", "--force", "x"], "apply"),
    (["-C", "d", "branch", "-M", "a", "b"], "apply"), (["worktree", "prune"], "apply"),
    (["worktree", "remove", "--force", "p"], "apply"), (["worktree", "remove", "-f", "p"], "apply"),
    (["push", "origin", "x"], "apply"), (["fetch", "--prune"], "apply"), (["reset", "--hard"], "apply"),
    (["merge", "--squash", "x"], "apply"), (["merge", "-X", "theirs", "x"], "apply"),
    (["merge", "--allow-unrelated-histories", "x"], "apply"), (["merge", "--no-verify", "x"], "apply"),
    (["switch", "--force", "x"], "apply"), (["switch", "--detach", "x"], "apply"),
    (["config", "user.name", "x"], "apply"), (["config", "--unset", "a.b"], "apply"),
    (["update-ref", "-d", "refs/heads/x"], "apply"), (["rebase", "main"], "apply"), (["stash", "push"], "apply"),
    (["gc"], "apply"), (["clean", "-fd"], "apply"),
    # attached and bundled spellings
    (["merge", "--no-ff", "-Xtheirs", "abc"], "apply"), (["merge", "--strategy-option=theirs", "abc"], "apply"),
    (["merge", "--strategy=ours", "abc"], "apply"), (["merge", "-sours", "abc"], "apply"),
    (["branch", "-df", "x"], "apply"), (["branch", "-Dq", "x"], "apply"), (["worktree", "remove", "-ff", "p"], "apply"),
    # force-create, checkout, remote-tracking refs, worktree management, tags, HEAD rewrites
    (["switch", "-C", "main", "abc"], "apply"), (["switch", "--force-create", "main", "abc"], "apply"),
    (["checkout", "-B", "main", "abc"], "apply"), (["checkout", "-f", "agent/release"], "apply"),
    (["checkout", "agent/release"], "apply"), (["branch", "-d", "-r", "origin/x"], "apply"),
    (["branch", "--delete", "--remotes", "origin/x"], "apply"), (["remote", "prune", "origin"], "apply"),
    (["remote", "remove", "origin"], "apply"), (["worktree", "move", "a", "b"], "apply"),
    (["worktree", "unlock", "p"], "apply"), (["tag", "-a", "v1", "-m", "x"], "apply"), (["tag", "-d", "v1"], "apply"),
    (["symbolic-ref", "HEAD", "refs/heads/x"], "apply"), (["update-index", "--skip-worktree", "x"], "apply"),
    (["add", "."], "apply"), (["commit", "-m", "x"], "apply"),
]
ALLOWED_APPLY = [
    ["merge", "--no-ff", "-m", "Merge branch 'a' into t", "abc"], ["merge", "--abort"], ["branch", "-d", "x"],
    ["branch", "--unset-upstream", "x"], ["branch", "--set-upstream-to=origin/x", "x"], ["worktree", "remove", "p"],
    ["switch", "--no-overwrite-ignore", "t"], ["-c", "a=b", "-C", "d", "status", "--porcelain"],
    ["config", "user.name"], ["config", "--get", "branch.main.remote"], ["merge-tree", "--write-tree", "a", "b"],
    ["config", "--bool", "--default", "false", "core.ignorecase"], ["branch", "-u", "origin/x", "x"],
]
READ_ONLY = [
    ["rev-parse", "--show-toplevel"], ["for-each-ref", "--format=%(refname)", "refs/heads"], ["status", "--porcelain=v1"],
    ["worktree", "list", "--porcelain"], ["branch", "-vv"], ["branch", "--list"], ["branch", "--show-current"],
    ["branch", "--contains", "abc"], ["tag", "--list"], ["tag"], ["config", "user.name"], ["config", "--get", "a.b"],
    ["merge-tree", "--write-tree", "a", "b"], ["submodule", "status"], ["stash", "list"], ["remote", "-v"],
    ["log", "--oneline", "a..b"], ["--exec-path"], ["--version"], ["--git-dir", "x", "status"], ["ls-remote", "origin"],
    ["diff", "--name-only", "a", "b"], ["ls-files", "--others", "--ignored", "--exclude-standard"],
    ["check-ignore", "-v", ".env"], ["cherry", "-v", "main", "feat"], ["show-branch", "a", "b"],
    ["range-diff", "a...b"], ["tag", "--contains", "abc"], ["tag", "--merged", "main"], ["tag", "--points-at", "HEAD"],
    ["branch", "--sort=-committerdate"], ["branch", "--format", "%(refname)"], ["reflog", "exists", "refs/heads/x"],
    ["symbolic-ref", "-q", "--short", "HEAD"], ["config", "--get", "--bool", "core.ignorecase"],
    ["config", "--bool", "--default", "false", "core.ignorecase"], ["ls-files", "-v"],
]
NOT_READ_ONLY = [
    ["switch", "x"], ["merge", "x"], ["merge", "--abort"], ["branch", "new-branch"], ["branch", "-d", "x"],
    ["branch", "--unset-upstream", "x"], ["worktree", "remove", "p"], ["worktree", "add", "p", "b"], ["tag", "v1"],
    ["tag", "-d", "v1"], ["config", "a.b", "c"], ["config", "--unset", "a.b"], ["submodule", "update"],
    ["stash", "push"], ["remote", "add", "o", "u"], ["checkout", "x"], ["add", "."], ["commit", "-m", "x"],
    ["symbolic-ref", "HEAD", "refs/heads/x"], ["symbolic-ref", "--delete", "HEAD"],
    ["branch", "--sort=x", "newname"], ["update-index", "--skip-worktree", "x"], ["tag", "-a", "v1", "-m", "x"],
]


class CommandPolicy(unittest.TestCase):
    """Table-driven checks of violations() and is_read_only()."""

    def test_forbidden_commands_are_reported(self):
        for args, mode in FORBIDDEN:
            with self.subTest(args=args):
                self.assertTrue(policy.violations([args], mode), args)

    def test_contract_operations_are_allowed_when_applying(self):
        for args in ALLOWED_APPLY:
            with self.subTest(args=args):
                self.assertEqual(policy.violations([args], "apply"), [], args)

    def test_read_only_commands_pass_in_preview(self):
        for args in READ_ONLY:
            with self.subTest(args=args):
                self.assertEqual(policy.violations([args], "preview"), [], args)

    def test_writing_commands_fail_in_preview(self):
        for args in NOT_READ_ONLY:
            with self.subTest(args=args):
                self.assertTrue(policy.violations([args], "preview"), args)

    def test_option_values_are_not_positionals(self):
        self.assertEqual(policy.parse("merge", ["--no-ff", "-m", "msg", "abc"]), (["--no-ff", "-m"], ["abc"]))
        self.assertEqual(policy.parse("branch", ["-df", "x"]), (["-d", "-f"], ["x"]))
        self.assertEqual(policy.parse("merge", ["-Xtheirs", "abc"]), (["-X"], ["abc"]))
        self.assertEqual(policy.parse("config", ["--default", "false", "core.ignorecase"]), (["--default"], ["core.ignorecase"]))

    def test_global_options_are_skipped(self):
        self.assertEqual(policy.subcommand(["-c", "a=b", "-C", "d", "--no-pager", "merge", "--no-ff"]), ("merge", ["--no-ff"]))
        self.assertEqual(policy.subcommand(["--git-dir", "g", "--work-tree", "w", "status"]), ("status", []))
        self.assertEqual(policy.subcommand([]), ("", []))


class ShellParsing(unittest.TestCase):
    """Git calls are found inside compound shell commands."""

    def test_finds_every_git_call(self):
        calls = policy.shell_git_calls('cd "/tmp/r" && git status --porcelain; T=x; for b in a b; do git log --oneline $b; done | head')
        self.assertEqual([c[0] for c in calls], ["status", "log"])

    def test_non_git_commands_are_ignored(self):
        self.assertEqual(policy.shell_git_calls("echo git is great; ls -la"), [])
        self.assertEqual(policy.shell_git_calls("grep -r git docs/"), [])

    def test_assignments_keywords_and_wrappers_precede_the_command_word(self):
        calls = policy.shell_git_calls("T=refs/heads/x git status; if git merge-base a b; then rtk git log; fi; GIT_DIR=x git branch -d y")
        self.assertEqual([c[0] for c in calls], ["status", "merge-base", "log", "branch"])
        self.assertEqual(policy.shell_git_calls('"C:\\Program Files\\Git\\cmd\\git.exe" status')[0][0], "status")


if __name__ == "__main__":
    unittest.main(verbosity=1)
