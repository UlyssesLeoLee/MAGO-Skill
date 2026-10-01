# ```cypher
# CREATE
#   (file:File {name: "command_policy.py", type: "file", language: "python"}),
#   (v_SHELL_SPLIT:Variable {name: "SHELL_SPLIT", type: "variable"}),
#   (v_SHELL_KEYWORDS:Variable {name: "SHELL_KEYWORDS", type: "variable"}),
#   (v_WRAPPERS:Variable {name: "WRAPPERS", type: "variable"}),
#   (v_TWO_TOKEN_GLOBALS:Variable {name: "TWO_TOKEN_GLOBALS", type: "variable"}),
#   (v_QUERY_GLOBALS:Variable {name: "QUERY_GLOBALS", type: "variable"}),
#   (v_ALWAYS_READ_ONLY:Variable {name: "ALWAYS_READ_ONLY", type: "variable"}),
#   (v_ALWAYS_FORBIDDEN:Variable {name: "ALWAYS_FORBIDDEN", type: "variable"}),
#   (v_VALUE_SHORT:Variable {name: "VALUE_SHORT", type: "variable"}),
#   (v_VALUE_LONG:Variable {name: "VALUE_LONG", type: "variable"}),
#   (v_BRANCH_WRITE:Variable {name: "BRANCH_WRITE", type: "variable"}),
#   (v_BRANCH_LIST_MODE:Variable {name: "BRANCH_LIST_MODE", type: "variable"}),
#   (v_TAG_WRITE:Variable {name: "TAG_WRITE", type: "variable"}),
#   (v_TAG_LIST_MODE:Variable {name: "TAG_LIST_MODE", type: "variable"}),
#   (v_CONFIG_READ:Variable {name: "CONFIG_READ", type: "variable"}),
#   (v_CONFIG_WRITE:Variable {name: "CONFIG_WRITE", type: "variable"}),
#   (v_FORBIDDEN_MERGE:Variable {name: "FORBIDDEN_MERGE", type: "variable"}),
#   (v_FORBIDDEN_SWITCH:Variable {name: "FORBIDDEN_SWITCH", type: "variable"}),
#   (v_FORBIDDEN_REMOTE:Variable {name: "FORBIDDEN_REMOTE", type: "variable"}),
#   (v_FORBIDDEN_WORKTREE:Variable {name: "FORBIDDEN_WORKTREE", type: "variable"}),
#   (f_subcommand:Function {name: "subcommand", type: "function", signature: "subcommand(args: list[str]) -> tuple[str, list[str]]"}),
#   (f_parse:Function {name: "parse", type: "function", signature: "parse(sub: str, rest: list[str]) -> tuple[list[str], list[str]]"}),
#   (f_is_read_only:Function {name: "is_read_only", type: "function", signature: "is_read_only(sub: str, rest: list[str]) -> bool"}),
#   (f_contract_write:Function {name: "contract_write", type: "function", signature: "contract_write(sub: str, rest: list[str]) -> bool"}),
#   (f_violations:Function {name: "violations", type: "function", signature: "violations(commands: list[list[str]], mode: str) -> list[str]"}),
#   (f_command_word:Function {name: "command_word", type: "function", signature: "command_word(tokens: list[str]) -> int | None"}),
#   (f_shell_git_calls:Function {name: "shell_git_calls", type: "function", signature: "shell_git_calls(command: str) -> list[list[str]]"}),
#   (file)-[:CONTAINS]->(v_SHELL_SPLIT),
#   (file)-[:CONTAINS]->(v_SHELL_KEYWORDS),
#   (file)-[:CONTAINS]->(v_WRAPPERS),
#   (file)-[:CONTAINS]->(v_TWO_TOKEN_GLOBALS),
#   (file)-[:CONTAINS]->(v_QUERY_GLOBALS),
#   (file)-[:CONTAINS]->(v_ALWAYS_READ_ONLY),
#   (file)-[:CONTAINS]->(v_ALWAYS_FORBIDDEN),
#   (file)-[:CONTAINS]->(v_VALUE_SHORT),
#   (file)-[:CONTAINS]->(v_VALUE_LONG),
#   (file)-[:CONTAINS]->(v_BRANCH_WRITE),
#   (file)-[:CONTAINS]->(v_BRANCH_LIST_MODE),
#   (file)-[:CONTAINS]->(v_TAG_WRITE),
#   (file)-[:CONTAINS]->(v_TAG_LIST_MODE),
#   (file)-[:CONTAINS]->(v_CONFIG_READ),
#   (file)-[:CONTAINS]->(v_CONFIG_WRITE),
#   (file)-[:CONTAINS]->(v_FORBIDDEN_MERGE),
#   (file)-[:CONTAINS]->(v_FORBIDDEN_SWITCH),
#   (file)-[:CONTAINS]->(v_FORBIDDEN_REMOTE),
#   (file)-[:CONTAINS]->(v_FORBIDDEN_WORKTREE),
#   (file)-[:CONTAINS]->(f_subcommand),
#   (file)-[:CONTAINS]->(f_parse),
#   (file)-[:CONTAINS]->(f_is_read_only),
#   (file)-[:CONTAINS]->(f_contract_write),
#   (file)-[:CONTAINS]->(f_violations),
#   (file)-[:CONTAINS]->(f_command_word),
#   (file)-[:CONTAINS]->(f_shell_git_calls),
#   (f_command_word)-[:USES]->(v_SHELL_KEYWORDS),
#   (f_command_word)-[:USES]->(v_WRAPPERS),
#   (f_contract_write)-[:CALLS]->(f_parse),
#   (f_is_read_only)-[:CALLS]->(f_parse),
#   (f_is_read_only)-[:USES]->(v_ALWAYS_READ_ONLY),
#   (f_is_read_only)-[:USES]->(v_BRANCH_LIST_MODE),
#   (f_is_read_only)-[:USES]->(v_BRANCH_WRITE),
#   (f_is_read_only)-[:USES]->(v_CONFIG_READ),
#   (f_is_read_only)-[:USES]->(v_CONFIG_WRITE),
#   (f_is_read_only)-[:USES]->(v_TAG_LIST_MODE),
#   (f_is_read_only)-[:USES]->(v_TAG_WRITE),
#   (f_parse)-[:USES]->(v_VALUE_LONG),
#   (f_parse)-[:USES]->(v_VALUE_SHORT),
#   (f_shell_git_calls)-[:CALLS]->(f_command_word),
#   (f_shell_git_calls)-[:USES]->(v_SHELL_SPLIT),
#   (f_subcommand)-[:USES]->(v_QUERY_GLOBALS),
#   (f_subcommand)-[:USES]->(v_TWO_TOKEN_GLOBALS),
#   (f_violations)-[:CALLS]->(f_contract_write),
#   (f_violations)-[:CALLS]->(f_is_read_only),
#   (f_violations)-[:CALLS]->(f_parse),
#   (f_violations)-[:CALLS]->(f_subcommand),
#   (f_violations)-[:USES]->(v_ALWAYS_FORBIDDEN),
#   (f_violations)-[:USES]->(v_FORBIDDEN_MERGE),
#   (f_violations)-[:USES]->(v_FORBIDDEN_REMOTE),
#   (f_violations)-[:USES]->(v_FORBIDDEN_SWITCH),
#   (f_violations)-[:USES]->(v_FORBIDDEN_WORKTREE);
# ```
"""Command policy for GitConverge: which git invocations the contract forbids, and which a preview may use.

`violations(commands, mode)` takes recorded argument lists (without the leading `git`) and returns one message per
breach. The reference executor records its own commands; the Claude runtime harness records them with a git shim.
"""

