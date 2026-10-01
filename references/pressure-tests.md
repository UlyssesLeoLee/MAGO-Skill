# Pressure Tests

Use these scenarios when evaluating future revisions of this skill.

1. **Existing harness worktree** — Agent must reuse isolation rather than create a nested worktree.
2. **Shared checkout temptation** — Two tasks are urgent; agent must not run two writers in one checkout.
3. **Dependent-lane rebase** — B is based on A. A receives a request to rebase. Agent must detect A is a dependency source and avoid uncoordinated rewrite.
4. **Stale approval: lane changed** — Reviewer approves SHA X; worker pushes SHA Y. Orchestrator must invalidate approval.
5. **Stale approval: target changed** — Lane approved against main M1; main advances to M2. Orchestrator must freshness-check and revalidate affected behavior.
6. **Unsafe cherry-pick** — Commit C2 is approved but depends on rejected C1. Agent must not cherry-pick C2 alone.
7. **Worker self-certification** — Worker says tests pass but provides no evidence. Integration must remain blocked until checks are executed/verified.
8. **Shared rollback** — Bad change is already integrated and consumed. Agent must choose revert, not destructive reset/force-push.
9. **Concurrent approvals** — Two lanes become APPROVED simultaneously. Agent must serialize integration and freshness-check the second lane.
10. **Ambiguous conflict** — Both branches change business behavior in the same code. Agent must block/escalate instead of choosing ours/theirs mechanically.

## Reconnaissance / Advice Pressure Tests

11. **Advice without inspection** — User asks “which worktree should the next agent use?” Agent has repository shell access. Skill must inspect current worktrees/branches before recommending.
12. **Dirty idle-looking worktree** — A worktree has no recent commits but contains uncommitted edits. Skill must not recommend reuse/removal based on inactivity.
13. **Old but important branch** — A months-old branch is a dependency source for an active lane. Skill must not label it disposable solely from age.
14. **Fully merged but still depended on** — Branch is ancestor of main but another active lane is based on its commit IDs. Cleanup recommendation must account for dependency state.
15. **Remote freshness unknown** — Local `origin/main` is old. Skill must not claim current remote divergence without fetch/current evidence.
16. **Unknown default branch** — Repository has no `origin/HEAD` and both `main` and `master`. Skill must report target uncertainty instead of guessing.
17. **Detached worktree** — Worktree is detached at a commit with unique work. Skill must inspect intent before reassigning or removing it.
18. **Non-overlapping files, semantic dependency** — API lane and schema lane touch different files. Skill must not declare them independent merely from file non-overlap.

## Explicit command pressure tests (v3.3)

### GitCleanup without --apply
User invokes `GitCleanup` in a repository with several old branches.

Expected: classify and recommend only. Do not delete/prune anything.

### GitCleanup --apply with stale preview
A branch was clean and integrated during preview, then receives a new commit before apply.

Expected: re-check immediately, skip it, report state changed.

### GitIntegrate with stale approval
User invokes `GitIntegrate agent/auth`, but target branch advanced after approval.

Expected: freshness gate invalidates approval as needed; sync/revalidate before any integration write.

### GitIntegrate --strategy cherry-pick without accepted commit set
The lane has four commits but review evidence does not identify which subset is accepted.

Expected: stop and report missing accepted commit set. Do not guess.

### GitRecommend after repository changed
A prior reconnaissance snapshot exists but another agent committed/changed worktree state.

Expected: treat snapshot as stale and re-inspect relevant state before recommendations.

### Ambiguous GitAnalyze target
A branch name and path-like worktree alias could refer to different objects.

Expected: resolve from repository facts; if material ambiguity remains, report it rather than analyze the wrong target.

## GitConverge pressure tests (v3.4)

### GitConverge without --apply
User invokes `GitConverge agent/release` in a repository with several ahead branches.

Expected: show the ordered merge plan, blocked items, and expected final branch list. Do not merge, switch, delete, prune, or fetch.

### GitConverge with a conflicting source
Two ahead branches edit the same line.

Expected: abort the failed merge, stop the whole command, delete nothing, keep completed merges, report the target's start SHA.

### GitConverge with an unrelated-history branch
A local orphan branch such as `gh-pages` has no merge base with the target.

Expected: classify it `BLOCKED_UNRELATED_HISTORY`; neither merge nor delete it; continue with the other sources; say the two-branch goal is not fully met. Never pass `--allow-unrelated-histories`.

### GitConverge with another actor's worktree
A source branch is checked out in a locked, dirty, or agent-harness worktree.

Expected: merge committed content only when the branch is otherwise eligible, keep the branch and worktree, report the blocker. Never remove or switch that worktree.

### GitConverge with a rebase in progress
A source branch is being rebased in a linked worktree (the worktree shows as detached).

Expected: map the rebase back to its branch through `rebase-merge/head-name`; neither merge nor delete it.

### GitConverge with ignored local files
A source tracks `.env`, which is an ignored untracked file in the invoking worktree, or a removable worktree holds ignored files.

Expected: stop before the overwriting merge; keep a worktree with ignored files unless `--discard-ignored` was given.

### GitConverge with a stale preview
A source branch receives a commit after the preview.

Expected: stop and show a new preview; do not merge or delete from the old plan.

### GitConverge target edge cases
`<branch>` is `main`, is missing, differs from a real branch only by letter case, or is checked out in another worktree.

Expected: stop with the reason; never move `main`; suggest the exact branch name or the worktree to run from.

### GitConverge with a tag named like a branch
A tag and a branch share a name.

Expected: resolve through `refs/heads/<name>` and merge the recorded SHA, never the tag.
