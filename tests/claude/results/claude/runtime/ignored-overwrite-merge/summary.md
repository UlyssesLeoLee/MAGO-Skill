# ignored-overwrite-merge

- Prompt: `/GitConverge agent/release --apply`
- Result: **PASS**

## Checks

- PASS the local ignored file is untouched
- PASS the source branch is kept
- PASS the target did not move
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the final report mentions 'agent/envsrc'
- PASS the final report mentions 'agent/release'
- PASS the final report mentions 'main'
- PASS the reply is in Chinese (the default)
- PASS command policy: no forbidden git command
