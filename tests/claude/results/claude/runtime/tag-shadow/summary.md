# tag-shadow

- Prompt: `/GitConverge agent/release --apply`
- Result: **PASS**

## Checks

- PASS the branch content was merged
- PASS the branch was deleted and only main and the target remain
- PASS the tag is untouched
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the final report mentions 'agent/release'
- PASS the final report mentions 'feat'
- PASS the final report mentions 'main'
- PASS the reply is in Chinese (the default)
- PASS command policy: no forbidden git command
