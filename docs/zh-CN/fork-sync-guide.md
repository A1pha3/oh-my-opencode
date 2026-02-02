# Fork 仓库同步指南与版本管理最佳实践

> **适用场景**：从 GitHub fork 的仓库需要同步上游（upstream）更新
>
> **目标读者**：使用 oh-my-opencode 或类似项目的开发者

---

## 目录

- [1. 理解 Fork 工作流](#1-理解-fork-工作流)
- [2. 配置远程仓库](#2-配置远程仓库)
- [3. 同步策略选择](#3-同步策略选择)
- [4. 推荐的同步流程](#4-推荐的同步流程)
- [5. 解决冲突](#5-解决冲突)
- [6. 推送到远程 Fork](#6-推送到远程-fork)
- [7. 最佳实践](#7-最佳实践)
- [8. 常见问题与解决方案](#8-常见问题与解决方案)

---

## 1. 理解 Fork 工作流

### 1.1 什么是 Fork？

Fork 是 GitHub 提供的仓库复制功能，允许你：

- 创建一个仓库的独立副本
- 完全控制该副本（可以自由修改）
- 保留与原始仓库的关联（upstream）

```
原始仓库 (code-yeongyu/oh-my-opencode)
        ↑
        │  upstream 远程
        │
你的 Fork (A1pha3/oh-my-opencode)
        ↑
        │  origin 远程
        │
你的本地仓库 (~/projects/oh-my-opencode)
```

### 1.2 Fork 与 Clone 的区别

| 特性 | Fork | Clone |
|------|------|-------|
| 所有权 | 你拥有完整所有权 | 原始仓库所有 |
| 贡献方式 | 通过 Pull Request | 直接 push |
| 独立性 | 独立仓库，可自由实验 | 与原仓库强关联 |
| 同步需求 | 需要手动同步 | 通常不需要 |

### 1.3 为什么需要同步？

原始仓库（upstream）会持续更新：

- 修复 bug
- 添加新功能
- 更新文档
- 安全补丁

不同步意味着：

- ❌ 错过重要的安全更新
- ❌ 使用过时的 API
- ❌ 贡献时产生合并冲突
- ❌ 与社区脱节

---

## 2. 配置远程仓库

### 2.1 查看当前远程配置

```bash
git remote -v
```

**正常输出：**

```
origin  https://github.com/YOUR_USERNAME/oh-my-opencode.git (fetch)
origin  https://github.com/YOUR_USERNAME/oh-my-opencode.git (push)
```

### 2.2 添加 Upstream 远程

如果 upstream 不存在，添加它：

```bash
# 添加 upstream 远程
git remote add upstream https://github.com/code-yeongyu/oh-my-opencode.git

# 验证
git remote -v
```

**输出：**

```
origin    https://github.com/YOUR_USERNAME/oh-my-opencode.git (fetch)
origin    https://github.com/YOUR_USERNAME/oh-my-opencode.git (push)
upstream  https://github.com/code-yeongyu/oh-my-opencode.git (fetch)
upstream  https://github.com/code-yeongyu/oh-my-opencode.git (push)
```

### 2.3 更新 Upstream URL

如果 upstream URL 变更或初始设置错误：

```bash
# 方法 1：先删除再添加
git remote remove upstream
git remote add upstream https://github.com/code-yeongyu/oh-my-opencode.git

# 方法 2：直接修改 URL
git remote set-url upstream https://github.com/code-yeongyu/oh-my-opencode.git
```

---

## 3. 同步策略选择

### 3.1 策略对比

| 策略 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Merge** | 保留完整历史，产生合并提交 | 历史较乱，难以阅读记录何时 | 需要清晰同步 |
| **Rebase** | 历史整洁，线性流程 | 改写历史，危险操作 | 个人开发分支，追求整洁历史 |
| **Cherry-pick** | 选择性应用，灵活 | 需手动管理 | 只想要特定提交 |

### 3.2 Merge 详解

**原理**：将 upstream 的更改合并为一个合并提交

```bash
# 获取 upstream 更新
git fetch upstream

# 合并到当前分支
git merge upstream/dev
```

**结果：**

```
*   08889b8 - (upstream/dev) 最新 upstream 提交
*   abc448b - upstream 更新
*   |
|   *  d8afce9 - (HEAD -> dev) Merge branch 'upstream/dev'
|   |
*   08889b8 - upstream 提交
*   abc448b - upstream 提交
```

**优点：**
- ✅ 保留完整历史
- ✅ 清晰显示何时同步
- ✅ 不会丢失任何提交
- ✅ 更安全（不重写历史）

**缺点：**
- ❌ 产生大量合并提交
- ❌ 历史较乱
- ❌ 不利于代码审查

### 3.3 Rebase 详解

**原理**：将你的提交重新应用到 upstream 最新提交之上

```bash
# 获取 upstream 更新
git fetch upstream

# 变基到 upstream 最新
git rebase upstream/dev
```

**结果：**

```
*  d8afce9 - (HEAD -> dev) 你的最新提交
*  a52cd26 - 你的提交
*  08889b8 - (upstream/dev) 最新 upstream 提交
*  abc448b - upstream 更新
```

**优点：**
- ✅ 历史整洁，线性流程
- ✅ 容易追踪你的贡献
- ✅ 便于代码审查

**缺点：**
- ❌ **改写历史**，危险操作
- ❌ 已推送的提交不能再 rebase
- ❌ 可能产生复杂冲突

### 3.4 何时使用哪种策略？

| 场景 | 推荐策略 | 理由 |
|------|---------|------|
| 个人开发分支 | Rebase | 历史整洁 |
| 已推送到远程 | Merge | 不改写历史 |
| 需要保留合并记录 | Merge | 记录何时同步 |
| 做 PR 前 | Rebase | 整洁的审查历史 |
| 分支已经分享 | Merge | 避免影响他人 |

---

## 4. 推荐的同步流程

### 4.1 日常同步流程

```bash
# 1. 确保工作区干净
git status  # 确保没有未提交的更改

# 2. 获取 upstream 最新更新
git fetch upstream

# 3. 切换到要同步的分支
git checkout dev

# 4. 使用 rebase 同步（推荐）
git rebase upstream/dev

# 5. 如果有冲突，解决后继续
# git add <冲突文件>
# git rebase --continue

# 6. 推送到你的 fork（需要 force push）
git push --force-with-lease
```

### 4.2 完整工作流示例

```bash
# Step 1: 查看状态
$ git status
On branch dev
Your branch is up to date with 'origin/dev'.

nothing to commit, working tree clean

# Step 2: 获取 upstream 更新
$ git fetch upstream
remote: Enumerating objects: 45, done.
remote: Counting objects: 100% (45/45), done.
remote: Compressing objects: 100% (15/15), done.
remote: Total 23 (delta 8), reused 15 (delta 5)
Unpacking objects: 100 1/08889b8..d8afce9  23/23)
From https://github.com/code-yeongyu/oh-my-opencode
 * [new branch]      dev -> upstream/dev

# Step 3: 查看 upstream 有哪些新提交
$ git log --oneline upstream/dev -5
08889b8 @gburch has signed the CLA...
abc448b feat(config): disable todowrite...
523ef0d @YanzheL has signed the CLA...
134dc76 fix(task-tool): add task ID...
914a480 @code-yeongyu has signed the CLA...

# Step 4: 变基
$ git rebase upstream/dev
Successfully rebased and updated refs/heads/dev.

# Step 5: 推送到远程
$ git push --force-with-lease
Enumerating objects: 45, done.
Writing objects: 100% (45/45), 2.34 KiB | 2.34 MiB/s, done.
Total 45 (delta 8), reused 15 (delta 5)
To https://github.com/A1pha3/oh-my-opencode.git
   abc448b..08889b8  dev -> dev
```

### 4.3 安全检查

在同步前，检查以下项目：

```bash
# 1. 工作区是否干净？
git status

# 2. 是否有未推送的提交？
git log origin/dev..HEAD --oneline

# 3. upstream 有多少新提交？
git log HEAD..upstream/dev --oneline | wc -l

# 4. 是否有重要文件被修改？
git diff --stat upstream/dev
```

---

## 5. 解决冲突

### 5.1 冲突的产生原因

当你的修改与 upstream 的修改涉及同一文件同一位置时，会产生冲突。

```
你的修改：
<<<<<<< HEAD
const model = "claude-opus-4-5"
=======
const model = "anthropic/claude-opus-4-5"
>>>>>>> upstream/dev 的提交
```

### 5.2 解决冲突的步骤

```bash
# 1. 查看冲突文件
git diff --name-only --diff-filter=U

# 2. 查看冲突详情
git diff <冲突文件>

# 3. 编辑文件解决冲突
# 删除 <<<<<<<, =======, >>>>>>> 标记
# 保留正确的代码

# 4. 标记冲突已解决
git add <冲突文件>

# 5. 继续变基
git rebase --continue
```

### 5.3 解决策略

**策略 1：保留你的更改**

```bash
git checkout --ours <文件>
git add <文件>
git rebase --continue
```

**策略 2：保留 upstream 的更改**

```bash
git checkout --theirs <文件>
git add <文件>
git rebase --continue
```

**策略 3：手动解决**

```bash
# 编辑文件
vim <冲突文件>

# 解决后
git add <文件>
git rebase --continue
```

### 5.4 放弃解决

如果冲突太复杂，可以放弃：

```bash
git rebase --abort
```

---

## 6. 推送到远程 Fork

### 6.1 Force Push 的风险

**重要警告**：rebase 会改写历史，强制推送会覆盖远程仓库的历史。

```bash
# ✅ 安全的方式：force-with-lease
git push --force-with-lease

# ❌ 危险的方式：可能覆盖他人的工作
git push --force
```

### 6.2 Force With Lease vs Force

| 命令 | 行为 | 安全性 |
|------|------|--------|
| `git push` | 正常推送 | ✅ 安全 |
| `git push --force` | 强制覆盖远程 | ❌ 危险 |
| `git push --force-with-lease` | 检查远程变化后强制推送 | ⚠️ 较安全 |

### 6.3 检查推送影响

```bash
# 查看本地与远程的差异
git log origin/dev..HEAD --oneline

# 如果输出为空，说明没有新提交可以推送
# 如果有输出，说明会覆盖远程的提交
```

### 6.4 处理远程分支已更新

如果远程分支在你工作期间有新提交：

```bash
# 场景：你 fetch 后，远程有了新提交

# 方法 1：先 pull 再 push
git pull --rebase origin dev
git push origin dev

# 方法 2：强制推送（不推荐，会覆盖他人工作）
# 只有在确认远程提交可以丢弃时才使用
git push --force-with-lease
```

---

## 7. 最佳实践

### 7.1 同步频率

| 场景 | 推荐频率 |
|------|---------|
| 活跃开发的项目 | 每天或每次开发前 |
| 稳定项目 | 每周 |
| 低活跃项目 | 每月或每次有发布时 |

### 7.2 工作区管理

**同步前：**

```bash
# 1. 提交或暂存你的更改
git add .
git commit -m "WIP: 保存工作进度"

# 或者 stash
git stash
```

**同步后：**

```bash
# 恢复 stash
git stash pop

# 或者恢复提交
git reset --soft HEAD~1
git reset
```

### 7.3 分支策略

**推荐分支结构：**

```
main/stable     # 稳定版本，与 upstream/main 同步
dev             # 开发分支，与 upstream/dev 同步
feature/xxx     # 功能分支，基于 dev
```

**同步各分支：**

```bash
# 同步 dev 分支（最常用）
git checkout dev
git fetch upstream
git rebase upstream/dev
git push --force-with-lease

# 同步 main 分支（定期）
git checkout main
git fetch upstream
git rebase upstream/main
git push --force-with-lease
```

### 7.4 处理自己的贡献

**场景：你想同时保留自己的修改和 upstream 更新**

```bash
# 方法 1：rebase（推荐）
git fetch upstream
git rebase upstream/dev

# 你的提交会保留在 upstream 最新之上
```

**场景：你fork时的版本与upstream差异很大**

```bash
# 方法 2：使用 merge
git fetch upstream
git merge upstream/dev

# 会产生合并提交，但保留完整历史
```

### 7.5 测试同步后的代码

同步后务必测试：

```bash
# 1. 运行类型检查
bun run typecheck

# 2. 运行测试
bun test

# 3. 尝试构建
bun run build

# 4. 如果有 lint，运行 lint
bun run lint
```

### 7.6 记录同步历史

在同步时添加注释：

```bash
git fetch upstream
git rebase upstream/dev

# 如果有合并，添加日志
git log --oneline -1
# 记录：Sync with upstream @ $(date)
```

---

## 8. 常见问题与解决方案

### Q后中文1: 同步文档丢失？

**问题**：rebase 时使用 `--strategy=ours` 导致提交被丢弃。

**解决方案**：

```bash
# 1. 查看 reflog 找到丢弃的提交
git reflog | grep -E "docs.*zh-CN"

# 2. 恢复提交
git cherry-pick <commit-hash>

# 3. 如果有冲突，解决后继续
git add <冲突文件>
git cherry-pick --continue
```

**预防措施**：

- 避免使用 `--strategy=ours` 或 `--strategy=theirs`
- 优先解决冲突，而不是跳过
- 同步前备份重要分支

### Q2: "Your branch and 'origin/dev' have diverged"

**问题**：本地和远程分支有不同的提交。

```
On branch dev
Your branch and 'origin/dev' have diverged,
and have 44 and 8 different commits each, respectively.
```

**原因**：
- 本地有 44 个提交
- 远程有 8 个提交（可能是之前 force push 的）
- 两者没有共同的祖先

**解决方案**：

```bash
# 选项 1：强制推送本地版本（会覆盖远程）
git push --force-with-lease

# 选项 2：先 pull 远程版本，再手动合并
git pull --rebase origin dev
# 解决冲突
git push origin dev
```

**预防**：

- 不要在共享分支上使用 rebase
- 同步前先 push 或 stash

### Q3: "cannot rebase onto unconnected history"

**问题**：尝试 rebase 到一个不存在的提交。

```bash
git rebase upstream/dev
fatal: git rebase: cannot rebase onto unconnected history
```

**原因**：upstream 分支不存在或 URL 错误。

**解决方案**：

```bash
# 检查 remote 配置
git remote -v

# 重新添加 upstream
git remote remove upstream
git remote add upstream https://github.com/code-yeongyu/oh-my-opencode.git

# 重新 fetch
git fetch upstream
```

### Q4: 冲突太多，想放弃同步

```bash
# 放弃当前的 rebase/merge
git rebase --abort
# 或
git merge --abort

# 工作区会恢复到同步前的状态
```

### Q5: 如何只同步特定提交？

```bash
# 获取 upstream
git fetch upstream

# 查看提交
git log upstream/dev --oneline

# 选择性 cherry-pick
git cherry-pick <commit-hash>
```

### Q6: 同步后代码报错

**可能原因**：
1. upstream 更改了 API
2. 依赖版本变更
3. 配置文件格式变化

**解决步骤**：

```bash
# 1. 查看变更
git diff upstream/dev --stat

# 2. 运行测试
bun test

# 3. 查看详细错误
bun run typecheck

# 4. 根据错误修复
```

### Q7: 如何撤销同步？

```bash
# 方法 1：使用 reflog
git reflog
git reset --hard HEAD@{<n>}  # n 是步骤数

# 方法 2：查看同步前的分支
git branch -vv | grep origin/dev
git reset --hard <之前的-commit-hash>
```

### Q8: 保持 fork 与上游完全一致

```bash
# 危险操作：重置 fork 到 upstream 完全一致
git fetch upstream
git checkout dev
git reset --hard upstream/dev
git push --force-with-lease

# 警告：这会删除所有本地和远程的提交
# 只有在确认不需要保留时才使用
```

---

## 快速参考卡片

### 日常同步命令

```bash
# 完整同步流程
git fetch upstream
git checkout dev
git rebase upstream/dev
# 解决冲突（如果有）
git push --force-with-lease
```

### 紧急情况

```bash
# 放弃同步
git rebase --abort

# 强制重置到 upstream
git fetch upstream
git reset --hard upstream/dev
git push --force-with-lease
```

### 检查命令

```bash
# 查看 upstream 最新提交
git log upstream/dev -3 --oneline

# 查看本地与 upstream 的差异
git log HEAD..upstream/dev --oneline

# 查看冲突文件
git diff --name-only --diff-filter=U
```

---

## 参考资源

- [Git 官方文档 - Rebase](https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E5%9F%BA%E7%A7%AF)
- [GitHub 官方指南 - Syncing a fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork)
- [Oh My OpenCode GitHub](https://github.com/code-yeongyu/oh-my-opencode)
