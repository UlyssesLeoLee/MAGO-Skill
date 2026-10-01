# claude-session-worktree

- Title: A Claude Code session worktree under <repo>/.claude/worktrees is never removed
- Mode: apply
- Result: **PASS**

## Checks

- PASS the session branch is kept
- PASS the session worktree is kept
- PASS its committed content was merged
- PASS the ordinary source was merged and deleted
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
