# upstream-of-kept

- Title: A branch that a kept branch tracks is merged but kept
- Mode: apply
- Result: **PASS**

## Checks

- PASS the tracked branch is kept
- PASS its content was merged
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
