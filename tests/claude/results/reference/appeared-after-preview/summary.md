# appeared-after-preview

- Title: A branch created after the preview is left untouched
- Mode: apply
- Result: **PASS**

## Checks

- PASS the late branch still exists unmerged
- PASS the late branch was not merged
- PASS the previewed source was merged and deleted
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS command policy: no forbidden git command
