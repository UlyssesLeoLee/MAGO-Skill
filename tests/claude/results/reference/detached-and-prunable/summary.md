# detached-and-prunable

- Title: A detached worktree is left alone and a missing branch worktree is removed by path only
- Mode: apply
- Result: **PASS**

## Checks

- PASS the missing-directory branch was merged and deleted
- PASS the detached worktree entry is still listed
- PASS the detached commit still exists
- PASS the gone branch's worktree entry was removed
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
