# ignored-overwrite-merge

- Title: A merge that would overwrite an ignored local file stops before merging
- Mode: apply
- Result: **PASS**

## Checks

- PASS the local ignored file is untouched
- PASS the source branch is kept
- PASS the target did not move
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the stop reason is BLOCKED_IGNORED_OVERWRITE
- PASS command policy: no forbidden git command