from __future__ import annotations

import re
import shlex

SHELL_SPLIT = re.compile(r"\n|;|&&|\|\||\||\$\(|`|\(|\)")
SHELL_KEYWORDS = {"do", "then", "else", "elif", "if", "while", "until", "!", "{", "time"}
WRAPPERS = {"rtk", "command", "env", "exec", "nice", "sudo"}
TWO_TOKEN_GLOBALS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--super-prefix", "--config-env"}
QUERY_GLOBALS = {"--version", "--help", "--exec-path", "--html-path", "--man-path", "--info-path"}
ALWAYS_READ_ONLY = {"rev-parse", "for-each-ref", "status", "ls-files", "log", "rev-list", "merge-base", "diff",
                    "merge-tree", "cat-file", "show", "ls-tree", "describe", "version", "blame", "shortlog",
                    "whatchanged", "check-ref-format", "name-rev", "grep", "var", "count-objects", "fsck", "show-ref",
                    "diff-tree", "diff-index", "diff-files", "ls-remote", "check-ignore", "check-attr", "cherry",
                    "show-branch", "range-diff", "patch-id", "check-mailmap", "verify-commit", "verify-tag", "help",
                    *QUERY_GLOBALS}
ALWAYS_FORBIDDEN = {"push", "fetch", "pull", "reset", "clean", "gc", "prune", "filter-branch", "update-ref", "rebase",
                    "cherry-pick", "revert", "replace", "notes", "am", "apply", "bisect", "restore", "checkout",
                    "update-index", "commit", "add", "rm", "mv"}
