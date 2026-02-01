# Oh-My-OpenCode 功能特性

---

## 代理：您的 AI 团队

Oh-My-OpenCode 提供 10 个专业 AI 代理。每个都有独特的专业知识、优化的模型和工具权限。

### 核心代理

| 代理 | 模型 | 目的 |
|------|------|------|
| **Sisyphus** | `anthropic/claude-opus-4-5` | **默认编排器。** 使用专业子代理通过激进并行执行规划、委托和执行复杂任务。Todo 驱动的工作流，扩展思考（32k 预算）。回退：kimi-k2.5 → glm-4.7 → gpt-5.2-codex → gemini-3-pro。 |
| **oracle** | `openai/gpt-5.2` | 架构决策、代码审查、调试。只读咨询 - 出色的逻辑推理和深度分析。灵感来自 AmpCode。 |
| **Oracle** | `openai/gpt-5.2` | 架构决策、代码审查、调试。只读咨询 - 出色的逻辑推理和深度分析。灵感来自 AmpCode。 |
| **librarian** | `zai-coding-plan/glm-4.7` | 多仓库分析、文档查找、开源实现示例。深度代码库理解，基于证据的回答。回退：glm-4.7-free → claude-sonnet-4-5。 |
| **Librarian** | `zai-coding-plan/glm-4.7` | 多仓库分析、文档查找、开源实现示例。深度代码库理解，基于证据的回答。回退：glm-4.7-free → claude-sonnet-4-5。 |
| **explore** | `anthropic/claude-haiku-4-5` | 快速代码库探索和上下文感知 grep。回退：gpt-5-mini → gpt-5-nano。 |
| **multimodal-looker** | `google/gemini-3-flash` | 视觉内容专家。分析 PDF、图像、图表以提取信息。回退：gpt-5.2 → glm-4.6v → kimi-k2.5 → claude-haiku-4-5 → gpt-5-nano。 |

### 规划代理

| 代理 | 模型 | 目的 |
|------|------|------|
| **Prometheus** | `anthropic/claude-opus-4-5` | 具有采访模式的战略规划师。通过迭代提问创建详细的工作计划。回退：kimi-k2.5 → gpt-5.2 → gemini-3-pro。 |
| **Metis** | `anthropic/claude-opus-4-5` | 规划顾问 - 预先规划分析。识别隐藏的意图、歧义和 AI 失败点。回退：kimi-k2.5 → gpt-5.2 → gemini-3-pro。 |
| **Momus** | `openai/gpt-5.2` | 规划审查员 - 根据清晰度、可验证性和完整性标准验证计划。回退：gpt-5.2 → claude-opus-4-5 → gemini-3-pro。 |

### 调用代理

主代理自动调用这些，但您可以显式调用它们：

```
Ask @oracle to review this design and propose an architecture
Ask @librarian how this is implemented - why does the behavior keep changing?
Ask @explore for the policy on this feature
```

### 工具限制

| 代理 | 限制 |
|------|------|
| oracle | 只读：不能写、编辑或委托 |
| librarian | 不能写、编辑或委托 |
| explore | 不能写、编辑或委托 |
| multimodal-looker | 仅允许列表：读取、glob、grep |

### 后台代理

在后台运行代理并继续工作：

- 让 GPT 调试而 Claude 尝试不同的方法
- Gemini 写前端而 Claude 处理后端
- 发起大规模并行搜索，继续实现，准备好时使用结果

```
# 在后台启动
delegate_task(agent="explore", background=true, prompt="Find auth implementations")

# 继续工作...
# 系统在完成时通知

# 需要时检索结果
background_output(task_id="bg_abc123")
```

#### 使用 Tmux 的可视化多代理

启用 `tmux.enabled` 在单独的 tmux 窗格中查看后台代理：

```json
{
  "tmux": {
    "enabled": true,
    "layout": "main-vertical"
  }
}
```

在 tmux 内运行时：
- 后台代理在新窗格中生成
- 实时观看多个代理工作
- 每个窗格实时显示代理输出
- 代理完成时自动清理

