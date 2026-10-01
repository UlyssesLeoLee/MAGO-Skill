# dependency-of-remaining-lane

- Title: A branch that a kept lane tracks is merged but kept
- Mode: apply
- Result: **PASS**

## Checks

- PASS the dirty lane is kept
- PASS the branch it tracks is kept
- PASS both were merged
- PASS the lane's upstream still resolves
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
