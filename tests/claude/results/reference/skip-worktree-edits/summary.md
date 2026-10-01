# skip-worktree-edits

- Title: Edits hidden by skip-worktree keep the worktree and branch
- Mode: apply
- Result: **PASS**

## Checks

- PASS the hidden edit survives
- PASS the branch is kept
- PASS its committed content was merged
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
