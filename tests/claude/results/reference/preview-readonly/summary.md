# preview-readonly

- Title: Without --apply nothing changes and the plan is reported
- Mode: preview
- Result: **PASS**

## Checks

- PASS preview changes no ref, worktree, or file
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS main merges first, then by descending unique commits
- PASS agent/c is classified CONTAINED
- PASS expected final branches are main and the target
- PASS the clean worktree is scheduled for removal
- PASS command policy: no forbidden git command and read-only preview
