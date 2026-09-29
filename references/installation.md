# 用户级安装同步与验收

从仓库根目录运行以下命令。首次运行会列出每个目标文件的状态和源文件、已安装文件的 SHA-256；不会写入文件。

```powershell
python -X utf8 scripts/sync_hosts.py
python -X utf8 scripts/sync_hosts.py --verify
python -X utf8 scripts/sync_hosts.py --apply
python -X utf8 scripts/sync_hosts.py --verify
```

Use `--host codex` to inspect, sync, or verify Codex alone. Repeat `--host` to select multiple hosts.

`--verify` 在所有文件匹配时返回 0，存在缺失或差异时返回 1。缺少安装根目录、仓库源文件，或目标路径不安全时返回 2。`--apply` 会先检查所有目标；预检查失败时不会写入任何文件。复制中断后可再次运行 `--verify` 查看状态，再重试 `--apply`。使用 `--json` 可保存机器可读的验收记录。

同步范围固定为：

| 目标 | 需要预先存在的目录 | 同步文件 |
| --- | --- | --- |
| Claude | `~/.claude/commands` | 仓库 `commands/Git*.md`，共 5 个 |
| Codex | `~/.codex/skills/MAGOS` | `references/commands.md`、五个 `commands/Git*.md`、五个 `skills/git-*/SKILL.md`、五个 `skills/git-*/agents/openai.yaml`，共 16 个 |
| Hermes | `~/.hermes/skills/multi-agent-git-orchestrator` | 与 Codex 相同的 16 个文件 |

这些目录应由相应宿主的正常安装流程先创建。脚本只更新表中的相对路径，创建这些路径所需的子目录；不会删除其他文件，也不会改动 Codex 或 Hermes 安装根目录中的 `SKILL.md`。文件已匹配时不会重写。`--apply` 采用同目录临时文件替换目标文件。

如需在隔离目录验证脚本，可指定 `--home PATH`。默认会检查三个安装根目录；限定宿主时只需预先创建所选宿主的安装根目录。例如：

```powershell
python -X utf8 scripts/sync_hosts.py --host codex --home C:\temp\magos-test-home --verify --json
```

`--verify` 校验磁盘上的安装内容。参数灰字提示由各宿主的命令或 skill 选择界面决定；更新安装文件后，可能需要重新载入宿主会话才能看到新的说明。界面效果仍应在对应宿主中单独检查。
