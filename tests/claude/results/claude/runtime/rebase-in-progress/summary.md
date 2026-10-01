# rebase-in-progress

- Prompt: `/GitConverge agent/release --apply`
- Result: **FAIL**

## Checks

- PASS the topic branch tip is unchanged
- PASS its stale tip was not merged
- PASS the rebase is still in progress
- PASS the ordinary source was merged and deleted
- PASS branches are main, the target, and topic
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- FAIL the plan is printed before the first write
- PASS command policy: no forbidden git command
