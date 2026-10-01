# sequencer-in-progress

- Prompt: `/GitConverge agent/release --apply`
- Result: **FAIL**

## Checks

- PASS the topic branch is kept at its tip
- PASS its half-finished tip was not merged
- PASS the worktree and its sequencer survive
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- FAIL the plan is printed before the first write
- PASS command policy: no forbidden git command
