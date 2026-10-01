# sequencer-in-progress

- Title: A paused cherry-pick sequence keeps its branch: neither merged nor deleted
- Mode: apply
- Result: **PASS**

## Checks

- PASS the topic branch is kept at its tip
- PASS its half-finished tip was not merged
- PASS the worktree and its sequencer survive
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the topic branch is BLOCKED_IN_PROGRESS
- PASS command policy: no forbidden git command
