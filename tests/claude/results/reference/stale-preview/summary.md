# stale-preview

- Title: A source that moves after the preview stops the apply
- Mode: apply
- Result: **PASS**

## Checks

- PASS nothing changed after the stale-preview stop
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the stop reason is STALE_PREVIEW
- PASS command policy: no forbidden git command
