# Multi-Agent Git Orchestrator Skills

> **让多个 AI Agent 安全地并行开发同一个 Git 仓库。**

`Multi-Agent Git Orchestrator` 是一个面向 Claude Code、Codex、Cursor、OpenCode 等 Coding Agent 的 Git Workflow Skill。

它会主动调查当前仓库的 **Branch / Worktree / Commit / Ahead-Behind / Dependency** 状态，并帮助 Agent 决定：

- 哪些任务可以并行
- 哪些 Worktree 可以复用
- 哪些 Branch 应该 Rebase / Merge
- 哪些 Commit 适合 Cherry-pick
- 哪些分支已经可以安全清理
- 如何避免多个 Agent 同时破坏 `main`
<img width="1254" height="1254" alt="MAGOS2" src="https://github.com/user-attachments/assets/4d450361-25b5-4d35-90d8-d5656bd496cb" />

---

## Why?

多 Agent 开发很容易变成：

```text
Agent A ─┐
Agent B ─┼── 同一个目录 ── 冲突 / 覆盖 / 历史混乱
Agent C ─┘
```

本 Skill 将其变成：

```mermaid
flowchart LR
    M["main"] --> A["Agent A<br/>Branch + Worktree"]
    M --> B["Agent B<br/>Branch + Worktree"]
    M --> C["Agent C<br/>Branch + Worktree"]

    A --> R["Review / Validation"]
    B --> R
    C --> R

    R --> Q["Merge Queue"]
    Q --> M2["main"]
```

核心原则：

> **One Agent Lane = One Branch + One Worktree**

---

## 核心能力

| 能力 | 说明 |
|---|---|
| Repository Recon | 主动调查 Branch / Worktree / HEAD / Dirty / Ahead-Behind |
| Dependency DAG | 判断 Agent 任务之间的依赖关系 |
| Worktree Isolation | 避免多个 Agent 修改同一个 Checkout |
| Rewrite Safety | 判断什么时候可以 Rebase，什么时候禁止重写历史 |
| Selective Integration | Merge / Squash / Cherry-pick 按实际情况选择 |
| Freshness Gate | 防止 Review 后 `main` 已变化却继续错误集成 |
| Merge Queue | 串行写入共享集成分支 |
| Safe Cleanup | 安全识别已完成 Branch / Worktree |
| Safe Rollback | 私有历史用 Reset，共享历史优先 Revert |

---

## 五个核心命令

### `/GitRecon`

查看整个仓库当前状态。

```text
/GitRecon
```

调查：

```text
Worktrees
Branches
HEAD
Dirty / Untracked
Ahead / Behind
Detached
Remote tracking
Merge candidates
Risk
```

默认 **只读**。

---

### `/GitAnalyze`

深入分析指定 Branch 或 Worktree。

```text
/GitAnalyze agent/auth
```

例如判断：

```text
agent/auth

Ahead:     3
Behind:    2
State:     DIVERGED
Depends:   agent/core
Rewrite:   FROZEN

Recommendation:
不要直接 rebase
建议同步 integration branch 后重新验证
```

---

### `/GitRecommend`

根据仓库真实状态给出下一步建议。

```text
/GitRecommend 下一步怎么安排 3 个 Agent
```

Agent 会先调查，再回答：

```text
Agent A → 可以继续并行
Agent B → 与 A 文件高度重叠，建议串行
Agent C → 依赖 A，等待 A 完成

agent/old-ui → cleanup candidate
agent/auth   → rewrite frozen
```

---

### `/GitIntegrate`

安全集成一个 Agent 的成果。

```text
/GitIntegrate agent/auth
```

流程：

```mermaid
flowchart TD
    A["Agent Lane"] --> B["Refresh"]
    B --> C["Validation"]
    C --> D["Review"]
    D --> E["Freshness Check"]
    E --> F{"接受范围"}
    F -->|"全部"| G["Merge / Squash"]
    F -->|"部分"| H["Cherry-pick"]
    G --> I["Validate main"]
    H --> I
```

不会因为 Agent 说一句 **“Done”** 就直接进入 `main`。

---

### `/GitCleanup`

