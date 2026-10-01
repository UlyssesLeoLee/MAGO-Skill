# conflict-stops

- Title: A conflicting source aborts its merge, stops the command, and deletes nothing
- Mode: apply
- Result: **PASS**

## Checks

- PASS no branch was deleted
- PASS no merge is left in progress
- PASS the working tree is clean
- PASS the two conflicting sources are not both merged
- PASS main was not moved
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the stop reason is MERGE_FAILED
- PASS per-source merge-tree cannot see the x1/x2 clash (documented blind spot)
- PASS command policy: no forbidden git command
