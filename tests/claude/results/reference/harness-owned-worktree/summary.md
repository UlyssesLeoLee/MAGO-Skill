# harness-owned-worktree

- Title: A worktree under an agent-harness root is never removed
- Mode: apply
- Result: **PASS**

## Checks

- PASS the held branch is kept
- PASS its worktree directory is kept
- PASS its committed content was still merged
- PASS the other source was merged and deleted
- PASS branches are main, the target, and the held branch
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
