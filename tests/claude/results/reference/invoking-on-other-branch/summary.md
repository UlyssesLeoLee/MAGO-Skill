# invoking-on-other-branch

- Title: The invoking worktree moves to the target and its old branch is merged and deleted
- Mode: apply
- Result: **PASS**

## Checks

- PASS the invoking worktree is now on the target
- PASS only main and the target remain
- PASS the former current branch was merged
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
