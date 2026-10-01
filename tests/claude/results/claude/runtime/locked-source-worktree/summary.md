# locked-source-worktree

- Prompt: `/GitConverge agent/release --apply`
- Result: **PASS**

## Checks

- PASS the held branch is kept
- PASS its worktree directory is kept
- PASS its committed content was still merged
- PASS the other source was merged and deleted
- PASS branches are main, the target, and the held branch
- PASS the worktree is still locked
- PASS command policy: no forbidden git command
