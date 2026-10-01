# validation-fails

- Title: A failing post-merge check keeps the merges and deletes nothing
- Mode: apply
- Result: **PASS**

## Checks

- PASS the merge is kept
- PASS no branch was deleted
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
