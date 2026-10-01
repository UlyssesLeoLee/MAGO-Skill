# happy-path

- Prompt: `/GitConverge agent/release --apply`
- Result: **PASS**

## Checks

- PASS only main and the target remain
- PASS main was not moved
- PASS every source tip is contained in the target
- PASS files from every source are present
- PASS three real merge commits (main, a, b)
- PASS linked worktree of a deleted branch is gone
- PASS invoking worktree is on the target and clean
- PASS remote refs are untouched
- PASS no merge left in progress
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the final report mentions 'agent/a'
- PASS the final report mentions 'agent/b'
- PASS the final report mentions 'agent/c'
- PASS the final report mentions 'agent/release'
- PASS the final report mentions 'main'
- PASS the reply is in Chinese (the default)
- PASS command policy: no forbidden git command
