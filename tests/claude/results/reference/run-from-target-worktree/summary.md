# run-from-target-worktree

- Title: Running from the worktree that holds the target works and leaves main's worktree alone
- Mode: apply
- Result: **PASS**

## Checks

- PASS only main and the target remain
- PASS the main worktree still stands on main
- PASS the source was merged
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
