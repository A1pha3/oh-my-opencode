# 功能完整参考

> 📖 **本文档适合**：想了解 Oh My OpenCode 所有可用功能的开发者
>
> ⏱️ **预计阅读时间**：60 分钟
>
> ✅ **完成本章后你将能够**：
> - 了解所有 10 个专业代理
> - 掌握 32 个生命周期钩子
> - 熟悉 20+ 工具和命令
> - 知道如何配置和使用每个功能

---

## 目录

- [代理：你的 AI 团队](#代理你的ai团队)
- [技能：领域专业知识](#技能领域专业知识)
- [命令：斜杠工作流](#命令斜杠工作流)
- [钩子：生命周期自动化](#钩子生命周期自动化)
- [工具：代理能力](#工具代理能力)
- [MCP 服务器：外部集成](#mcp-服务器外部集成)
- [上下文注入：智能代码感知](#上下文注入智能代码感知)
- [Claude Code 兼容性](#claude-code-兼容性)
- [后台代理系统](#后台代理系统)
- [会话工具：历史管理](#会话工具历史管理)
- [交互式终端：Tmux 集成](#交互式终端tmux-集成)

---

## 代理：你的 AI 团队

Oh My OpenCode 提供 10 个专业 AI 代理，每个都有明确的专长、优化模型和工具权限。

### 核心代理

#### 1. Sisyphus（主协调器）

| 属性 | 值 |
|------|-----|
| **模型** | `anthropic/claude-opus-4-5` |
| **回退** | kimi-k2.5 → glm-4.7 → gpt-5.2-codex → gemini-3-pro |
| **角色** | 默认协调器。规划、委托、执行复杂任务 |
| **特点** | 激进并行执行、Todo 驱动的工作流、扩展思考（32k 预算） |

**能力：**
- 🎯 规划复杂任务
- 🤝 委托给专业代理
- 🔧 使用 LSP 和 AST-Grep 进行重构
- ⚡ 并行运行后台代理
- 📋 强制任务完成（Todo Continuation Enforcer）

**最佳使用场景：**
- 复杂的多步骤任务
- 需要多代理协作的功能
- 需要持续工作直到完成的任务

#### 2. Oracle（架构顾问）

| 属性 | 值 |
|------|-----|
| **模型** | `openai/gpt-5.2` |
| **回退** | gpt-5.2 → gemini-3-pro → claude-opus-4-5 |
| **角色** | 架构决策、代码审查、调试 |
| **特点** | 只读咨询、卓越逻辑推理和深度分析 |

**能力：**
- 🏗️ 系统架构设计
- 🔍 复杂 bug 调试
- 📊 性能优化建议
- ⚖️ 技术方案权衡
- 🔮 设计模式推荐

**工具权限：** 只读（不能写、编辑或委托）

**最佳使用场景：**
- 需要深度推理的架构决策
- 难以修复的复杂 bug
- 代码审查和重构建议
- 技术选型咨询

**调用方式：**
```
Ask @oracle to review this design and propose an architecture
请求 @oracle 审查这个设计并建议架构
```

#### 3. Librarian（文档研究员）

| 属性 | 值 |
|------|-----|
| **模型** | `zai-coding-plan/glm-4.7` |
| **回退** | glm-4.7-free → claude-sonnet-4-5 |
| **角色** | 多仓库分析、文档查找、开源实现示例 |
| **特点** | 深度代码库理解、基于证据的回答 |

**能力：**
- 📚 查找官方文档
- 🔍 搜索开源实现示例
- 🗺️ 理解多仓库代码结构
- 📊 分析代码库模式
- 💡 提供最佳实践参考

**工具权限：** 只读（不能写、编辑或委托）

**内置 MCP：**
- **context7**：官方文档查找
- **grep_app**：GitHub 代码搜索

**最佳使用场景：**
- 需要使用陌生框架/库
- 查找开源实现示例
- 理解复杂代码库
- 学习 API 用法

**调用方式：**
```
Ask @librarian how this is implemented - why does the behavior keep changing?
请求 @librarian 这个如何实现的 - 为什么行为一直在变？
```

#### 4. Explore（代码搜索）

| 属性 | 值 |
|------|-----|
| **模型** | `anthropic/claude-haiku-4-5` |
| **回退** | gpt-5-mini → gpt-5-nano |
| **角色** | 快速代码库探索和上下文 grep |
| **特点** | 高速、低成本、专注上下文搜索 |

**能力：**
- ⚡ 快速搜索代码库
- 🔍 识别代码模式
- 📂 查找文件和目录
- 🎯 定位特定功能实现

**工具权限：** 只读（不能写、编辑或委托）

**最佳使用场景：**
- 快速找到函数/类定义
- 理解代码库结构
- 定位相关文件
- 查找使用某个 API 的地方

**调用方式：**
```
Ask @explore for the policy on this feature
请求 @explore 查找这个功能的策略
```

#### 5. Multimodal Looker（视觉内容专家）

| 属性 | 值 |
|------|-----|
| **模型** | `google/gemini-3-flash` |
| **回退** | gpt-5.2 → glm-4.6v → kimi-k2.5 → claude-haiku-4-5 → gpt-5-nano |
| **角色** | 视觉内容专家。分析 PDF、图片、图表以提取信息 |
| **特点** | 快速、支持多模态输入 |

**能力：**
- 📄 分析 PDF 文档
- 🖼️ 提取图片中的信息
- 📊 理解图表和示意图
- 🔍 文本识别（OCR）

**工具权限：** 白名单（只能用 read、glob、grep）

**最佳使用场景：**
- 从图片中提取信息
- 分析 PDF 文档
- 理解技术图表
- 处理扫描文档

**调用方式：**
```
Ask @multimodal-looker to analyze this diagram
请求 @multimodal-looker 分析这个图表
```

### 规划代理

#### 6. Prometheus（规划师）

| 属性 | 值 |
|------|-----|
| **模型** | `anthropic/claude-opus-4-5` |
| **回退** | kimi-k2.5 → gpt-5.2 → gemini-3-pro |
| **角色** | 战略规划、需求采访、工作计划创建 |
| **约束** | **只读**。只能在 `.sisyphus/` 目录内创建/修改 markdown 文件 |
| **特点** | 不直接写代码，专注"如何做" |

**工作流程：**
1. 🎯 识别用户意图（重构 vs 新功能）
2. 🔍 通过 explore 和 librarian 研究代码库和文档
3. ❓ 采访用户以明确需求
4. 📝 在 `.sisyphus/drafts/` 中记录讨论
5. 📋 在 `.sisyphus/plans/` 中创建详细计划

**如何进入：** 按 **Tab** 键切换到 Prometheus 模式

**最佳使用场景：**
- 复杂或多天的项目
- 需要完整决策记录
- 涉及多个文件的重构
- 需要明确的验收标准

#### 7. Metis（规划顾问）

| 属性 | 值 |
|------|-----|
| **模型** | `anthropic/claude-opus-4-5` |
| **回退** | kimi-k2.5 → gpt-5.2 → gemini-3-pro |
| **角色** | 规划前分析和差距检测 |
| **特点** | 强制在计划创建前进行预分析 |

**能力：**
- 🔍 识别用户请求中的隐藏意图
- ⚠️ 防止 AI 过度工程
- 🎯 消除模糊性
- ✅ 确保完整的验收标准
- 🔮 预见边缘情况

**为什么需要 Metis：**

规划者有"ADHD 工作记忆"——它建立的连接从未显式记录。Metis 强制将隐式知识显式化。

**最佳使用场景：**
- 在 Prometheus 生成计划前
- 任何需要清晰需求分析的任务
- 防止范围蔓延

#### 8. Momus（计划审查者）

| 属性 | 值 |
|------|-----|
| **模型** | `openai/gpt-5.2` |
| **回退** | gpt-5.2 → claude-opus-4-5 → gemini-3-pro |
| **角色** | 高精度计划验证（高精度模式） |
| **触发** | 当用户请求"高精度"时激活 |

**审查标准：**

| 标准 | 要求 |
|-----|------|
| **清晰度** | 每个任务必须指定"在哪里"找到实现细节 |
| **可验证性** | 验收标准必须具体可测量 |
| **上下文** | 必须有足够上下文，猜测不超过 10% |
| **大局** | 目的、背景、工作流必须清晰 |

**Momus 循环：**

Momus 只在以下条件全部满足时说"OKAY"：
- ✅ 100% 的文件引用已验证
- ✅ ≥80% 的任务有清晰的参考来源
- ✅ ≥90% 的任务有具体的验收标准
- ✅ 零个任务需要关于业务逻辑的假设
- ✅ 零个关键红旗

如果被拒绝，Prometheus 修复问题并重新提交。**无最大重试限制。**

### 协调代理

#### 9. Atlas（协调器）

| 属性 | 值 |
|------|-----|
| **模型** | `anthropic/claude-sonnet-4-5` |
| **回退** | kimi-k2.5 → gpt-5.2 |
| **角色** | 执行和委托。读取计划、分配任务、验证结果 |
| **特点** | 累积学习、独立验证、持续工作 |

**能力：**
- 📋 读取和解析计划文件
- 🔧 任务分解和依赖分析
- 🤝 委托任务给专业代理
- ✅ 独立验证每个任务完成
- 🧠 累积学习并传递给后续代理
- 🔄 支持并行执行

**关键特征：**

1. **不直接写代码**：必须委托给 Junior 或其他代理
2. **信任但验证**：从不信任代理的自我报告
3. **持续工作**：不停止直到所有任务完成
4. **智能恢复**：通过 `boulder.json` 支持会话中断恢复

**与 Prometheus 配合使用：**
```bash
# 1. 按 Tab 进入 Prometheus 模式
# 2. 描述工作，生成计划
# 3. 输入以下命令执行
/start-work
```

---

## 技能：领域专业知识

### 内置技能

#### 1. Playwright（浏览器自动化）

| 属性 | 值 |
|------|-----|
| **触发** | 浏览器任务、测试、截图 |
| **描述** | 通过 Playwright MCP 实现浏览器自动化 |
| **强制使用** | 任何浏览器相关任务 |
| **MCP** | `@playwright/mcp` |

**能力：**
- 🌐 浏览和交互网页
- 📸 截图和 PDF
- 📝 填写表单和点击元素
- ⏳ 等待网络请求
- 🕷️ 网页爬取内容

**使用示例：**
```
/playwright Navigate to example.com and take a screenshot
/playwright 导航到 example.com 并截图
```

**最佳使用场景：**
- 验证实现的 UI 渲染
- E2E 测试编写
- 网页自动化任务
- 动态内容抓取

#### 2. Frontend UI/UX（前端设计师）

| 属性 | 值 |
|------|-----|
| **触发** | UI/UX 任务、样式设计 |
| **描述** | 转型设计师的开发者，即使没有设计稿也能制作精美 UI/UX |
| **特点** | 强调大胆的审美方向、独特的排版、协调的色调 |

**设计原则：**
- **设计流程**：目的、调性、约束、差异化
- **审美方向**：选择极端风格——野兽派、极繁主义、复古未来主义、奢华、俏皮
- **排版**：独特字体，避免通用（Inter、Roboto、Arial）
- **色彩**：协调的色调，避免 AI slop 的紫色底白
- **动画**：高影响力的交错揭示、滚动触发、惊喜的悬停状态
- **反模式**：通用字体、可预测布局、cookie-cutter 设计

**最佳使用场景：**
- UI 设计任务
- 视觉变更
- 动画效果
- 响应式布局

#### 3. Git Master

| 属性 | 值 |
|------|-----|
| **触发** | commit、rebase、squash、"who wrote"、"when was X added" |
| **描述** | MUST USE for ANY git operations。原子提交、依赖排序、风格检测 |
| **MCP** | 无（使用 git 命令） |

**核心原则：**

**多提交默认原则：**
```
3+ 文件 → 必须是 2+ 个提交
5+ 文件 → 必须是 3+ 个提交
10+ 文件 → 必须是 5+ 个提交
```

**三重专业化：**

1. **提交架构师（Commit Architect）**：
   - 原子提交（atomic commits）
   - 依赖顺序
   - 风格检测

2. **变基外科医生（Rebase Surgeon）**：
   - 历史重写
   - 冲突解决
   - 分支清理

3. **历史考古学家（History Archaeologist）**：
   - 查找特定变更的引入时间和位置

**自动风格检测：**
- 分析最近 30 个提交的语言（韩语/英语）和风格（语义/简单/简短）
- 自动匹配你仓库的提交约定

**使用示例：**
```
/git-master commit these changes
/git-master rebase onto main
/git-master who wrote this authentication code?
```

**最佳使用场景：**
- 任何 git 操作
- 提交多个文件
- 代码历史搜索
- 变基和压缩提交

### 技能配置

禁用内置技能：
```json
{
  "disabled_skills": ["playwright"]
}
```

加载自定义技能（从项目或用户目录）：
```json
{
  "skills": {
    "sources": [
      { "path": "./custom-skills", "recursive": true }
    ]
  }
}
```

---

## 命令：斜杠工作流

命令是斜杠触发的工作流，执行预定义的模板。

### 内置命令

| 命令 | 描述 |
|------|------|
| `/init-deep` | 初始化分层 AGENTS.md 知识库 |
| `/ralph-loop` | 开始自引用开发循环直到完成 |
| `/ulw-loop` | 开始 ultrawork 循环——以 ultrawork 模式持续 |
| `/cancel-ralph` | 取消活动的 Ralph Loop |
| `/refactor` | 智能重构，带 LSP、AST-grep、架构分析和 TDD 验证 |
| `/start-work` | 从 Prometheus 计划开始 Sisyphus 工作会话 |

### 命令详解

#### /init-deep

**目的**：在项目中生成分层 AGENTS.md 文件

**用法：**
```
/init-deep [--create-new] [--max-depth=N]
```

**创建的目录结构：**
```
project/
├── AGENTS.md              # 项目范围上下文
├── src/
│   ├── AGENTS.md          # src 特有上下文
│   └── components/
│       └── AGENTS.md      # 组件特有上下文
```

**工作原理**：代理在读取文件时自动注入这些上下文文件。

#### /ralph-loop

**目的**：自引用开发循环，持续工作直到任务完成

**用法：**
```
/ralph-loop "Build a REST API with authentication"
/ralph-loop "Refactor the payment module" --max-iterations=50
```

**行为：**
- 持续向目标工作
- 检测 `<promise>DONE</promise>` 知道何时完成
- 如果代理停止但未完成，自动继续
- 在完成、达到最大迭代（默认 100）或 `/cancel-ralph` 时结束

**配置：**
```json
{
  "ralph_loop": {
    "enabled": true,
    "default_max_iterations": 100
  }
}
```

#### /ulw-loop

**目的**：同 ralph-loop，但激活 ultrawork 模式

**特点：** 所有内容以最大强度运行——并行代理、后台任务、激进的探索。

#### /refactor

**目的**：带完整工具链的智能重构

**用法：**
```
/refactor <target> [--scope=<file\|module\|project>] [--strategy=<safe\|aggressive>]
```

**功能：**
- LSP 驱动的重命名和导航
- AST-grep 模式匹配
- 变更前架构分析
- 变更后 TDD 验证
- 代码图生成

#### /start-work

**目的**：从 Prometheus 生成的计划开始执行

**用法：**
```
/start-work [plan-name]
```

**工作原理：**
- 查找 `.sisyphus/plans/` 中的计划
- 使用 Atlas 协调器系统化执行计划中的任务

### 自定义命令

加载位置：
- `.opencode/command/*.md`（项目）
- `~/.config/opencode/command/*.md`（用户）
- `.claude/commands/*.md`（Claude Code 兼容）
- `~/.claude/commands/*.md`（Claude Code 用户）

---

## 钩子：生命周期自动化

钩子拦截并修改代理生命周期的关键点行为。

### 钩子事件

| 事件 | 何时 | 能力 |
|------|------|------|
| **PreToolUse** | 工具执行前 | 阻止、修改输入、注入上下文 |
| **PostToolUse** | 工具执行后 | 添加警告、修改输出、注入消息 |
| **UserPromptSubmit** | 用户提交提示时 | 阻止、注入消息、转换提示 |
| **Stop** | 会话空闲时 | 注入后续提示 |

### 内置钩子

#### 上下文和注入

| 钩子 | 事件 | 描述 |
|------|-------|------|
| **directory-agents-injector** | PostToolUse | 读取文件时自动注入 AGENTS.md。从文件到项目根遍历，收集所有 AGENTS.md 文件。**OpenCode 1.1.37+ 已弃用**——当原生 AGENTS.md 注入可用时自动禁用。 |
| **directory-readme-injector** | PostToolUse | 注入 README.md 以获取目录上下文 |
| **rules-injector** | PostToolUse | 当条件匹配时从 `.claude/rules/` 注入规则。支持 glob 和 alwaysApply |
| **compaction-context-injector** | Stop | 在会话压缩期间保留关键上下文 |

#### 生产力与控制

| 钩子 | 事件 | 描述 |
|------|-------|------|
| **keyword-detector** | UserPromptSubmit | 检测关键词并激活模式：`ultrawork`/`ulw`（最大性能）、`search`/`find`（并行探索）、`analyze`/`investigate`（深度分析） |
| **think-mode** | UserPromptSubmit | 自动检测扩展思考需求。捕获"think deeply"、"ultrathink"并调整模型设置 |
| **ralph-loop** | Stop | 管理自引用循环延续 |
| **start-work** | PostToolUse | 处理 /start-work 命令执行 |
| **auto-slash-command** | UserPromptSubmit | 自动从提示词执行斜杠命令 |

#### 质量与安全

| 钩子 | 事件 | 描述 |
|------|-------|------|
| **comment-checker** | PostToolUse | 提醒代理减少过度注释。智能忽略 BDD、指令、docstring |
| **thinking-block-validator** | PreToolUse | 验证思考块以防止 API 错误 |
| **empty-message-sanitizer** | PreToolUse | 防止来自空聊天消息的 API 错误 |
| **edit-error-recovery** | PostToolUse | 从编辑工具失败中恢复 |

#### 恢复与稳定性

| 钩子 | 事件 | 描述 |
|------|-------|------|
| **session-recovery** | Stop | 从会话错误中恢复——丢失的工具结果、思考块问题、空消息 |
| **anthropic-context-window-limit-recovery** | Stop | 优雅处理 Claude 上下文窗口限制 |
| **background-compaction** | Stop | 自动压缩达到 token 限制的会话 |

#### 截断与上下文管理

| 钩子 | 事件 | 描述 |
|------|-------|------|
| **grep-output-truncator** | PostToolUse | 基于上下文窗口动态截断 grep 输出。保留 50% 余量，上限 50k token |
| **tool-output-truncator** | PostToolUse | 截断来自 Grep、Glob、LSP、AST-grep 工具的输出 |

#### 通知与 UX

| 钩子 | 事件 | 描述 |
|------|-------|------|
| **auto-update-checker** | UserPromptSubmit | 检查新版本，显示启动 toast，包含版本和 Sisyphus 状态 |
| **background-notification** | Stop | 后台代理任务完成时通知 |
| **session-notification** | Stop | 代理空闲时 OS 通知。支持 macOS、Linux、Windows |
| **agent-usage-reminder** | PostToolUse | 提醒你利用专业代理获得更好结果 |

#### 任务管理

| 钩子 | 事件 | 描述 |
|------|-------|------|
| **task-resume-info** | PostToolUse | 提供任务恢复信息以实现连续性 |
| **delegate-task-retry** | PostToolUse | 重试失败的 delegate_task 调用 |

#### 集成

| 钩子 | 事件 | 描述 |
|------|-------|------|
| **claude-code-hooks** | All | 执行 Claude Code settings.json 中的钩子 |
| **atlas** | All | 主协调逻辑（771 行） |
| **interactive-bash-session** | PreToolUse | 管理 CLI 的交互式 tmux 会话 |
| **non-interactive-env** | PreToolUse | 处理非交互环境约束 |

#### 专用

| 钩子 | 事件 | 描述 |
|------|-------|------|
| **prometheus-md-only** | PostToolUse | 强制 Prometheus 规划器只输出 markdown |

### 禁用钩子

```json
{
  "disabled_hooks": [
    "comment-checker",
    "auto-update-checker",
    "startup-toast"
  ]
}
```

---

## 工具：代理能力

### LSP 工具（IDE 功能）

| 工具 | 描述 |
|------|------|
| **lsp_diagnostics** | 在构建前获取错误/警告 |
| **lsp_prepare_rename** | 验证重命名操作 |
| **lsp_rename** | 跨工作区重命名符号 |
| **lsp_goto_definition** | 跳转到符号定义 |
| **lsp_find_references** | 在整个工作区查找所有使用 |
| **lsp_symbols** | 获取文件大纲或工作区符号搜索 |

**使用示例：**
```typescript
// 检查错误
const diagnostics = await lsp_diagnostics({
  filePath: "src/app.tsx"
})

// 重命名符号
await lsp_rename({
  filePath: "src/components/User.tsx",
  line: 10,
  character: 15,
  newName: "userName"
})

// 查找定义
const definition = await lsp_goto_definition({
  filePath: "src/app.ts",
  line: 42,
  character: 8
})
```

### AST-Grep 工具

| 工具 | 描述 |
|------|------|
| **ast_grep_search** | AST 感知的代码模式搜索（25 种语言） |
| **ast_grep_replace** | AST 感知的代码替换 |

**支持的语言：**
- TypeScript/JavaScript、Python、Rust、Go、Java 等 25 种语言

**使用示例：**
```typescript
// 搜索所有 console.log 调用
const results = await ast_grep_search({
  pattern: "console.log($MSG)",
  lang: "typescript"
})

// 替换为 logger.info
await ast_grep_replace({
  pattern: "console.log($MSG)",
  rewrite: "logger.info($MSG)",
  lang: "typescript",
  dryRun: false
})
```

### 委托工具

| 工具 | 描述 |
|------|------|
| **call_omo_agent** | 生成 explore/librarian 代理。支持 `run_in_background` |
| **delegate_task** | 基于类别的任务委托。支持类别（visual、business-logic）或直接代理定位 |
| **background_output** | 检索后台任务结果 |
| **background_cancel** | 取消运行中的后台任务 |

**delegate_task 参数：**
```typescript
await delegate_task({
  category: "visual-engineering",  // 或 "ultrabrain"、"quick" 等
  load_skills: ["frontend-ui-ux"], // 加载的技能
  prompt: "...",  // 任务描述
  run_in_background: true,  // 后台运行
  session_id: "..." // 继续之前的会话
})
```

### 会话工具

| 工具 | 描述 |
|------|------|
| **session_list** | 列出所有 OpenCode 会话 |
| **session_read** | 从会话读取消息和历史 |
| **session_search** | 会话消息全文搜索 |
| **session_info** | 获取会话元数据和统计 |

**使用示例：**
```typescript
// 列出所有会话
const sessions = await session_list({
  limit: 20,
  from_date: "2026-01-01",
  to_date: "2026-01-31"
})

// 读取会话
const sessionData = await session_read({
  session_id: "ses_abc123",
  include_todos: true,
  include_transcript: true
})

// 搜索会话
const results = await session_search({
  query: "authentication",
  limit: 10
})
```

### 交互式终端工具

| 工具 | 描述 |
|------|------|
| **interactive_bash** | 基于 tmux 的终端，用于 TUI 应用（vim、htop、pudb）。直接传递 tmux 子命令，不带前缀。 |

**使用示例：**
```typescript
// 创建新会话
interactive_bash(tmux_command="new-session -d -s dev-app")

// 发送按键到会话
interactive_bash(tmux_command="send-keys -t dev-app 'vim main.py' Enter")

// 捕获窗格输出
interactive_bash(tmux_command="capture-pane -p -t dev-app")
```

---

## MCP 服务器：外部集成

### 内置 MCP

#### websearch（Exa AI）

**功能：** 由 [Exa AI](https://exa.ai) 提供的实时网络搜索

**使用场景：**
- 搜索最新技术新闻
- 查找教程和指南
- 研究竞争对手

#### context7

**功能：** 任何库/框架的官方文档查找

**使用场景：**
- 查找 API 文档
- 了解框架新功能
- 学习最佳实践

#### grep_app

**功能：** 通过 [grep.app](https://grep.app) 跨数百万公开 GitHub 仓库的超快代码搜索

**使用场景：**
- 查找开源实现示例
- 研究代码库模式
- 学习特定技术的使用方式

### 技能嵌入 MCP

技能可以携带自己的 MCP 服务器：

```yaml
---
description: Browser automation skill
mcp:
  playwright:
    command: npx
    args: ["@anthropic-ai/mcp-playwright"]
---
```

**skill_mcp 工具会自动发现并调用这些操作。**

### OAuth 启用的 MCP

技能可以定义 OAuth 保护的远程 MCP 服务器。完全符合 RFC 的 OAuth 2.1 支持（RFC 9728, 8414, 8707, 7591）。

**特性：**
- 🔐 自动发现：获取 `/.well-known/oauth-protected-resource` (RFC 9728)，回退到 `/.well-known/oauth-authorization-server` (RFC 8414)
- 🔑 动态客户端注册：支持 RFC 7591 的服务器自动注册（clientId 可选）
- 🔒 PKCE：所有流程强制使用
- 📊 资源指示符：根据 RFC 8707 从 MCP URL 自动生成
- 💾 Token 存储：持久化在 `~/.config/opencode/mcp-oauth.json` (chmod 0600)
- 🔄 自动刷新：401 时刷新 token；403 时通过 `WWW-Authenticate` 进行升级授权
- 🔌 动态端口：OAuth 回调服务器使用自动发现的可用端口

---

## 上下文注入：智能代码感知

### 目录 AGENTS.md

读取文件时自动注入 AGENTS.md。从文件目录遍历到项目根：

```
project/
├── AGENTS.md              # 第一个注入
├── src/
│   ├── AGENTS.md          # 第二个注入
│   └── components/
│       ├── AGENTS.md      # 第三个注入
│       └── Button.tsx     # 读取这个注入所有 3 个
```

### 条件规则

当条件匹配时从 `.claude/rules/` 注入规则：

```markdown
---
globs: ["*.ts", "src/**/*.js"]
description: "TypeScript/JavaScript 编码规则"
---
- 使用 PascalCase 命名接口
- 使用 camelCase 命名函数
```

**支持：**
- `.md` 和 `.mdc` 文件
- `globs` 字段用于模式匹配
- `alwaysApply: true` 用于无条件规则
- 从文件到项目根遍历，加上 `~/.claude/rules/`

---

## Claude Code 兼容性

完整兼容 Claude Code 配置。

### 配置加载器

| 类型 | 位置 |
|------|------|
| **命令** | `~/.claude/commands/`、`.claude/commands/` |
| **技能** | `~/.claude/skills/*/SKILL.md`、`.claude/skills/*/SKILL.md` |
| **代理** | `~/.claude/agents/*.md`、`.claude/agents/*.md` |
| **MCP** | `~/.claude/.mcp.json`、`.mcp.json`、`.claude/.mcp.json` |

MCP 配置支持环境变量展开：`${VAR}`。

### 数据存储

| 数据 | 位置 | 格式 |
|------|------|------|
| Todos | `~/.claude/todos/` | Claude Code 兼容 |
| Transcripts | `~/.claude/transcripts/` | JSONL |

### 兼容性开关

```json
{
  "claude_code": {
    "mcp": false,
    "commands": false,
    "skills": false,
    "agents": false,
    "hooks": false,
    "plugins": false
  }
}
```

---

## 后台代理系统

### 并行执行

运行后台代理并继续工作：

```
# 启动在后台
delegate_task(agent="explore", background=true, prompt="Find auth implementations")

# 继续工作...
# 系统在完成时通知

# 需要时检索结果
background_output(task_id="bg_abc123")
```

**使用场景：**
- 让 GPT 调试的同时 Claude 尝试不同方法
- Gemini 编写前端的同时 Claude 处理后端
- 触发大规模并行搜索，继续实现，准备就绪后使用结果

### Tmux 多代理可视化

启用 `tmux.enabled` 在单独的 tmux 窗格中查看后台代理：

```json
{
  "tmux": {
    "enabled": true,
    "layout": "main-vertical"
  }
}
```

**当在 tmux 内运行时：**
- 后台代理在新窗格中生成
- 实时观看多个代理工作
- 每个窗格显示代理实时输出
- 代理完成时自动清理

---

## 会话工具：历史管理

### 会话列表

列出所有会话并过滤：

```bash
session_list --limit=20 --from_date=2026-01-01
```

### 会话读取

读取会话消息和历史：

```bash
session_read --session_id=ses_abc123 --include_todos --include_transcript
```

### 会话搜索

跨会话消息全文搜索：

```bash
session_search --query="authentication" --limit=10
```

### 会话信息

获取会话元数据和统计：

```bash
session_info --session_id=ses_abc123
```

---

## 交互式终端：Tmux 集成

### 启用 Tmux 集成

```json
{
  "tmux": {
    "enabled": true,
    "layout": "main-vertical",
    "main_pane_size": 60,
    "main_pane_min_width": 120,
    "agent_pane_min_width": 40
  }
}
```

### 工作原理

1. OpenCode 必须在 tmux 会话中运行
2. 启用 `--port` 标志启用子代理窗格生成
3. 后台代理在新 tmux 窗格中生成
4. 窗格显示代理实时输出
5. 代理完成时窗格自动关闭

### 布局选项

| 布局 | 描述 |
|------|------|
| `main-vertical` | 主窗格在左，代理窗格在右侧堆叠（默认） |
| `main-horizontal` | 主窗格在顶，代理窗格在底部堆叠 |
| `tiled` | 所有窗格在等大小网格中 |
| `even-horizontal` | 所有窗格在水平行中 |
| `even-vertical` | 所有窗格在垂直堆栈中 |

---

## 总结

Oh My OpenCode 提供了一套完整的功能系统：

- **10 个专业代理**：涵盖规划、协调、执行、研究、UI 等所有领域
- **3 个内置技能**：浏览器自动化、前端设计、Git 管理
- **6 个内置命令**：深度知识库、自引用循环、智能重构
- **32 个生命周期钩子**：覆盖所有关键点
- **20+ 工具**：LSP、AST-Grep、委托、会话管理等

所有这些功能共同工作，创建一个强大、专业、可靠的 AI 开发环境。

---

## 📖 相关文档

- [架构原理深度解析](../architecture/core-principles.md) - 理解设计哲学
- [配置完整指南](../configuration/complete-guide.md) - 定制所有功能
- [编排系统详解](../orchestration/deep-dive.md) - 深入理解工作流
- [最佳实践](../best-practices/development.md) - 最高效地使用这些功能
