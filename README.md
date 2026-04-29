# ai-dev

个人 AI 开发工作空间。把多个语言的 repo 平铺克隆到 `repos/` 下，
通过顶层 `Taskfile.yml` 从外部驱动各 repo 的命令，子 repo 保持零侵入。

## 目录结构

```
ai-dev/
├── README.md
├── repos.yaml          # 子 repo 清单（事实之源）
├── Taskfile.yml        # 顶层 task 入口
├── taskfiles/          # 每个子 repo 的命令定义
│   └── <name>.yml
├── repos/              # 子 repo 平铺克隆（gitignored）
│   └── <name>/
└── .gitignore
```

## 命令约定

```bash
task                # 列出所有可用任务
task <name>:<cmd>   # 在 repos/<name>/ 下执行该 repo 的 <cmd>
```

例：`task zeus:test` → 在 `repos/zeus/` 下跑 zeus 的 test 命令。

## 添加新子 repo

1. **Clone 到 `repos/<name>`**
   ```bash
   git clone <url> repos/<name>
   ```

2. **新建 `taskfiles/<name>.yml`**，写入该 repo 的命令：
   ```yaml
   version: '3'
   tasks:
     test:
       cmds: ['<test 命令>']
     lint:
       cmds: ['<lint 命令>']
   ```

3. **在顶层 `Taskfile.yml` 加 `includes.<name>` 块**：
   ```yaml
   includes:
     <name>:
       taskfile: ./taskfiles/<name>.yml
       dir: ./repos/<name>
   ```

4. **在 `repos.yaml` 追加一条记录**：
   ```yaml
   - name: <name>
     path: <name>
     url: <git url>
     default_branch: <主分支>
     language: [<lang>]
   ```

## 依赖

- [go-task/task](https://taskfile.dev) ≥ 3.x
