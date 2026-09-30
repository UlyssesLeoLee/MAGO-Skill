# Explicit Command Contracts

This reference defines the command-layer behavior for `multi-agent-git-orchestrator` v3.3.

These are **semantic command intents**. Canonical names use a leading `/`. A host may expose them as slash commands, palette actions, prompt aliases, or plain-text invocations. If slash commands are unsupported, accept the same name without `/`. The behavior must remain the same.

## Argument and Help Behavior

All five commands accept `--help`. When it is present, show that command's usage, argument descriptions, defaults, and examples, then stop before inspecting or changing a repository. `--help` takes precedence over other arguments.

Recognize only the options listed for each command. For an unknown option or a required option value that is missing or invalid, explain the issue and show the relevant usage without executing the command. If a required positional target is missing, ask the user for it. Host adapters should preserve the supplied argument text and route `--help` to this reference.

Host entry points are Claude Code `/GitRecon`, Hermes `/git-recon`, and Codex `$git-recon` (use the corresponding command name for the other four). Append the same arguments after the host-specific entry point.

## Host Adapter Contract

Each host reaches the same canonical command through its own adapter. Adapters differ only in how they receive arguments and locate shared files; the command behavior below is identical.

| Host | Adapter | Arguments arrive as | Shared files are located by |
|---|---|---|---|
| Claude Code | `commands/Git*.md` (installed into `~/.claude/commands/`) | `$ARGUMENTS` in the command template | loading the orchestrator skill (listed as `MAGOS`, `multi-agent-git-orchestrator`, or `MAGO-Skill`) |
| Codex | `skills/git-*/SKILL.md` + `agents/openai.yaml` | the text after `$git-*` in the user's message | resolving `../../SKILL.md` and `../../references/*.md` relative to the adapter's `SKILL.md` |
| Hermes | `skills/git-*/SKILL.md` | the instruction Hermes appends after the skill content ("...alongside the skill invocation:" for one command, `User instruction:` for stacked commands) | the absolute `[Skill directory: ...]` path plus `../..`, read with the file or terminal tool (the skill viewer rejects `..`), or the root skill `multi-agent-git-orchestrator` and its `references/` files |

Rules for every adapter:

- `skills/` adapters must not read `commands/*.md`; those wrappers contain Claude-specific loading steps.
- Codex adapters set `policy.allow_implicit_invocation: false`, so they run only when selected explicitly; the root skill keeps semantic activation. Hermes has no per-skill switch, so `git-integrate` and `git-cleanup` refuse to write unless invoked explicitly.
- If the shared rules (`SKILL.md`, `references/commands.md`) cannot be read, read-only commands may continue read-only and report the incomplete installation; `GitIntegrate` must not integrate and `GitCleanup` must not delete.
- An installed package must contain `SKILL.md`, every file under `references/`, and every `skills/git-*/SKILL.md` with its `agents/openai.yaml`, laid out exactly as in this repository, so that the relative paths above resolve.

## 1. GitRecon

### Invocation

```text
/GitRecon
/GitRecon --remote
/GitRecon --help
```

### Arguments

| Argument | Required | Description |
|---|---:|---|
| `--remote` | No | Refresh remote-tracking refs before classification. It does not change branches, worktrees, or commit history. |
| `--help` | No | Show this command's usage and stop without inspecting the repository. |

Examples: `/GitRecon --remote`, `/GitRecon --help`.

### 中文描述

调查当前 Git 仓库整体状态。主动检查 branch、worktree、HEAD、ahead/behind、dirty、detached、upstream、已合并情况和潜在风险，并生成仓库现状摘要。默认只读，不修改分支、worktree 或提交历史。

### Required behavior

1. Run the Quick Scan from `reconnaissance.md`.
2. Deep-scan only branches/worktrees needed to explain risks or topology.
3. Classify worktrees and branches.
4. Report integration-target confidence and remote freshness.
5. Do not mutate repository topology.

