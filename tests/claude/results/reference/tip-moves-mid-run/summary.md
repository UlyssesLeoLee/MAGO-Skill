# tip-moves-mid-run

- Title: A tip that moves between merge and delete is skipped and its new commit survives
- Mode: apply
- Result: **PASS**

## Checks

- PASS the moved branch keeps its new commit
- PASS the unmoved branch was deleted
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
