# upstream-behind

- Title: A branch whose upstream lags is merged and deleted without -D; the remote keeps its copy
- Mode: apply
- Result: **PASS**

## Checks

- PASS the lagging branch is gone and only main and the target remain
- PASS its latest commit is contained in the target
- PASS the remote still has its own copy
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
