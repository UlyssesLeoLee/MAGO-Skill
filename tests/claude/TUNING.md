# GitConverge tuning log

Every round: what the tests showed, which of the three things was wrong (the **contract**, the **reference executor**, or the
**test itself**), what was changed, and what the rerun showed. Environment: Git 2.41.0.windows.1, Windows 11, Python 3.13,
Claude Code 2.1.284 with `claude-sonnet-5-5` for the runtime layer.

## Round 1: Git behavior probes

| | |
|---|---|
| Symptom | 12/12 probes passed, but the `ignored_overwrite` probe recorded `overlap_before_merge: []` |
| Cause | **Test bug.** The overlap between "paths the source changes" and "ignored local files" was computed after the merge, when `.env` had become tracked |
| Change | Compute the overlap before the merge and assert it equals `[".env"]` |
| Result | The contract's detection formula (`diff --name-only <merge-base> <sha>` ∩ `ls-files -o -i --exclude-standard`) is now itself verified |

Two probes also confirmed platform facts worth keeping: `refs/heads/Target` resolves on this NTFS checkout while a differently
cased name is not in the exact `for-each-ref` listing (so the exact-match rule is needed), and removing the worktree you stand in
exits 255 after Git has already dropped its metadata (so a non-zero `worktree remove` must keep the branch).

## Round 2: reference scenarios, first run (29/31)

| Failure | Cause | Change |
|---|---|---|
| `upstream-behind`: `branch -d` refused | **Reference bug.** It read the upstream with `rev-parse refs/heads/x@{upstream}`, which Git rejects ("no such branch") | Contract now records the upstream with `git for-each-ref --format='%(upstream)\|%(upstream:short)'`, which works with full refnames and is empty when there is none. Probe `upstream_read` locks this in, including restoring with `--set-upstream-to=<short>` |
| `conflict-stops`: expected `merge-tree` to predict the x1/x2 clash | **Contract wording and test both overstated.** `merge-tree` tests a source against the current target tip only, so it cannot see a clash between two sources | Contract: "a hint only; it cannot see a clash between two sources". Test now asserts that blind spot explicitly. New scenario `conflict-predicted` covers a source that clashes with the target tip itself |

Result: 32/32.

## Round 3: do the tests have teeth? (mutation checks)

All-green runs say nothing about whether the oracles would catch a wrong implementation, so 20 rules were broken on purpose.

| Finding | Cause | Change |
|---|---|---|
| `branch -D` and `branch -d` leave identical repositories | **Test gap.** State oracles cannot see several hard stops | Added the command trace and `command_policy.py`: forbidden commands in any mode, read-only commands in preview. `force-delete-D` is now killed by the policy alone |
| 6 mutations "killed" only because an oracle crashed (`KeyError: 'main'` after main was deleted, `None["code"]` after a run that should have stopped) | **Test bug.** A crash is not a diagnosis | Oracles read with `.get()`; `stop_code()` tolerates runs that did not stop |
| `no-unrelated-check` died with a Git usage error, not a scenario failure | **Mutation was unrealistic** | The fake `merge-base` now returns a real ref so the merge itself fails |

Result: 19/20 killed. The survivor, `ignore-lock-gate`, is expected: Git refuses to remove a locked worktree, so the end state
does not change. That gate is defence in depth and is checked at the source-contract layer.

## Round 4: the real Claude CLI

First run of `/GitConverge agent/release` through `claude -p` in a disposable repository: the agent loaded the skill, read
section 6, inspected, and produced a correct plan (17 turns, $0.47). Infrastructure defects found on the way:

| Symptom | Cause | Change |
|---|---|---|
| The git trace held only 6 calls; none were the agent's | **Harness bug.** A PATH shim is bypassed because Git Bash's `/etc/profile` puts `/mingw64/bin` first | Replaced the shim with `GIT_TRACE2_EVENT`, which logs every git process however it is launched (25 calls in the same case) |
| Policy flagged Claude Code's own `git config user.name` as a config write | **Policy bug.** A single-key `config` is a read | `config <key>` with no value and no write flag is read-only |
| Policy flagged `git --exec-path` | **Policy bug.** The parser treated `--exec-path` as an option to skip | Query globals (`--exec-path`, `--version`, ...) are subcommands; two-token globals (`--git-dir x`) are skipped properly |
| `fixture-check` failed `dirty-source-worktree` | **Test bug.** That fixture is dirty on purpose | The check now asserts only that `.claude` appears in no worktree status |
| `echo git is great` parsed as a git call | **Parser bug** | A git call must be in command position (after assignments, `do`/`then`, and wrappers such as `rtk`) |

Core scenarios on the real CLI, before any wording change: **8/8 PASS** (~$2 total, 5 to 34 turns each). The agent rejected
`Agent/Release` with the exact name suggested, stopped before an ignored-file overwrite, left the orphan `gh-pages` alone, kept a dirty
worktree's branch, merged `feat` rather than the same-named tag, and aborted a conflicting merge without deleting anything.

## Round 5: something the end state cannot show

Reading the transcripts of the apply runs showed that the agent surveyed silently and **merged after only a status line**
(0 to 199 characters before the first write), although the contract says `--apply` acts on "the plan printed by that run", which is
the user's acceptance. Every state oracle passed because the final repositories were right.

| | |
|---|---|
| Measure | New check `the plan is printed before the first write`: at least 300 characters of assistant text, naming every local branch, before the first git call that can change the repository (found by parsing each Bash command with the policy classifier) |
| Baseline | 0 of 6 apply runs that wrote anything complied |
| Change | See Round 6 |
