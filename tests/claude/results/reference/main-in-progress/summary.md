# main-in-progress

- Title: main mid-merge in the main worktree is neither merged nor a crash
- Mode: apply
- Result: **PASS**

## Checks

- PASS the main worktree is still mid-merge
- PASS main's commit was not merged into the target
- PASS the ordinary source was merged and deleted
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS main is BLOCKED_IN_PROGRESS
- PASS the run did not stop
- PASS command policy: no forbidden git command
