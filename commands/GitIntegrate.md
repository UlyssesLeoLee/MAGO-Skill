---
description: 安全集成指定 Agent Lane 或分支（先过 review / dependency / freshness 门禁）
argument-hint: "<lane|branch> [--strategy auto|merge|squash|cherry-pick]"
disable-model-invocation: true
---

Run the Multi-Agent Git Orchestrator command `/GitIntegrate $ARGUMENTS`.

1. Load the orchestrator skill with the Skill tool. Use whichever name the skill listing shows: `MAGO-Skill` (GitHub clone directory) or `multi-agent-git-orchestrator` (frontmatter name). If neither is listed, tell the user the skill is not installed, then continue read-only only: report observations, but do not mutate branches, worktrees, refs, or history.
2. Execute `/GitIntegrate` exactly as defined in the skill's **Explicit Command Interface** and `references/commands.md`.
   Arguments (may be empty): $ARGUMENTS
3. Inspect the current repository before giving any state-dependent advice.

Safety default (applies even if the skill fails to load): write intent, but only after review, dependency, freshness, protected-branch, and repository-policy gates pass. If any gate fails, stop and report the blocker. Never force-push or rewrite shared history. If no target is given, ask for one.
