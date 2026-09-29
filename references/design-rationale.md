# Design Rationale

The main `SKILL.md` is intentionally policy-oriented rather than tutorial-oriented. Agents load it on activation; detailed edge cases live in references so ordinary tasks spend less context.

## Public patterns combined

1. **Isolation before implementation** — Superpowers' worktree guidance detects existing isolation first, prefers harness-native isolation, and establishes a clean baseline before implementation.
2. **Traceable task decomposition** — CCPM connects specification/task context to parallel work and durable handoff state rather than relying on conversation memory.
3. **Workspace/session isolation** — Claude Squad uses separate agent sessions plus Git worktrees so parallel agents do not share a writable checkout.
4. **Role separation** — Ruflo distinguishes coordination, coding, review, and testing roles; this skill keeps those responsibilities separable without depending on Ruflo itself.
5. **Evidence over claims** — repository state and executed checks are authoritative.
6. **Progressive disclosure** — Agent Skills supports a small `SKILL.md` plus on-demand `references/` resources.
7. **Skill pressure testing** — Superpowers' skill-authoring guidance treats process skills like code: pressure-test failure modes, then close loopholes.

## Additional safeguards introduced here

### Rewrite freeze for dependency sources

A private branch is not automatically safe to rebase once another lane is based on its commit IDs. The skill therefore separates **private** from **rewrite-safe** and freezes dependency-source history unless dependents are coordinated.

### Integration freshness gate

Review and integration are separate moments. A lane or target branch can change after approval. The skill invalidates stale approval rather than assuming the earlier review still applies.

### Serialized integration

Multiple approved lanes can race on a protected branch. A single integration writer or merge queue creates a deterministic order and forces later lanes to re-check freshness.

### Repository policy controls history representation

The orchestrator decides whether to accept a whole lane, a subset, or nothing. It does not globally impose fast-forward, merge-commit, or squash-merge style; that remains repository policy.

## Source references

- Superpowers: https://github.com/obra/superpowers
- CCPM: https://github.com/automazeio/ccpm
- Claude Squad: https://github.com/smtg-ai/claude-squad
- Ruflo: https://github.com/ruvnet/ruflo
- Agent Skills specification: https://agentskills.io/specification

## Proactive repository reconnaissance (v3.2)

Repository-specific Git advice is unsafe when based only on conversation assumptions. v3.2 adds a non-destructive reconnaissance mode that inventories worktrees, local branches, upstream tracking, dirtiness, ancestry, ahead/behind state, and overlap before recommending operations.

The survey uses stable Git plumbing/porcelain intended for machine consumption where practical (`git worktree list --porcelain`, `git for-each-ref`, `git rev-list --left-right --count`, and `git merge-base`). It deliberately separates local read-only observation from remote refresh: fetching changes remote-tracking refs and is therefore performed only when current remote truth materially affects the decision and the environment permits it.

The advice model distinguishes **observed**, **recorded**, **inferred**, and **unknown** facts so an agent does not invent branch ownership or semantic dependencies from topology alone.
