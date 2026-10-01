# rerun-after-interrupted-apply

- Title: A rerun in the same conversation finishes an interrupted apply
- Mode: apply
- Result: **PASS**

## Checks

- PASS only main and the target remain
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the first run stopped on the conflict
- PASS the rerun is not treated as a stale preview
- PASS command policy: no forbidden git command
