# conflict-predicted

- Title: A source that clashes with the target tip itself is predicted and then stops the apply
- Mode: apply
- Result: **PASS**

## Checks

- PASS no branch was deleted
- PASS no merge is left in progress
- PASS the clashing source is not merged
- PASS the working tree is clean
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS merge-tree predicts the clash against the target tip
- PASS the clean source is predicted clean
- PASS the stop reason is MERGE_FAILED
- PASS command policy: no forbidden git command
