# submodule-worktree

- Title: A worktree with an initialized submodule is kept because git refuses to remove it
- Mode: apply
- Result: **PASS**

## Checks

- PASS the branch is kept
- PASS the worktree is kept
- PASS its committed content was merged
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