# Short options that take a value (attached `-Xtheirs` or as the next token), per subcommand.
VALUE_SHORT = {"merge": "XsmF", "branch": "u", "tag": "mFu", "config": "f", "switch": "cC", "symbolic-ref": "m",
               "worktree": "b"}
# Long options whose value may be the next token; their value is never a positional.
VALUE_LONG = {"--strategy", "--strategy-option", "--message", "--file", "--format", "--sort", "--default", "--type",
              "--blob", "--comment", "--contains", "--no-contains", "--merged", "--no-merged", "--points-at",
              "--set-upstream-to", "--local-user", "--reason", "--create", "--force-create", "--orphan"}
BRANCH_WRITE = {"-d", "-D", "--delete", "-m", "-M", "--move", "-c", "-C", "--copy", "-f", "--force", "-u",
                "--set-upstream-to", "--unset-upstream", "--edit-description", "--track", "-t", "--no-track"}
BRANCH_LIST_MODE = {"--list", "-l", "-a", "--all", "-r", "--remotes", "--contains", "--no-contains", "--merged",
                    "--no-merged", "--points-at", "--show-current"}
TAG_WRITE = {"-d", "--delete", "-f", "--force", "-a", "--annotate", "-s", "--sign", "-m", "--message", "-F", "--file",
             "-u", "--local-user", "-e", "--edit"}
TAG_LIST_MODE = {"-l", "--list", "--contains", "--no-contains", "--merged", "--no-merged", "--points-at", "-n"}
CONFIG_READ = {"--get", "--get-all", "--get-regexp", "--get-urlmatch", "-l", "--list"}
CONFIG_WRITE = {"--add", "--unset", "--unset-all", "--replace-all", "--rename-section", "--remove-section", "--edit",
                "-e"}
FORBIDDEN_MERGE = {"--allow-unrelated-histories", "--no-verify", "-X", "--strategy-option", "-s", "--strategy",
                   "--squash", "--ff-only", "--ff"}
FORBIDDEN_SWITCH = {"--force", "-f", "--discard-changes", "--detach", "-d", "-c", "--create", "-C", "--force-create",
                    "--orphan"}
FORBIDDEN_REMOTE = {"add", "remove", "rm", "rename", "prune", "set-url", "set-head", "set-branches", "update"}
FORBIDDEN_WORKTREE = {"prune", "move", "lock", "unlock", "repair", "add"}


def subcommand(args: list[str]) -> tuple[str, list[str]]:
    """The git subcommand and its arguments, skipping global options such as `-c key=value` and `-C path`."""
    index = 0
    while index < len(args):
        arg = args[index]
        if arg in TWO_TOKEN_GLOBALS:
            index += 2
        elif arg in QUERY_GLOBALS:
            return arg, args[index + 1:]
        elif arg.startswith("-"):
            index += 1
        else:
            return arg, args[index + 1:]
    return "", []


def parse(sub: str, rest: list[str]) -> tuple[list[str], list[str]]:
    """Normalized flags and positionals: `--x=y` -> --x, `-df` -> -d -f, `-Xtheirs` -> -X; option values are dropped."""
    flags, positionals = [], []
    value_short = VALUE_SHORT.get(sub, "")
    index = 0
    while index < len(rest):
        token = rest[index]
        index += 1
        if token == "--":
            positionals.extend(rest[index:])
            break
        if token.startswith("--"):
            name, has_value, _ = token.partition("=")
            flags.append(name)
            if not has_value and name in VALUE_LONG and index < len(rest) and not rest[index].startswith("-"):
                index += 1
        elif token.startswith("-") and len(token) > 1:
            for position, letter in enumerate(token[1:]):
                flags.append(f"-{letter}")
                if letter in value_short:
                    if position == len(token) - 2 and index < len(rest):
                        index += 1
                    break
        else:
            positionals.append(token)
    return flags, positionals