有关完整配置选项，请参阅 [Tmux 集成](configurations.md#tmux-integration)。

在 `oh-my-opencode.json` 中自定义代理模型、提示和权限。请参阅[配置](configurations.md#agents)。

---

## 技能：专业知识

技能提供具有嵌入式 MCP 服务器和详细说明的专业工作流。

### 内置技能

| 技能 | 触发器 | 描述 |
|------|--------|------|
| **playwright** | 浏览器任务、测试、截图 | 通过 Playwright MCP 进行浏览器自动化。必须用于任何浏览器相关任务 - 验证、浏览、网页抓取、测试、截图。 |
| **frontend-ui-ux** | UI/UX 任务、样式 | 设计师转开发者的角色。即使没有设计稿也能制作出色的 UI/UX。强调大胆的美学方向、独特的排版、凝聚力的调色板。 |
| **git-master** | 提交、rebase、squash、blame | 必须用于任何 Git 操作。原子提交自动拆分、rebase/squash 工作流、历史搜索（blame、bisect、log -S）。 |

### 技能：浏览器自动化（playwright / agent-browser）

**触发**：任何浏览器相关请求

Oh-My-OpenCode 提供两种浏览器自动化提供商，可通过 `browser_automation_engine.provider` 配置：

#### 选项 1：Playwright MCP（默认）

默认提供商使用 Playwright MCP 服务器：

```yaml
mcp:
  playwright:
    command: npx
    args: ["@playwright/mcp@latest"]
```

**使用**：
```
/playwright Navigate to example.com and take a screenshot
```

#### 选项 2：Agent Browser CLI（Vercel）

使用 [Vercel 的 agent-browser CLI](https://github.com/vercel-labs/agent-browser) 的替代提供商：

```json
{
  "browser_automation_engine": {
    "provider": "agent-browser"
  }
}
```

**需要安装**：
```bash
bun add -g agent-browser
```

**使用**：
```
Use agent-browser to navigate to example.com and extract the main heading
```

#### 功能（两个提供商）

- 导航并与网页交互
- 截图和 PDF
- 填写表单并点击元素
- 等待网络请求
- 抓取内容

### 技能：frontend-ui-ux

**触发**：UI 设计任务、视觉更改

一位设计师转开发者，制作令人惊叹的界面：

- **设计流程**：目的、语气、约束、差异化
- **美学方向**：选择极端 - 野蛮主义、极繁主义、复古未来主义、奢华、俏皮
- **排版**：独特的字体，避免通用（Inter、Roboto、Arial）
- **颜色**：具有锐利点缀的凝聚调色板，避免紫底白 AI 垃圾
- **动效**：高冲击的交错揭示、滚动触发、令人惊讶的悬停状态
- **反模式**：通用字体、可预测的布局、千篇一律的设计

### 技能：git-master

**触发**：提交、rebase、squash、"谁写的"、"何时添加的"

一个技能，三种专业：

1. **提交架构师**：原子提交、依赖排序、风格检测
2. **Rebase 外科医生**：历史重写、冲突解决、分支清理
3. **历史考古学家**：查找特定更改何时/在哪里引入

**核心原则 - 默认多个提交**：
```
3+ 文件 -> 必须是 2+ 提交
5+ 文件 -> 必须是 3+ 提交
10+ 文件 -> 必须是 5+ 提交
```

**自动风格检测**：
- 分析最近 30 次提交的语言（韩语/英语）和风格（语义/普通/简短）
- 自动匹配您的仓库的提交约定

**使用**：
```
/git-master commit these changes
/git-master rebase onto main
/git-master who wrote this authentication code?
```

### 自定义技能

从以下位置加载自定义技能：
- `.opencode/skills/*/SKILL.md`（项目）
- `~/.config/opencode/skills/*/SKILL.md`（用户）
- `.claude/skills/*/SKILL.md`（Claude Code 兼容）
- `~/.claude/skills/*/SKILL.md`（Claude Code 用户）

通过配置中的 `disabled_skills: ["playwright"]` 禁用内置技能。

---

## 命令：斜杠工作流

命令是触发预定义模板执行的斜杠工作流。

### 内置命令

| 命令 | 描述 |
|------|------|
| `/init-deep` | 初始化分层 AGENTS.md 知识库 |
| `/ralph-loop` | 开始自引用开发循环直到完成 |
| `/ulw-loop` | 开始 ultrawork 循环 - 继续使用 ultrawork 模式 |
| `/cancel-ralph` | 取消活动的 Ralph Loop |
| `/refactor` | 智能重构，具有 LSP、AST-grep、架构分析和 TDD 验证 |
| `/start-work` | 从 Prometheus 计划开始 Sisyphus 工作会话 |

### 命令：/init-deep

**目的**：在整个项目中生成分层 AGENTS.md 文件

**使用**：
```
/init-deep [--create-new] [--max-depth=N]
```

创建代理自动读取的目录特定上下文文件：
```
project/
├── AGENTS.md              # 项目范围上下文
├── src/
│   ├── AGENTS.md          # src 特定上下文
│   └── components/
│       └── AGENTS.md      # 组件特定上下文
```

### 命令：/ralph-loop

**目的**：自引用开发循环，持续运行直到任务完成

**命名来源**：Anthropic 的 Ralph Wiggum 插件

**使用**：
```
/ralph-loop "Build a REST API with authentication"
/ralph-loop "Refactor the payment module" --max-iterations=50
```

**行为**：
- 代理持续朝着目标工作
- 检测 `<promise>DONE</promise>` 知道何时完成
- 如果代理在没有完成的情况下停止则自动继续
- 结束条件：检测到完成、达到最大迭代次数（默认 100）或 `/cancel-ralph`

**配置**：`{ "ralph_loop": { "enabled": true, "default_max_iterations": 100 } }`

### 命令：/ulw-loop

**目的**：与 ralph-loop 相同，但带有 ultrawork 模式

一切都以最大强度运行 - 并行代理、后台任务、积极探索。

### 命令：/refactor

**目的**：具有完整工具链的智能重构

**使用**：
```
/refactor <target> [--scope=<file|module|project>] [--strategy=<safe|aggressive>]
```

**功能**：
- LSP 支持的重命名和导航
- 用于模式匹配的 AST-grep
- 更改前的架构分析
- 更改后的 TDD 验证
- 代码图生成

### 命令：/start-work

**目的**：从 Prometheus 生成的计划开始执行

**使用**：
```
/start-work [plan-name]
```

使用 atlas 代理系统地执行计划的任务。

### 自定义命令

从以下位置加载自定义命令：
- `.opencode/command/*.md`（项目）
- `~/.config/opencode/command/*.md`（用户）
- `.claude/commands/*.md`（Claude Code 兼容）
- `~/.claude/commands/*.md`（Claude Code 用户）

---

## 钩子：生命周期自动化

钩子在代理生命周期的关键点拦截和修改行为。

### 钩子事件

| 事件 | 何时 | 可以 |
|------|------|------|
| **PreToolUse** | 工具执行前 | 阻止、修改输入、注入上下文 |
| **PostToolUse** | 工具执行后 | 添加警告、修改输出、注入消息 |
| **UserPromptSubmit** | 用户提交提示时 | 阻止、注入消息、转换提示 |
| **Stop** | 会话空闲时 | 注入后续提示 |

### 内置钩子

#### 上下文和注入

| 钩子 | 事件 | 描述 |
|------|------|------|
| **directory-agents-injector** | PostToolUse | 读取文件时自动注入 AGENTS.md。从文件到项目根目录，收集所有 AGENTS.md 文件。**对于 OpenCode 1.1.37+ 已弃用** - 当本地 AGENTS.md 注入可用时自动禁用。 |
| **directory-readme-injector** | PostToolUse | 自动注入 README.md 以获取目录上下文。 |
| **rules-injector** | PostToolUse | 当条件匹配时从 `.claude/rules/` 注入规则。支持 glob 和 alwaysApply。 |
| **compaction-context-injector** | Stop | 在会话压缩期间保留关键上下文。 |

#### 生产力和控制

| 钩子 | 事件 | 描述 |
|------|------|------|
| **keyword-detector** | UserPromptSubmit | 检测关键字并激活模式：`ultrawork`/`ulw`（最大性能）、`search`/`find`（并行探索）、`analyze`/`investigate`（深度分析）。 |
| **think-mode** | UserPromptSubmit | 自动检测扩展思考需求。捕获 "think deeply"、"ultrathink" 并调整模型设置。 |
| **ralph-loop** | Stop | 管理自引用循环继续。 |
| **start-work** | PostToolUse | 处理 /start-work 命令执行。 |
| **auto-slash-command** | UserPromptSubmit | 自动从提示执行斜杠命令。 |

#### 质量和安全

| 钩子 | 事件 | 描述 |
|------|------|------|
| **comment-checker** | PostToolUse | 提醒代理减少过多注释。智能忽略 BDD、指令、文档字符串。 |
| **thinking-block-validator** | PreToolUse | 验证思考块以防止 API 错误。 |
| **empty-message-sanitizer** | PreToolUse | 防止空聊天消息导致的 API 错误。 |
| **edit-error-recovery** | PostToolUse | 从编辑工具失败中恢复。 |

#### 恢复和稳定性

| 钩子 | 事件 | 描述 |
|------|------|------|
| **session-recovery** | Stop | 从会话错误恢复 - 缺少工具结果、思考块问题、空消息。 |
| **anthropic-context-window-limit-recovery** | Stop | 优雅地处理 Claude 上下文窗口限制。 |
| **background-compaction** | Stop | 自动压缩达到令牌限制的会话。 |

#### 截断和上下文管理

| 钩子 | 事件 | 描述 |
|------|------|------|
| **grep-output-truncator** | PostToolUse | 基于上下文窗口动态截断 grep 输出。保持 50% 余量，上限为 50k 令牌。 |
| **tool-output-truncator** | PostToolUse | 截断来自 Grep、Glob、LSP、AST-grep 工具的输出。 |

#### 通知和用户体验

| 钩子 | 事件 | 描述 |
|------|------|------|
| **auto-update-checker** | UserPromptSubmit | 检查新版本，显示带有版本和 Sisyphus 状态的启动提示。 |
| **background-notification** | Stop | 当后台代理任务完成时通知。 |
| **session-notification** | Stop | 代理空闲时的操作系统通知。在 macOS、Linux、Windows 上工作。 |
| **agent-usage-reminder** | PostToolUse | 提醒您利用专业代理以获得更好的结果。 |

#### 任务管理

| 钩子 | 事件 | 描述 |
|------|------|------|
| **task-resume-info** | PostToolUse | 为连续性提供任务恢复信息。 |
| **delegate-task-retry** | PostToolUse | 重试失败的 delegate_task 调用。 |

#### 集成

| 钩子 | 事件 | 描述 |
|------|------|------|
| **claude-code-hooks** | All | 从 Claude Code 的 settings.json 执行钩子。 |
| **atlas** | All | 主要编排逻辑（771 行）。 |
| **interactive-bash-session** | PreToolUse | 管理交互式 CLI 的 tmux 会话。 |
| **non-interactive-env** | PreToolUse | 处理非交互式环境约束。 |

#### 专业

| 钩子 | 事件 | 描述 |
|------|------|------|
| **prometheus-md-only** | PostToolUse | 为 Prometheus 规划器强制纯 markdown 输出。 |

### Claude Code 钩子集成

通过 Claude Code 的 `settings.json` 运行自定义脚本：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "eslint --fix $FILE" }]
      }
    ]
  }
}
```

**钩子位置**：
- `~/.claude/settings.json`（用户）
- `./.claude/settings.json`（项目）
- `./.claude/settings.local.json`（本地，git 忽略）

### 禁用钩子

在配置中禁用特定钩子：

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

### LSP 工具（代理的 IDE 功能）

| 工具 | 描述 |
|------|------|
| **lsp_diagnostics** | 在构建前获取错误/警告 |
| **lsp_prepare_rename** | 验证重命名操作 |
| **lsp_rename** | 重命名跨工作区的符号 |
| **lsp_goto_definition** | 跳转到符号定义 |
| **lsp_find_references** | 查找跨工作区的所有用法 |
| **lsp_symbols** | 获取文件大纲或工作区符号搜索 |

### AST-Grep 工具

| 工具 | 描述 |
|------|------|
| **ast_grep_search** | AST 感知代码模式搜索（25 种语言） |
| **ast_grep_replace** | AST 感知代码替换 |

### 委托工具

| 工具 | 描述 |
|------|------|
| **call_omo_agent** | 生成探索/Librarian 代理。支持 `run_in_background`。 |
| **delegate_task** | 基于分类的任务委托。支持分类（visual、business-logic）或直接代理定位。 |
| **background_output** | 检索后台任务结果 |
| **background_cancel** | 取消运行中的后台任务 |

### 会话工具

| 工具 | 描述 |
|------|------|
| **session_list** | 列出所有 OpenCode 会话 |
| **session_read** | 从会话读取消息和历史 |
| **session_search** | 跨会话消息的全文搜索 |
| **session_info** | 获取会话元数据和统计信息 |

### 交互式终端工具

| 工具 | 描述 |
|------|------|
| **interactive_bash** | 基于 Tmux 的终端，适用于 TUI 应用程序（vim、htop、pudb）。直接传递 tmux 子命令，无需前缀。 |

**使用示例**：
```bash
# 创建新会话
interactive_bash(tmux_command="new-session -d -s dev-app")