`--remote` permits a remote refresh before classification. Report if refresh fails or is unavailable.

### Output

```text
Repository Snapshot
- integration target
- worktrees summary
- branches summary
- remote freshness
- high-risk findings
- unknowns
```

## 2. GitAnalyze

### Invocation

```text
/GitAnalyze <branch>
/GitAnalyze <worktree-path>
/GitAnalyze <target> --remote
/GitAnalyze --help
```

### Arguments

| Argument | Required | Description |
|---|---:|---|
| `<target>` | Yes | Branch name or worktree path to analyze. |
| `--remote` | No | Refresh remote-tracking refs before analysis. It does not change branches, worktrees, or commit history. |
| `--help` | No | Show this command's usage and stop without inspecting the repository. |

Examples: `/GitAnalyze feature/auth`, `/GitAnalyze feature/auth --remote`, `/GitAnalyze --help`.

### 中文描述

深入分析指定 branch 或 worktree。调查它与集成分支之间的共同祖先、ahead/behind、独有提交、修改文件、是否已被集成、下游依赖、rewrite 安全性，以及 merge、rebase、cherry-pick、归档或删除等操作的安全性。

### Required behavior

1. Resolve target identity and current HEAD.
2. Establish the integration target or mark it uncertain.
3. Compute ancestry/ahead-behind and unique commits.
4. Inspect worktree cleanliness if the target has a linked worktree.
5. Inspect recorded downstream dependencies and clearly separate inferred semantic risks.
6. Produce an operation-by-operation safety assessment.

### Output

```text
Target
Observed state
Dependencies
Risk findings
Operation safety:
- merge
- rebase
- cherry-pick
- squash/rewrite
- cleanup/delete
Recommendation
```

## 3. GitRecommend

### Invocation

```text
/GitRecommend
/GitRecommend <goal>
/GitRecommend <goal> --remote
/GitRecommend --help
```

### Arguments

| Argument | Required | Description |
|---|---:|---|
| `[goal]` | No | Natural-language question or desired outcome. Omit it for general next-step recommendations. |
| `--remote` | No | Refresh remote-tracking refs before making recommendations. It does not change branches, worktrees, or commit history. |
| `--help` | No | Show this command's usage and stop without inspecting the repository. |

Examples: `/GitRecommend`, `/GitRecommend 哪些分支可以先集成`, `/GitRecommend --remote`, `/GitRecommend --help`.

Example goals:

```text
/GitRecommend 下一步怎么安排3个Agent
/GitRecommend 哪些分支应该先合并
/GitRecommend 给新任务找最合适的worktree
```

### 中文描述

基于当前仓库真实状态给出下一步 Git / 多 Agent 编排建议。主动调查必要的 branch、worktree、依赖和风险，并按优先级建议并行/串行关系、同步顺序、集成候选、阻塞 Lane、下一 Agent 落点和清理候选。

### Required behavior

1. Reuse a reconnaissance snapshot only if it is still fresh; otherwise refresh it.
2. Deep-scan only entities material to the user's goal.
3. Rank recommendations by risk and dependency, not by branch age alone.
4. Each recommendation must include evidence and expected next action.
5. Do not mutate repository state.

### Output

```text
Observed facts
Top risks
Recommended next actions (ordered)
Why
Blocked/unknown items
```

## 4. GitIntegrate

### Invocation

```text
/GitIntegrate <lane-or-branch>
/GitIntegrate <lane-or-branch> --strategy auto
/GitIntegrate <lane-or-branch> --strategy merge
/GitIntegrate <lane-or-branch> --strategy squash
/GitIntegrate <lane-or-branch> --strategy cherry-pick
/GitIntegrate --help
```

### Arguments

| Argument | Required | Description |
|---|---:|---|
| `<lane-or-branch>` | Yes | Source lane or branch to integrate. |
| `--strategy <value>` | No | Integration strategy: `auto`, `merge`, `squash`, or `cherry-pick`. Defaults to `auto`. |
| `--help` | No | Show this command's usage and stop without inspecting or changing the repository. |