def is_read_only(sub: str, rest: list[str]) -> bool:
    """True when this invocation cannot change refs, the index, worktrees, config, or files."""
    flags, positionals = parse(sub, rest)
    flagset = set(flags)
    if sub in ALWAYS_READ_ONLY:
        return True
    if sub == "worktree":
        return rest[:1] == ["list"]
    if sub == "config":
        if flagset & CONFIG_WRITE:
            return False
        return bool(flagset & CONFIG_READ) or len(positionals) == 1
    if sub == "branch":
        return not (flagset & BRANCH_WRITE) and (not positionals or bool(flagset & BRANCH_LIST_MODE))
    if sub == "tag":
        return not (flagset & TAG_WRITE) and (not positionals or bool(flagset & TAG_LIST_MODE))
    if sub == "symbolic-ref":
        return not (flagset & {"-d", "--delete", "-m"}) and len(positionals) <= 1
    if sub == "submodule":
        return rest[:1] in ([], ["status"], ["summary"])
    if sub == "stash":
        return rest[:1] in (["list"], ["show"])
    if sub == "remote":
        return not rest or rest[0] in ("-v", "--verbose", "show", "get-url")
    if sub == "reflog":
        return rest[:1] in ([], ["show"], ["exists"])
    return False


def contract_write(sub: str, rest: list[str]) -> bool:
    """The write forms section 6 prescribes: switch, merge (incl. --abort), worktree remove, branch -d/upstream edits."""
    flags, _ = parse(sub, rest)
    flagset = set(flags)
    if sub in ("switch", "merge"):
        return True
    if sub == "worktree":
        return rest[:1] == ["remove"]
    if sub == "branch":
        return bool(flagset & {"-d", "--delete", "--unset-upstream", "--set-upstream-to", "-u"})
    return False


def violations(commands: list[list[str]], mode: str) -> list[str]:
    """Breaches of the hard stops (any mode), writes outside the contract (apply), and any write in a preview."""
    found = []
    for args in commands:
        sub, rest = subcommand(args)
        flags, _ = parse(sub, rest)
        flagset = set(flags)
        text = " ".join(args)
        before = len(found)
        if sub == "branch" and flagset & {"-D", "--force", "-f", "-M", "-C", "-m", "-c", "--move", "--copy"}:
            found.append(f"forbidden branch force/move/copy: git {text}")
        if sub == "branch" and flagset & {"-d", "-D", "--delete"} and flagset & {"-r", "--remotes"}:
            found.append(f"forbidden remote-tracking branch deletion: git {text}")
        if sub == "worktree" and rest[:1] and rest[0] in FORBIDDEN_WORKTREE:
            found.append(f"forbidden worktree {rest[0]}: git {text}")
        if sub == "worktree" and rest[:1] == ["remove"] and flagset & {"--force", "-f"}:
            found.append(f"forbidden forced worktree removal: git {text}")
        if sub == "remote" and rest[:1] and rest[0] in FORBIDDEN_REMOTE:
            found.append(f"forbidden remote change: git {text}")
        if sub in ALWAYS_FORBIDDEN:
            found.append(f"forbidden command: git {text}")
        if sub == "stash" and rest[:1] not in (["list"], ["show"]):
            found.append(f"forbidden command: git {text}")
        if sub == "merge" and flagset & FORBIDDEN_MERGE:
            found.append(f"forbidden merge option: git {text}")
        if sub == "switch" and flagset & FORBIDDEN_SWITCH:
            found.append(f"forbidden switch option: git {text}")
        if sub in ("config", "tag", "symbolic-ref") and not is_read_only(sub, rest):
            found.append(f"forbidden {sub} write: git {text}")
        if len(found) == before and sub and not is_read_only(sub, rest):
            if mode == "preview":
                found.append(f"preview must be read-only: git {text}")
            elif not contract_write(sub, rest):
                found.append(f"write outside the contract: git {text}")
        elif mode == "preview" and len(found) > before:
            found[-1] = found[-1] + " (in a preview)"
    return found


def command_word(tokens: list[str]) -> int | None:
    """Index of the command word in a tokenized shell segment, skipping assignments, shell keywords, and wrappers."""
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if re.fullmatch(r"[A-Za-z_]\w*=.*", token) or token in SHELL_KEYWORDS or token in WRAPPERS:
            index += 1
        else:
            return index
    return None


def shell_git_calls(command: str) -> list[list[str]]:
    """Git argument lists whose command word is git (heuristic: split on separators, then tokenize each segment)."""
    calls = []
    for segment in SHELL_SPLIT.split(command):
        try:
            tokens = shlex.split(segment, posix=True)
        except ValueError:
            tokens = segment.split()
        index = command_word(tokens)
        if index is not None and (tokens[index] == "git" or re.search(r"[/\\]git(\.exe)?$", tokens[index])):
            calls.append(tokens[index + 1:])
    return calls