寻找可安全清理的 Branch / Worktree。

```text
/GitCleanup
```

默认只显示：

```text
Cleanup Candidates
```

真正执行：

```text
/GitCleanup --apply
```

只有满足以下条件才允许进入清理候选：

```text
✓ 已完整集成
✓ Worktree clean
✓ 无活动 Owner
✓ 无下游依赖
✓ 无独有未保存成果
```

---

## 多 Agent 生命周期

```mermaid
stateDiagram-v2
    [*] --> PLANNED
    PLANNED --> ACTIVE
    ACTIVE --> READY
    READY --> APPROVED
    APPROVED --> INTEGRATING
    INTEGRATING --> INTEGRATED

    READY --> BLOCKED
    READY --> REJECTED
```

每条 Agent Lane 都记录：

```text
Task
Owner
Branch
Worktree
Base Branch
Base SHA
Current HEAD
Dependencies
Validation Evidence
Integration Decision
```

---

## Git 操作决策

```text
整个 Agent 成果都要
        ↓
      Merge

只要部分 Commit
        ↓
   Cherry-pick

Agent 私有分支落后 main
        ↓
  Rewrite-safe?
    ↓       ↓
   YES      NO
 Rebase    Merge target into lane

私有历史走错
        ↓
      Reset

已经进入共享历史后出错
        ↓
      Revert
```

---

## 安全原则

```text
Observe first.
Advise second.
Mutate only when needed.
```

本 Skill 默认禁止：

- 多个 Agent 同时修改同一个 Checkout
- 未调查仓库就给出具体 Branch / Worktree 建议
- 随意 Rebase 已被其他 Agent 依赖的 Branch
- 对共享历史执行 destructive reset
- 默认 Force Push
- 未检查依赖就 Cherry-pick
- Review 已过期仍然继续 Integration
- 仅因为 Branch 很旧就判断可以删除

---

## 安装

将目录放入支持 Agent Skills 的 Skills 路径：

```text
multi-agent-git-orchestrator/
├── SKILL.md
├── commands/                  # Claude Code command prompts
├── skills/                    # Codex / Hermes command adapters
└── references/
    ├── commands.md
    ├── reconnaissance.md
    ├── decision-matrix.md
    ├── handoff-and-state.md
    ├── design-rationale.md
    └── pressure-tests.md
```

Skill 可以通过语义自动触发。

### Claude Code：启用 Slash Command

Claude Code 只会为每个 Skill 注册**一个**以 Skill 名命名的斜杠命令，`/GitRecon` 等五个命令需要额外安装 `commands/` 下的命令文件：

```text
commands/
├── GitRecon.md
├── GitAnalyze.md
├── GitRecommend.md
├── GitIntegrate.md
└── GitCleanup.md
```

在本仓库根目录执行，复制到用户级命令目录（所有项目可用）；也可以复制到某个项目的 `.claude/commands/`（仅该项目可用）。注意不要放进 Skill 目录内部，那里的文件不会被识别为命令：

