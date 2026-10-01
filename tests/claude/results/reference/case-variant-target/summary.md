# case-variant-target

- Title: A differently-cased target is rejected, even with --apply
- Mode: apply
- Result: **PASS**

## Checks

- PASS a stopped command changes nothing
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the gate is TARGET_CASE_MISMATCH and suggests the real name
- PASS command policy: no forbidden git command
