# conflict-stops

- Prompt: `/GitConverge agent/release --apply`
- Result: **PASS**

## Checks

- PASS no branch was deleted
- PASS no merge is left in progress
- PASS the working tree is clean
- PASS the two conflicting sources are not both merged
- PASS main was not moved
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the final report mentions 'agent/ok'
- PASS the final report mentions 'agent/release'
- PASS the final report mentions 'agent/x1'
- PASS the final report mentions 'agent/x2'
- PASS the final report mentions 'main'
- PASS the reply is in Chinese (the default)
- PASS command policy: no forbidden git command
