# target-tag-shadow

- Title: A tag named like the target never stands in for the target branch
- Mode: apply
- Result: **PASS**

## Checks

- PASS the source's commits reached the target branch
- PASS only main and the target remain
- PASS the tag is untouched
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the source is MERGE, not CONTAINED
- PASS the collision with the target is reported
- PASS command policy: no forbidden git command