Examples: `/GitIntegrate agent/auth`, `/GitIntegrate agent/auth --strategy squash`, `/GitIntegrate --help`.

### 中文描述

安全集成指定 Agent Lane 或 branch。在实际写入集成分支前检查审核状态、commit 依赖、目标分支 freshness、当前 HEAD、验证结果和仓库集成策略；通过门禁后才执行 merge、squash merge 或 cherry-pick，并在集成后重新验证。

### Required behavior

1. Resolve lane/branch and intended integration target.
2. Confirm review/acceptance evidence and validation state.
3. Refresh refs as required by repository policy.
4. Acquire serialized integration ownership or equivalent merge-queue position.
5. Re-check lane HEAD and target HEAD immediately before integration.
6. Select strategy:
   - `auto`: follow repository policy and reviewed acceptance shape;
   - `merge`: whole-lane integration while preserving accepted commits;
   - `squash`: whole-lane delivery as one logical commit when policy allows;
   - `cherry-pick`: only dependency-safe accepted commits; if the accepted commit set is not known, stop and report what is needed.
7. Run post-integration validation.
8. Record source lane/commits and resulting integration commit(s).

### Hard stop conditions

Do not integrate when:

- review/acceptance is missing for non-trivial work;
- lane HEAD or integration target changed after approval and required revalidation is incomplete;
- selected cherry-picks have unresolved dependencies;
- protected-branch/repository policy forbids the operation;
- semantic conflict cannot be resolved from requirements/evidence;
- required validation is failing due to the candidate change.

Never convert this command into force-push, destructive reset, or blind conflict resolution.

## 5. GitCleanup

### Invocation

```text
/GitCleanup
/GitCleanup --apply
/GitCleanup --help
```

### Arguments

| Argument | Required | Description |
|---|---:|---|
| `--apply` | No | Apply safe local cleanup candidates after rechecking their state. Without it, only show a preview. |
| `--help` | No | Show this command's usage and stop without inspecting or changing the repository. |

Examples: `/GitCleanup`, `/GitCleanup --apply`, `/GitCleanup --help`.

### 中文描述

调查并整理可安全清理的 branch 和 worktree。默认只生成清理候选清单；只有显式 `--apply` 才实际删除已经证明安全的对象。

### Preview behavior (default)

Classify every relevant cleanup candidate with evidence:

```text
SAFE_CANDIDATE
BLOCKED_DIRTY
BLOCKED_UNIQUE_WORK
BLOCKED_ACTIVE_OWNER
BLOCKED_DEPENDENCY
BLOCKED_NOT_INTEGRATED
UNKNOWN
```

A branch/worktree is not safe merely because it is old or inactive.

### Apply behavior

`--apply` may clean only `SAFE_CANDIDATE` entries. Re-check each candidate immediately before mutation.

Typical safe operations may include:

```text
git worktree remove <path>
git branch -d <branch>
git worktree prune
```

Constraints:

- do not use `git branch -D` by default;
- do not delete dirty worktrees;
- do not remove branches with unique unpreserved commits;
- do not remove dependency-source branches required by active lanes;
- do not treat remote deletion as implied by local cleanup;
- if state changed between preview and apply, skip the candidate and report it.

### Output

```text
Cleanup candidates
Blocked items + reasons
Applied operations (only with --apply)
Skipped items + reasons
Remaining risks
```

## Command Relationship

```text
/GitRecon
   ↓ repository map
/GitAnalyze <target>
   ↓ deep single-target evidence
/GitRecommend [goal]
   ↓ decision support
/GitIntegrate <target>
   ↓ guarded integration mutation
/GitCleanup [--apply]
   ↓ guarded lifecycle cleanup
```

`/GitRecon`, `/GitAnalyze`, and `/GitRecommend` are observation/advice commands. `/GitIntegrate` is an integration write-intent. `/GitCleanup` is preview-only unless `--apply` is explicit.
