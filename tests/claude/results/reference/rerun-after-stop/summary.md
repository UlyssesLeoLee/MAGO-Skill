# rerun-after-stop

- Title: After the conflict is resolved by discarding the loser, a rerun finishes the job
- Mode: apply
- Result: **PASS**

## Checks

- PASS only main and the target remain after the rerun
- PASS x1 and ok are contained in the target
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS the first run stopped on the conflict
- PASS the rerun was not stopped
- PASS command policy: no forbidden git command
