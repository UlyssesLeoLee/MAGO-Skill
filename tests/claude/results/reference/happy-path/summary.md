# happy-path

- Title: Everything ahead is merged into the target and only main and the target remain
- Mode: apply
- Result: **PASS**

## Checks

- PASS only main and the target remain
- PASS main was not moved
- PASS every source tip is contained in the target
- PASS files from every source are present
- PASS three real merge commits (main, a, b)
- PASS linked worktree of a deleted branch is gone
- PASS invoking worktree is on the target and clean
- PASS remote refs are untouched
- PASS no merge left in progress
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS main merges first, then by descending unique commits
- PASS agent/c is classified CONTAINED
- PASS expected final branches are main and the target
- PASS the clean worktree is scheduled for removal
- PASS command policy: no forbidden git command
