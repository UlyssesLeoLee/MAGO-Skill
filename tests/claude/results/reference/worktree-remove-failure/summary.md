# worktree-remove-failure

- Title: A worktree another process is using is not half-deleted, and its branch is kept
- Mode: apply
- Result: **PASS**

## Checks

- PASS the branch whose worktree could not be removed is kept
- PASS the unrelated source was deleted
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the skip names the failed worktree removal
- PASS command policy: no forbidden git command
