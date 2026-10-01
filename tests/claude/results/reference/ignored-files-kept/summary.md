# ignored-files-kept

- Title: A worktree holding ignored files is kept unless --discard-ignored is given
- Mode: apply
- Result: **PASS**

## Checks

- PASS the branch is kept
- PASS the worktree and its ignored file are intact
- PASS its committed content was merged
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
