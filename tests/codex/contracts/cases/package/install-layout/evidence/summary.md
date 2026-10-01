# package/install-layout

- Skill: `package`
- Feature: Codex and Hermes installs contain every file the adapters reference, and a replica of each host's discovery rules finds every skill once
- Result: **PASS**

## Expected behavior

- sync_hosts.py installs the full package (SKILL.md, references/, skills/) for Codex and Hermes.
- Every ../../ reference in an adapter and every references/ link in SKILL.md resolves inside the installed tree.
- No adapter routes through commands/; all six adapters set policy.allow_implicit_invocation: false.
- Each skill name appears exactly once in the Codex and Hermes discovery replicas.

## Contract checks

- PASS `install:sync_hosts.py --apply --create-roots`
- PASS `install:roots stay inside the temporary home`
- PASS `install:codex relative references resolve`
- PASS `install:codex adapters do not route through commands/`
- PASS `install:codex adapters disable implicit invocation`
- PASS `install:codex discovery replica finds each skill once`
- PASS `install:hermes relative references resolve`
- PASS `install:hermes adapters do not route through commands/`
- PASS `install:hermes adapters disable implicit invocation`
- PASS `install:hermes discovery replica finds each skill once`

Evidence scope: source-contract check; no AI host CLI is invoked.
