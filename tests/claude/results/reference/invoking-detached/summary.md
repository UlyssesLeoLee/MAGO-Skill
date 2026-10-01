# invoking-detached

- Title: A detached invoking worktree is a gate
- Mode: apply
- Result: **PASS**

## Checks

- PASS a stopped command changes nothing
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
