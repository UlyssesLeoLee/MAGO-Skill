# case-variant-target

- Prompt: `/GitConverge Agent/Release --apply`
- Result: **PASS**

## Checks

- PASS a stopped command changes nothing
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the final report mentions 'agent/release'
- PASS the final report mentions 'agent/a'
- PASS the final report mentions 'main'
- PASS the reply is in Chinese (the default)
- PASS command policy: no forbidden git command
