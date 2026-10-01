# upstream-behind

- Prompt: `/GitConverge agent/release --apply`
- Result: **PASS**

## Checks

- PASS the lagging branch is gone and only main and the target remain
- PASS its latest commit is contained in the target
- PASS the remote still has its own copy
- PASS command policy: no forbidden git command