# 向会话发送按键
interactive_bash(tmux_command="send-keys -t dev-app 'vim main.py' Enter")

# 捕获窗格输出
interactive_bash(tmux_command="capture-pane -p -t dev-app")
```

**关键点**：
- 命令是 tmux 子命令（没有 `tmux` 前缀）
- 用于需要持久会话的交互式应用程序
- 一次性命令应该对常规 `Bash` 工具使用 `&`

---

## MCP：内置服务器

### websearch（Exa AI）

由 [Exa AI](https://exa.ai) 提供支持的实时网络搜索。

### context7

任何库/框架的官方文档查找。

### grep_app

跨公共 GitHub 仓库的超快代码搜索。非常适合查找实现示例。

### 技能嵌入式 MCP

技能可以自带 MCP 服务器：

```yaml
---
description: Browser automation skill
mcp:
  playwright:
    command: npx
    args: ["-y", "@anthropic-ai/mcp-playwright"]
---
```

`skill_mcp` 工具使用完整的模式发现调用这些操作。

#### OAuth 启用的 MCP

技能可以定义 OAuth 保护的远程 MCP 服务器。支持 OAuth 2.1 及完整 RFC 合规性（RFC 9728、8414、8707、7591）：

```yaml
---
description: My API skill
mcp:
  my-api:
    url: https://api.example.com/mcp
    oauth:
      clientId: ${CLIENT_ID}
      scopes: ["read", "write"]
