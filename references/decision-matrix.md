# Decision Matrix

Load this reference only when the correct Git operation is unclear.

| Situation | Operation | Why / guard |
|---|---|---|
| Start independent parallel task | branch + worktree | isolates writers |
| Harness already isolated workspace | reuse it | avoid phantom/nested state |
| Integration target advanced; lane is private and unconsumed | rebase | cleanly replay on latest base |
| Integration target advanced; lane is published or another lane depends on its commits | merge target into lane, or coordinated retarget | avoid breaking commit-ID dependencies |
| All lane changes approved | merge according to repo policy | accept coherent lane |
| All changes approved but repo wants one delivery commit | squash merge | concise integration history without requiring worker-history rewrite |
| Only some commits approved | cherry-pick dependency-safe set | selective integration |
| Selected commit depends on rejected earlier commit | include dependency, refactor commit, or reject selection | prevent incomplete change |
| Private checkpoint history is noisy | interactive rebase/squash | cleanup is safe only while rewrite-safe |
| Private lane is fundamentally wrong | reset/recreate | discard private history |
| Shared/integrated change is wrong | revert | preserves published history |
| Unfinished edits temporarily block an operation | prefer another worktree; stash only when warranted | hidden state is harder to orchestrate |
| Two lanes overlap heavily | serialize or appoint designated integrator | reduce conflict/race cost |
| Two approved lanes are ready simultaneously | merge queue / one integration writer | prevent stale approvals and target races |
| Review passed but lane HEAD changed afterward | invalidate approval; review changed delta | reviewed object no longer matches integrated object |
| Review passed but target advanced afterward | sync, validate, re-review affected delta | target assumptions may be stale |
| Conflict has ambiguous business meaning | BLOCKED | never guess semantics |

## Rewrite-Safety Test

History is rewrite-safe only if all are true:

1. branch is not protected/shared;
2. no human/agent is consuming its current commit IDs;
3. no active dependent lane is based on those commit IDs;
4. repository policy permits rewriting it.

If any condition is false or unknown, treat the branch as non-rewrite-safe.

## Cherry-Pick Safety Test

Before selective integration:

1. inspect selected commit diff and parent context;
2. identify required earlier commits, schema/config/API assumptions, and generated artifacts;
3. apply the intended set in dependency order to a temporary candidate if uncertainty remains;
4. run targeted and required repository validation;
5. only then integrate the set to the protected target.

## Merge Strategy

The skill deliberately does not mandate `--no-ff`, fast-forward, squash merge, or merge commits globally. The repository's existing policy is authoritative. The orchestrator chooses **what is accepted**; repository policy chooses **how accepted history is represented**.

## Reconnaissance / Advice Decisions

| Situation | First action | Recommendation guard |
|---|---|---|
| User asks which worktree/branch to use | quick repository scan | inspect current ownership, dirtiness, base, and active task before assigning |
| User asks whether a branch is safe to merge | deep-scan branch vs integration target | ancestry/ahead-behind is necessary but validation and semantic review still matter |
| User asks whether to rebase | inspect rewrite safety and downstream consumers | never infer safety merely because branch is private-looking |
| User asks what can be deleted | inspect integration, unique work, active dependencies, dirty worktrees | age/behind/upstream-gone alone is insufficient |
| User asks why branches diverged | calculate merge-base and ahead/behind, inspect unique commits | distinguish topology facts from semantic cause |
| User asks whether another agent can start | inspect available clean idle lanes and overlap/dependency risk | create a new worktree when reuse is uncertain |
| User asks for cleanup/organization advice | inventory all relevant worktrees/branches first | recommend actions; do not mutate during reconnaissance by default |
| Remote-current status matters | establish remote freshness | fetch only when authorized/appropriate, then re-run comparisons |