```bash
mkdir -p ~/.claude/commands && cp commands/Git*.md ~/.claude/commands/
```

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\commands"; Copy-Item commands\Git*.md "$HOME\.claude\commands\"
```

安装后**重新开启会话**，输入 `/Git` 即可看到五个命令。

也可以显式调用：

```text
/GitRecon
/GitAnalyze <branch>
/GitRecommend [goal]
/GitIntegrate <lane-or-branch>
/GitCleanup
```

五个命令的跨宿主名称和说明：

| 命令 | Claude Code | Hermes | Codex | 说明 |
|---|---|---|---|---|
| GitRecon | `/GitRecon` | `/git-recon` | `$git-recon` | 检查仓库 branch / worktree 状态并生成快照 |
| GitAnalyze | `/GitAnalyze` | `/git-analyze` | `$git-analyze` | 分析指定目标的差异、依赖和操作风险 |
| GitRecommend | `/GitRecommend` | `/git-recommend` | `$git-recommend` | 根据当前状态建议 Git 与多 Agent 下一步 |
| GitIntegrate | `/GitIntegrate` | `/git-integrate` | `$git-integrate` | 通过安全门禁后集成指定 lane 或 branch |
| GitCleanup | `/GitCleanup` | `/git-cleanup` | `$git-cleanup` | 默认预览可清理项；`--apply` 才允许删除 |

斜杠入口说明：

| 宿主 | 从 `/` 进入 | 前提条件 |
|---|---|---|
| Claude Code | 直接输入 `/GitRecon` 等五个命令 | `~/.claude/commands/Git*.md` 已安装（`sync_hosts.py --host claude`），并已新开会话 |
| Hermes | 直接输入 `/git-recon` 等五个命令 | 包已安装到 `<Hermes home>/skills/`，并已新开会话或执行 `/reload-skills` |
| Codex | 输入 `/skills`，打开 Skill 列表后选择 `git-*`；也可以直接输入 `$git-recon` | 包已安装到 `~/.agents/skills/MAGOS`（`sync_hosts.py --host codex`），并已重启 Codex |

Codex 的 `/` 菜单只包含内置命令（源码 `codex-rs/tui/src/bottom_pane/command_popup.rs` 中只有 `Builtin` 与 `ServiceTier` 两类条目），无法注册自定义的 `/git-*`。因此在 Codex 中，斜杠入口是内置的 `/skills`。

### 参数提示与帮助

Claude Code 会在命令补全中显示 `commands/` 文件里的 `argument-hint`，例如 `/GitAnalyze <branch|worktree> [--remote] [--help]`。Codex 的 Skill 列表和 Hermes 的 Slash Command 说明会尽量带上简短用法；选中后可用 `--help` 查看完整参数说明和示例。`--help` 只显示说明，不检查或修改仓库。

```text
Claude Code: /GitIntegrate agent/auth --strategy squash
Hermes:      /git-integrate agent/auth --strategy squash
Codex:       $git-integrate agent/auth --strategy squash

Claude help: /GitIntegrate --help
Hermes help: /git-integrate --help
Codex help:  $git-integrate --help
```

运行源码契约检查：`python -X utf8 tests/codex/contracts/run_contract_cases.py`。每个用例的输入和结果保存在 `tests/codex/contracts/cases/<group>/<case>/evidence/`。这些检查不启动 AI 宿主；其中 `package/install-layout` 会把 Codex 与 Hermes 包安装到临时 home，确认适配层引用的每个文件都存在，并按两个宿主的发现规则（复刻版）确认每个 Skill 只被发现一次。

### Codex / Hermes 的包结构

Codex 和 Hermes 都安装同一个宿主中立的包，目录结构必须与仓库一致，`skills/git-*/SKILL.md` 才能通过 `../../SKILL.md`、`../../references/*.md` 找到共享规则：

```text
MAGOS/                       # Codex 包根；Hermes 使用 multi-agent-git-orchestrator/
├── SKILL.md                 # 根 Skill：multi-agent-git-orchestrator（语义自动触发）
├── references/*.md          # 全部参考文档
└── skills/git-*/            # 五个命令适配层
    ├── SKILL.md
    └── agents/openai.yaml   # Codex：显示说明 + allow_implicit_invocation: false