---
```

当技能 MCP 配置了 `oauth` 时：
- **自动发现**：获取 `/.well-known/oauth-protected-resource`（RFC 9728），回退到 `/.well-known/oauth-authorization-server`（RFC 8414）
- **动态客户端注册**：与支持 RFC 7591 的服务器自动注册（clientId 变为可选）
- **PKCE**：所有流程强制要求
- **资源指示器**：根据 RFC 8707 从 MCP URL 自动生成
- **令牌存储**：持久化在 `~/.config/opencode/mcp-oauth.json`（chmod 0600）
- **自动刷新**：令牌在 401 时刷新；403 时的升级授权与 `WWW-Authenticate`
- **动态端口**：OAuth 回调服务器使用自动发现的可用端口

通过 CLI 预先验证：
```bash
bunx oh-my-opencode mcp oauth login <server-name> --server-url https://api.example.com
```

---

## 上下文注入

### 目录 AGENTS.md

读取文件时自动注入 AGENTS.md。从文件目录走到项目根目录：

```
project/
├── AGENTS.md              # 首先注入
├── src/
│   ├── AGENTS.md          # 第二注入
│   └── components/
│       ├── AGENTS.md      # 第三注入
│       └── Button.tsx     # 读取这个会注入所有 3 个
```

### 条件规则

当条件匹配时从 `.claude/rules/` 注入规则：

```markdown
---
globs: ["*.ts", "src/**/*.js"]
description: "TypeScript/JavaScript coding rules"
---
- Use PascalCase for interface names
- Use camelCase for function names
```

支持：
- `.md` 和 `.mdc` 文件
- 用于模式匹配的 `globs` 字段
- 用于无条件规则的 `alwaysApply: true`
- 从文件到项目根目录向上遍历，加上 `~/.claude/rules/`

---

## Claude Code 兼容性

Claude Code 配置的完整兼容层。

### 配置加载器

| 类型 | 位置 |
|------|------|
| **命令** | `~/.claude/commands/`、`.claude/commands/` |
| **技能** | `~/.claude/skills/*/SKILL.md`、`.claude/skills/*/SKILL.md` |
| **代理** | `~/.claude/agents/*.md`、`.claude/agents/*.md` |
| **MCP** | `~/.claude/.mcp.json`、`.mcp.json`、`.claude/.mcp.json` |

MCP 配置支持环境变量扩展：`${VAR}`。

### 数据存储

| 数据 | 位置 | 格式 |
|------|------|------|
| Todos | `~/.claude/todos/` | Claude Code 兼容 |
| Transcripts | `~/.claude/transcripts/` | JSONL |

### 兼容性切换

禁用特定功能：

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

| 切换 | 禁用 |
|------|------|
| `mcp` | `.mcp.json` 文件（保留内置 MCP） |
| `commands` | `~/.claude/commands/`、`.claude/commands/` |
| `skills` | `~/.claude/skills/`、`.claude/skills/` |
| `agents` | `~/.claude/agents/`（保留内置代理） |
| `hooks` | settings.json 钩子 |
| `plugins` | Claude Code 市场插件 |

禁用特定插件：

```json
{
  "claude_code": {
    "plugins_override": {
      "claude-mem@thedotmack": false
    }
  }
}
```
