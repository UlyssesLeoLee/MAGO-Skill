# target-tag-shadow

- Prompt: `/GitConverge agent/release --apply`
- Result: **FAIL**

## Checks

- PASS the source's commits reached the target branch
- PASS only main and the target remain
- PASS the tag is untouched
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- FAIL the plan is printed before the first write
- PASS command policy: no forbidden git command
