# target-prunable-entry

- Title: A target held only by a missing-directory worktree entry is a gate
- Mode: apply
- Result: **PASS**

## Checks

- PASS a stopped command changes nothing
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the gate is TARGET_PRUNABLE_ENTRY
- PASS command policy: no forbidden git command
