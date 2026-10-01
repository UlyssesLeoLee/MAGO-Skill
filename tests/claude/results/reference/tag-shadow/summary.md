# tag-shadow

- Title: A tag named like a branch never stands in for the branch
- Mode: apply
- Result: **PASS**

## Checks

- PASS the branch content was merged
- PASS the branch was deleted and only main and the target remain
- PASS the tag is untouched
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the collision is reported
- PASS command policy: no forbidden git command
