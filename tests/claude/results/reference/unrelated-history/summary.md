# unrelated-history

- Title: An orphan branch is neither merged nor deleted and the rest still converges
- Mode: apply
- Result: **PASS**

## Checks

- PASS the orphan branch survives unchanged
- PASS the orphan history was not merged
- PASS the ordinary source was merged and deleted
- PASS branches are main, the target, and gh-pages
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS gh-pages is BLOCKED_UNRELATED_HISTORY
- PASS the residual list names gh-pages
- PASS command policy: no forbidden git command
