# ignored-files-discard

- Title: --discard-ignored removes the worktree and its ignored files
- Mode: apply
- Result: **PASS**

## Checks

- PASS only main and the target remain
- PASS the worktree directory is gone
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