```

`commands/` 只供 Claude Code 使用，Codex / Hermes 包中不需要。推荐用同步脚本安装或更新（`--create-roots` 会创建缺失的安装根目录；脚本从不删除文件）：

```bash
python -X utf8 scripts/sync_hosts.py --host codex --host hermes --apply --create-roots
python -X utf8 scripts/sync_hosts.py --host codex --host hermes --verify
```

### Codex：启用命令 Skill

Codex 的自定义入口是 Skill 选择器（`$`），不是任意命名的 `/Git...` Slash Command。Codex 递归扫描 Skill 根目录，因此会同时加载根 Skill 和 `skills/` 下的五个命令 Skill；`agents/openai.yaml` 中的简短说明会显示在 Skill 列表里。五个命令 Skill 都设置了 `policy.allow_implicit_invocation: false`，只在显式选择时运行，语义自动触发由根 Skill 负责。

用户级安装位置是 `~/.agents/skills/MAGOS`。已经安装在旧位置 `$CODEX_HOME/skills/MAGOS`（默认 `~/.codex/skills/MAGOS`）的，同步脚本会继续更新旧位置；两个位置不要同时保留，否则 Codex 会看到重复的 Skill。手动安装（Windows PowerShell）：

```powershell
$codexPackage = Join-Path $HOME ".agents\skills\MAGOS"
New-Item -ItemType Directory -Force $codexPackage | Out-Null
Copy-Item -Path .\SKILL.md, .\references, .\skills -Destination $codexPackage -Recurse -Force
```

macOS / Linux：

```bash
mkdir -p "$HOME/.agents/skills/MAGOS"
cp -R SKILL.md references skills "$HOME/.agents/skills/MAGOS/"
```

重新启动 Codex 后，输入 `$` 选择命令 Skill，或直接调用 `$git-recon`、`$git-analyze`、`$git-recommend`、`$git-integrate`、`$git-cleanup`。`/skills` 可打开 Skill 浏览入口。参数写在 Skill 名后面，例如 `$git-analyze agent/auth --remote`；加 `--help` 可查看完整参数说明。

### Hermes：启用 Slash Skill

Hermes 会把已安装的每个 Skill 自动注册成一个 Slash Command（名称取自 frontmatter 的 `name`），并将 `description` 用作命令说明。安装后会出现 `/multi-agent-git-orchestrator` 和五个 `/git-*` 命令。

Hermes 的 home 目录依次取 `HERMES_HOME`、Windows 上的 `%LOCALAPPDATA%\hermes`、其他系统上的 `~/.hermes`，Skill 放在其下的 `skills/`。同步脚本按同样规则定位。如果已有 `<Hermes home>/skills/MAGOS`（例如直接 `git clone` 的安装），脚本会沿用它；如果它是 git checkout，脚本会拒绝复制文件，请改用 git 更新。手动安装（Windows PowerShell）：

```powershell
$hermesHome = if ($env:HERMES_HOME) { $env:HERMES_HOME } else { Join-Path $env:LOCALAPPDATA "hermes" }
$hermesSkills = Join-Path $hermesHome "skills\multi-agent-git-orchestrator"
New-Item -ItemType Directory -Force $hermesSkills | Out-Null
Copy-Item -Path .\SKILL.md, .\references, .\skills -Destination $hermesSkills -Recurse -Force
```

macOS / Linux：

```bash
mkdir -p "${HERMES_HOME:-$HOME/.hermes}/skills/multi-agent-git-orchestrator"
cp -R SKILL.md references skills "${HERMES_HOME:-$HOME/.hermes}/skills/multi-agent-git-orchestrator/"
```

重新启动 Hermes 后，可运行 `hermes skills list` 查看各命令说明，并调用 `/git-recon`、`/git-analyze`、`/git-recommend`、`/git-integrate` 或 `/git-cleanup`。参数直接跟在命令后面，例如 `/git-analyze main --remote`，也可用 `/git-analyze --help` 查看完整说明。Hermes 的 Skill 查看工具不接受含 `..` 的路径，适配层会改用 `[Skill directory: ...]` 给出的绝对路径读取共享文件。Hermes 没有按 Skill 关闭自动调用的开关，因此 `/git-integrate` 与 `/git-cleanup` 在适配层中规定：未经用户显式调用时不写入仓库。

如果宿主不支持自定义 Slash Command，也可以直接输入：

```text
GitRecon
GitAnalyze agent/auth
GitRecommend
```

---

## 适用场景

特别适合：

- Claude Code / Codex / Cursor 多 Agent 开发
- Git Worktree 并行开发
- AI 自动任务拆分
- 大量 Agent Branch 管理
- Human-in-the-loop Review
- Agent Worktree 可视化
- 自动 Merge Queue
- AI 生成代码的选择性集成

---

## Philosophy

Git 不只是版本管理工具。

在多 Agent 软件工程中，它还可以成为：

```text
Isolation Layer
+
Dependency Graph
+
Review Boundary
+
Integration Protocol
+
Rollback System
```

**让 Agent 可以大胆开发，让主分支保持可控。**

---

## License

Apache-2.0
