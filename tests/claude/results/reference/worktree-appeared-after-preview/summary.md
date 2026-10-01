# worktree-appeared-after-preview

- Title: A worktree added after the preview keeps its branch
- Mode: apply
- Result: **PASS**

## Checks

- PASS the branch is kept
- PASS its new worktree is kept
- PASS its previewed tip was still merged
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
