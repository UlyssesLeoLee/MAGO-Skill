# ordering-and-containment

- Title: Larger sources merge first so a contained source needs no second merge
- Mode: apply
- Result: **PASS**

## Checks

- PASS only main and the target remain
- PASS three merges: big (which carries mid), t1, t2
- PASS invariant: main did not move
- PASS invariant: tags unchanged
- PASS invariant: remote unchanged
- PASS invariant: remote-tracking refs unchanged
- PASS invariant: no merge left in progress
- PASS order is big, then the 2-commit tie by name, then mid
- PASS command policy: no forbidden git command
