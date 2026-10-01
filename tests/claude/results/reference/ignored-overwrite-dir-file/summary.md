# ignored-overwrite-dir-file

- Title: A source file named like an ignored local directory stops the merge
- Mode: apply
- Result: **PASS**

## Checks

- PASS every ignored local file is intact
- PASS the source branch is kept
- PASS the target did not move
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the stop reason is BLOCKED_IGNORED_OVERWRITE
- PASS command policy: no forbidden git command
