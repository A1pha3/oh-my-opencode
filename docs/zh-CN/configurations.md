# Oh-My-OpenCode 配置指南

高度个性化，但可根据个人喜好进行调整。

## 快速开始

**大多数用户不需要手动配置任何内容。** 运行交互式安装程序：

```bash
bunx oh-my-opencode install
```

它会询问您关于提供商（Claude、OpenAI、Gemini 等）的问题，并自动生成最佳配置。

**想要自定义？** 以下是常见模式：

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json",
   
  // 覆盖特定代理模型
  "agents": {
    "oracle": { "model": "openai/gpt-5.2" },           // 使用 GPT 进行调试
    "librarian": { "model": "zai-coding-plan/glm-4.7" }, // 使用便宜模型进行研究
    "explore": { "model": "opencode/gpt-5-nano" }        // 使用免费模型进行探索
  },
   
  // 覆盖类别模型（用于 delegate_task）
  "categories": {
    "quick": { "model": "opencode/gpt-5-nano" },         // 快速/便宜处理简单任务
    "visual-engineering": { "model": "google/gemini-3-pro" } // Gemini 用于 UI
  }
}
```

**查找可用模型：** 运行 `opencode models` 查看您环境中的所有模型。

## 配置文件位置

配置文件位置（按优先级排序）：
1. `.opencode/oh-my-opencode.json`（项目级）
2. 用户配置（平台特定）：

| 平台 | 用户配置路径 |
|------|------------|
| **Windows** | `~/.config/opencode/oh-my-opencode.json`（首选）或 `%APPDATA%\opencode\oh-my-opencode.json`（回退） |
| **macOS/Linux** | `~/.config/opencode/oh-my-opencode.json` |

支持架构自动补全：

```json
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json"
}
```

## JSONC 支持

`oh-my-opencode` 配置文件支持 JSONC（带注释的 JSON）：
- 行注释：`// comment`
- 块注释：`/* comment */`
- 尾随逗号：`{ "key": "value", }`

当 `oh-my-opencode.jsonc` 和 `oh-my-opencode.json` 文件同时存在时，`.jsonc` 优先。

**带注释的示例：**

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json",

  /* 代理覆盖 - 为特定任务自定义模型 */
  "agents": {
    "oracle": {
      "model": "openai/gpt-5.2"  // GPT 用于战略推理
    },
    "explore": {
      "model": "opencode/gpt-5-nano"  // 免费且快速用于探索
    },
  },
}
```

## Google 身份验证

**推荐**：对于 Google Gemini 身份验证，请安装 [`opencode-antigravity-auth`](https://github.com/NoeFabris/opencode-antigravity-auth) 插件（`@latest`）。它提供多账户负载均衡、基于变体的思考级别、双配额系统（Antigravity + Gemini CLI），并且有积极维护。参见[安装 > Google Gemini](docs/guide/installation.md#google-gemini-antigravity-oauth)。

## Ollama 提供商

**重要**：当使用 Ollama 作为提供商时，您**必须**禁用流式传输以避免 JSON 解析错误。

### 必需配置

```json
{
  "agents": {
    "explore": {
      "model": "ollama/qwen3-coder",
      "stream": false
    }
  }
}
```

### 为什么需要 `stream: false`

当启用流式传输时，Ollama 返回 NDJSON（换行分隔的 JSON），但 Claude Code SDK 期望单个 JSON 对象。这会导致代理尝试工具调用时出现 `JSON Parse error: Unexpected EOF`。

**问题示例**：
```json
// Ollama 流式响应（NDJSON - 多行）
{"message":{"tool_calls":[...]}, "done":false}
{"message":{"content":""}, "done":true}

// Claude Code SDK 期望（单个 JSON 对象）
{"message":{"tool_calls":[...], "content":""}, "done":true}
```

### 支持的模型

与 oh-my-opencode 配合良好的常见 Ollama 模型：

| 模型 | 最佳用途 | 配置 |
|------|----------|------|
| `ollama/qwen3-coder` | 代码生成、构建修复 | `{"model": "ollama/qwen3-coder", "stream": false}` |
| `ollama/ministral-3:14b` | 探索、代码库搜索 | `{"model": "ollama/ministral-3:14b", "stream": false}` |
| `ollama/lfm2.5-thinking` | 文档、写作 | `{"model": "ollama/lfm2.5-thinking", "stream": false}` |

### 故障排除

如果您遇到 `JSON Parse error: Unexpected EOF`：

1. **验证 `stream: false` 已设置**在您的代理配置中
2. **检查 Ollama 正在运行**：`curl http://localhost:11434/api/tags`
3. **使用 curl 测试**：
   ```bash
   curl -s http://localhost:11434/api/chat \
     -d '{"model": "qwen3-coder", "messages": [{"role": "user", "content": "Hello"}], "stream": false}'
   ```
4. **查看详细故障排除**：[docs/troubleshooting/ollama-streaming-issue.md](troubleshooting/ollama-streaming-issue.md)

### 未来 SDK 修复

长期修复需要 Claude Code SDK 正确解析 NDJSON 响应。在那之前，使用 `stream: false` 作为解决方法。

**跟踪**：[https://github.com/code-yeongyu/oh-my-opencode/issues/1124](https://github.com/code-yeongyu/oh-my-opencode/issues/1124)

## 代理

### 默认运行代理

设置 `oh-my-opencode run` 命令的默认代理：

| 选项 | 默认 | 描述 |
|------|------|------|
| `default_run_agent` | 无 | `oh-my-opencode run` 命令的默认代理名称（环境变量：`OPENCODE_DEFAULT_AGENT`） |

**配置示例：**

```json
{
  "default_run_agent": "Sisyphus"
}
```

可用代理名称：`sisyphus`、`prometheus`、`oracle`、`librarian`、`explore`、`multimodal-looker`、`hephaestus`。

### 覆盖内置代理设置：

```json
{
  "agents": {
    "explore": {
      "model": "anthropic/claude-haiku-4-5",
      "temperature": 0.5
    },
    "multimodal-looker": {
      "disable": true
    }
  }
}
```

每个代理支持：`model`、`temperature`、`top_p`、`prompt`、`prompt_append`、`tools`、`disable`、`description`、`mode`、`color`、`permission`、`category`、`variant`、`maxTokens`、`thinking`、`reasoningEffort`、`textVerbosity`、`providerOptions`。

### 附加代理选项

| 选项 | 类型 | 描述 |
|------|------|------|
| `category` | string | 类别名称，用于继承模型和其他设置 |
| `variant` | string | 模型变体（例如 `max`、`high`、`medium`、`low`、`xhigh`） |
| `maxTokens` | number | 响应的最大令牌数。直接传递给 OpenCode SDK。 |
| `thinking` | object | Anthropic 模型的扩展思考配置。请参阅下面的[思考选项](#思考选项-anthropic)。 |
| `reasoningEffort` | string | OpenAI 推理工作级别。值：`low`、`medium`、`high`、`xhigh`。 |
| `textVerbosity` | string | 文本详细程度级别。值：`low`、`medium`、`high`。 |
| `providerOptions` | object | 直接传递给 OpenCode SDK 的提供商特定选项。 |

#### 思考选项（Anthropic）

```json
{
  "agents": {
    "oracle": {
      "thinking": {
        "type": "enabled",
        "budgetTokens": 200000
      }
    }
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `type` | string | - | `enabled` 或 `disabled` |
| `budgetTokens` | number | - | 扩展思考的最大预算令牌数 |

使用 `prompt_append` 添加额外指令而不替换默认系统提示：

```json
{
  "agents": {
    "librarian": {
      "prompt_append": "Always use the elisp-dev-mcp for Emacs Lisp documentation lookups."
    }
  }
}
```

您也可以使用相同的选项覆盖 `Sisyphus`（主编排器）和 `build`（默认代理）的设置。

### 权限选项

对代理可以执行的操作进行细粒度控制：

```json
{
  "agents": {
    "explore": {
      "permission": {
        "edit": "deny",
        "bash": "ask",
        "webfetch": "allow"
      }
    }
  }
}
```

| 权限 | 描述 | 值 |
|------|------|------|
| `edit` | 文件编辑权限 | `ask` / `allow` / `deny` |
| `bash` | Bash 命令执行 | `ask` / `allow` / `deny` 或按命令：`{ "git": "allow", "rm": "deny" }` |
| `webfetch` | Web 请求权限 | `ask` / `allow` / `deny` |
| `doom_loop` | 允许无限循环检测覆盖 | `ask` / `allow` / `deny` |
| `external_directory` | 访问项目根目录外的文件 | `ask` / `allow` / `deny` |

或通过 `~/.config/opencode/oh-my-opencode.json` 或 `.opencode/oh-my-opencode.json` 中的 `disabled_agents` 禁用：

```json
{
  "disabled_agents": ["oracle", "multimodal-looker"]
}
```

可用代理：`sisyphus`、`prometheus`、`oracle`、`librarian`、`explore`、`multimodal-looker`、`metis`、`momus`、`atlas`

## 内置技能

Oh My OpenCode 包含提供附加能力的内置技能：

- **playwright**（默认）/ **agent-browser**：用于网页抓取、测试、截图和浏览器交互的浏览器自动化。请参阅[浏览器自动化](#浏览器自动化)以切换提供商。
- **git-master**：用于原子提交、rebase/squash 和历史搜索（blame、bisect、log -S）的 Git 专家。**强烈推荐**：与 `delegate_task(category='quick', load_skills=['git-master'], ...)` 一起使用以节省上下文。

通过 `~/.config/opencode/oh-my-opencode.json` 或 `.opencode/oh-my-opencode.json` 中的 `disabled_skills` 禁用内置技能：

```json
{
  "disabled_skills": ["playwright"]
}
```

可用内置技能：`playwright`、`agent-browser`、`git-master`

## 技能配置

配置高级技能设置，包括自定义技能源、启用/禁用特定技能以及定义自定义技能。

```json
{
  "skills": {
    "sources": [
      { "path": "./custom-skills", "recursive": true },
      "https://example.com/skill.yaml"
    ],
    "enable": ["my-custom-skill"],
    "disable": ["other-skill"],
    "my-skill": {
      "description": "Custom skill description",
      "template": "Custom prompt template",
      "from": "source-file.ts",
      "model": "custom/model",
      "agent": "custom-agent",
      "subtask": true,
      "argument-hint": "usage hint",
      "license": "MIT",
      "compatibility": ">= 3.0.0",
      "metadata": {
        "author": "Your Name"
      },
      "allowed-tools": ["tool1", "tool2"]
    }
  }
}
```

### 来源

从本地目录或远程 URL 加载技能：

```json
{
  "skills": {
    "sources": [
      { "path": "./custom-skills", "recursive": true },
      { "path": "./single-skill.yaml" },
      "https://example.com/skill.yaml",
      "https://raw.githubusercontent.com/user/repo/main/skills/*"
    ]
  }
}
```

| 选项 | 默认 | 描述 |
|------|------|------|
| `path` | - | 本地文件/目录路径或远程 URL |
| `recursive` | `false` | 从目录递归加载 |
| `glob` | - | 用于文件选择的 glob 模式 |

### 启用/禁用技能

```json
{
  "skills": {
    "enable": ["skill-1", "skill-2"],
    "disable": ["disabled-skill"]
  }
}
```

### 自定义技能定义

直接在配置中定义自定义技能：

| 选项 | 默认 | 描述 |
|------|------|------|
| `description` | - | 技能的人工可读描述 |
| `template` | - | 技能的自定义提示模板 |
| `from` | - | 用于加载模板的源文件 |
| `model` | - | 覆盖此技能的模型 |
| `agent` | - | 覆盖此技能的代理 |
| `subtask` | `false` | 是否作为子任务运行 |
| `argument-hint` | - | 如何使用技能的提示 |
| `license` | - | 技能许可证 |
| `compatibility` | - | 必需的 oh-my-opencode 版本兼容性 |
| `metadata` | - | 作为键值对的附加元数据 |
| `allowed-tools` | - | 此技能允许使用的工具数组 |

**示例：自定义技能**

```json
{
  "skills": {
    "data-analyst": {
      "description": "Specialized for data analysis tasks",
      "template": "You are a data analyst. Focus on statistical analysis, visualization, and data interpretation.",
      "model": "openai/gpt-5.2",
      "allowed-tools": ["read", "bash", "lsp_diagnostics"]
    }
  }
}
```

## 浏览器自动化

在两种浏览器自动化提供商之间选择：

| 提供商 | 接口 | 特性 | 安装 |
|--------|------|------|------|
| **playwright**（默认） | MCP 工具 | 具有结构化工具调用的 Playwright MCP 服务器 | 通过 npx 自动安装 |
| **agent-browser** | Bash CLI | Vercel 的 CLI，具有会话管理、并行浏览器 | 需要 `bun add -g agent-browser` |

通过 `oh-my-opencode.json` 中的 `browser_automation_engine` 切换提供商：

```json
{
  "browser_automation_engine": {
    "provider": "agent-browser"
  }
}
```

### Playwright（默认）

使用官方 Playwright MCP 服务器（`@playwright/mcp`）。浏览器自动化通过结构化的 MCP 工具调用发生。

### agent-browser

使用 [Vercel 的 agent-browser CLI](https://github.com/vercel-labs/agent-browser)。主要优势：
- **会话管理**：使用 `--session` 标志运行多个隔离的浏览器实例
- **持久配置文件**：使用 `--profile` 保持跨重启的浏览器状态
- **基于快照的工作流**：通过 `snapshot -i` 获取元素引用，使用 `@e1`、`@e2` 等交互
- **CLI 优先**：所有命令通过 Bash - 非常适合脚本编写

**需要安装**：
```bash
bun add -g agent-browser
agent-browser install  # 下载 Chromium
```

**示例工作流**：
```bash
agent-browser open https://example.com
agent-browser snapshot -i  # 获取带有引用的交互元素
agent-browser fill @e1 "user@example.com"
agent-browser click @e2
agent-browser screenshot result.png
agent-browser close
```

## Tmux 集成

在单独的 tmux 窗格中运行后台子代理，实现**可视化多代理执行**。并行查看您的代理工作，每个代理在自己的终端窗格中。

通过 `oh-my-opencode.json` 中的 `tmux` 启用 tmux 集成：

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

| 选项 | 默认 | 描述 |
|------|------|------|
| `enabled` | `false` | 启用 tmux 子代理窗格生成。仅在现有 tmux 会话中运行时才有效。 |
| `layout` | `main-vertical` | 代理窗格的 tmux 布局。请参阅下面的[布局选项](#布局选项)。 |
| `main_pane_size` | `60` | 主窗格大小百分比（20-80）。 |
| `main_pane_min_width` | 120 | 主窗格的最小宽度（列）。 |
| `agent_pane_min_width` | 40 | 每个代理窗格的最小宽度（列）。 |

### 布局选项

| 布局 | 描述 |
|------|------|
| `main-vertical` | 主窗格在左侧，代理窗格堆叠在右侧（默认） |
| `main-horizontal` | 主窗格在顶部，代理窗格堆叠在底部 |
| `tiled` | 所有窗格在等大小的网格中 |
| `even-horizontal` | 所有窗格在水平行中 |
| `even-vertical` | 所有窗格在垂直堆栈中 |

### 要求

1. **必须在 tmux 中运行**：仅当 OpenCode 已经在 tmux 会话中运行时，此功能才会激活
2. **安装 tmux**：要求 tmux 在 PATH 中可用
3. **服务器模式**：OpenCode 必须使用 `--port` 标志运行以启用子代理窗格生成

### 工作原理

当 `tmux.enabled` 为 `true` 且您在 tmux 会话中时：
- 后台代理（通过 `delegate_task(run_in_background=true)`）在新的 tmux 窗格中生成
- 每个窗格显示子代理的实时输出
- 子代理完成后窗格自动关闭
- 布局根据您的配置自动调整

### 使用 Tmux 子代理支持运行 OpenCode

要启用 tmux 子代理窗格，OpenCode 必须以带有 `--port` 标志的**服务器模式**运行。这会启动一个 HTTP 服务器，子代理窗格通过 `opencode attach` 连接。

**基本设置**：
```bash
# 启动 tmux 会话
tmux new -s dev

# 使用服务器模式运行 OpenCode（端口 4096）
opencode --port 4096

# 现在后台代理将出现在单独的窗格中
```

**推荐：Shell 函数**

为方便起见，创建一个自动处理 tmux 会话和端口分配的 shell 函数。以下是 Fish shell 的示例：

```fish
# ~/.config/fish/config.fish
function oc
    set base_name (basename (pwd))
    set path_hash (echo (pwd) | md5 | cut -c1-4)
    set session_name "$base_name-$path_hash"
    
    # 从 4096 开始查找可用端口
    function __oc_find_port
        set port 4096
        while test $port -lt 5096
            if not lsof -i :$port >/dev/null 2>&1
                echo $port
                return 0
            end
            set port (math $port + 1)
        end
        echo 4096
    end
    
    set oc_port (__oc_find_port)
    set -x OPENCODE_PORT $oc_port
    
    if set -q TMUX
        # 已在 tmux 内 - 只运行带端口的
        opencode --port $oc_port $argv
    else
        # 创建 tmux 会话并运行 opencode
        set oc_cmd "OPENCODE_PORT=$oc_port opencode --port $oc_port $argv; exec fish"
        if tmux has-session -t "$session_name" 2>/dev/null
            tmux new-window -t "$session_name" -c (pwd) "$oc_cmd"
            tmux attach-session -t "$session_name"
        else
            tmux new-session -s "$session_name" -c (pwd) "$oc_cmd"
        end
    end
    
    functions -e __oc_find_port
end
```

**Bash/Zsh 等效**：

```bash
# ~/.bashrc or ~/.zshrc
oc() {
    local base_name=$(basename "$PWD")
    local path_hash=$(echo "$PWD" | md5sum | cut -c1-4)
    local session_name="${base_name}-${path_hash}"
    
    # 查找可用端口
    local port=4096
    while [ $port -lt 5096 ]; do
        if ! lsof -i :$port >/dev/null 2>&1; then
            break
        fi
        port=$((port + 1))
    done
    
    export OPENCODE_PORT=$port
    
    if [ -n "$TMUX" ]; then
        opencode --port $port "$@"
    else
        local oc_cmd="OPENCODE_PORT=$port opencode --port $port $*; exec $SHELL"
        if tmux has-session -t "$session_name" 2>/dev/null; then
            tmux new-window -t "$session_name" -c "$PWD" "$oc_cmd"
            tmux attach-session -t "$session_name"
        else
            tmux new-session -s "$session_name" -c "$PWD" "$oc_cmd"
        fi
    fi
}
```

**子代理窗格的工作原理**：

1. 主 OpenCode 在指定端口（例如 `http://localhost:4096`）上启动 HTTP 服务器
2. 当后台代理生成时，Oh My OpenCode 创建一个新的 tmux 窗格
3. 窗格运行：`opencode attach http://localhost:4096 --session <session-id>`
4. 每个子代理窗格显示实时流式输出
5. 子代理完成后窗格自动关闭

**环境变量**：

| 变量 | 描述 |
|------|------|
| `OPENCODE_PORT` | HTTP 服务器的默认端口（如果未指定 `--port` 则使用） |

### 服务器模式参考

OpenCode 的服务器模式公开了用于程序化交互的 HTTP API：

```bash
# 独立服务器（无 TUI）
opencode serve --port 4096

# 带服务器的 TUI（推荐用于 tmux 集成）
opencode --port 4096
```

| 标志 | 默认 | 描述 |
|------|------|------|
| `--port` | 4096 | HTTP 服务器端口 |
| `--hostname` | `127.0.0.1` | 监听的主机名 |

更多详情，请参阅 [OpenCode 服务器文档](https://opencode.ai/docs/server/)。

## Git Master

配置 git-master 技能行为：

```json
{
  "git_master": {
    "commit_footer": true,
    "include_co_authored_by": true
  }
}
```

| 选项 | 默认 | 描述 |
|------|------|------|
| `commit_footer` | `true` | 在提交消息中添加 "Ultraworked with Sisyphus" 页脚。 |
| `include_co_authored_by` | `true` | 添加 `Co-authored-by: Sisyphus <clio-agent@sisyphuslabs.ai>` 尾部到提交中。 |

## Sisyphus 代理

启用时（默认），Sisyphus 提供了一个强大的编排器，具有可选的专业代理：

- **Sisyphus**：主要编排器代理（Claude Opus 4.5）
- **OpenCode-Builder**：OpenCode 的默认构建代理，由于 SDK 限制已重命名（默认禁用）
- **Prometheus（规划器）**：具有工作规划方法论的 OpenCode 默认规划代理（默认启用）
- **Metis（规划顾问）**：预先规划分析代理，识别隐藏的需求和 AI 失败点

**配置选项：**

```json
{
  "sisyphus_agent": {
    "disabled": false,
    "default_builder_enabled": false,
    "planner_enabled": true,
    "replace_plan": true
  }
}
```

**示例：启用 OpenCode-Builder：**

```json
{
  "sisyphus_agent": {
    "default_builder_enabled": true
  }
}
```

这将启用 OpenCode-Builder 代理与 Sisyphus 一起使用。当 Sisyphus 启用时，默认构建代理始终降级为子代理模式。

**示例：禁用所有 Sisyphus 编排：**

```json
{
  "sisyphus_agent": {
    "disabled": true
  }
}
```

您也可以像其他代理一样自定义 Sisyphus 代理：

```json
{
  "agents": {
    "Sisyphus": {
      "model": "anthropic/claude-sonnet-4",
      "temperature": 0.3
    },
    "OpenCode-Builder": {
      "model": "anthropic/claude-opus-4"
    },
    "Prometheus (Planner)": {
      "model": "openai/gpt-5.2"
    },
    "Metis (Plan Consultant)": {
      "model": "anthropic/claude-sonnet-4-5"
    }
  }
}
```

| 选项 | 默认 | 描述 |
|------|------|------|
| `disabled` | `false` | 当为 `true` 时，禁用所有 Sisyphus 编排并恢复原始 build/plan 作为主要。 |
| `default_builder_enabled` | `false` | 当为 `true` 时，启用 OpenCode-Builder 代理（与 OpenCode 构建相同，由于 SDK 限制已重命名）。默认禁用。 |
| `planner_enabled` | `true` | 当为 `true` 时，启用具有工作规划方法论的 Prometheus（规划器）代理。默认启用。 |
| `replace_plan` | `true` | 当为 `true` 时，将默认规划代理降级为子代理模式。设置为 `false` 以保持 Prometheus（规划器）和默认规划都可用。 |

## 后台任务

配置后台代理任务的并发限制。这控制了多少并行后台代理可以同时运行。

```json
{
  "background_task": {
    "defaultConcurrency": 5,
    "staleTimeoutMs": 180000,
    "providerConcurrency": {
      "anthropic": 3,
      "openai": 5,
      "google": 10
    },
    "modelConcurrency": {
      "anthropic/claude-opus-4-5": 2,
      "google/gemini-3-flash": 10
    }
  }
}
```

| 选项 | 默认 | 描述 |
|------|------|------|
| `defaultConcurrency` | - | 所有提供商/模型的默认最大并发后台任务 |
| `staleTimeoutMs` | `180000` | 过时超时（毫秒）- 中断在此持续时间内无活动的任务（最小值：60000 = 1 分钟） |
| `providerConcurrency` | - | 每个提供商的并发限制。键是提供商名称（例如 `anthropic`、`openai`、`google`） |
| `modelConcurrency` | - | 每个模型的并发限制。键是完整的模型名称（例如 `anthropic/claude-opus-4-5`）。覆盖提供商限制。 |

**优先级顺序**：`modelConcurrency` > `providerConcurrency` > `defaultConcurrency`

**使用场景**：
- 限制昂贵模型（例如 Opus）以防止成本激增
- 允许更多快速/便宜模型（例如 Gemini Flash）的并发任务
- 通过设置提供商级别上限来遵守提供商速率限制

## 类别

类别通过 `delegate_task` 工具启用域特定任务委托。每个类别在调用 `Sisyphus-Junior` 代理时应用运行时预设（模型、温度、提示附加）。

### 内置类别

所有 7 个类别都带有最佳的模型默认值，但**您必须配置它们才能使用这些默认值**：

| 类别 | 内置默认模型 | 描述 |
|------|--------------|------|
| `visual-engineering` | `google/gemini-3-pro-preview` | 前端、UI/UX、设计、样式、动画 |
| `ultrabrain` | `openai/gpt-5.2-codex`（xhigh） | 深度逻辑推理、需要广泛分析复杂架构决策 |
| `artistry` | `google/gemini-3-pro-preview`（max） | 高度创意/艺术任务、新想法 |
| `quick` | `anthropic/claude-haiku-4-5` | 简单任务 - 单文件更改、拼写错误修复、简单修改 |
| `unspecified-low` | `anthropic/claude-sonnet-4-5` | 不适合其他类别的任务，低工作量要求 |
| `unspecified-high` | `anthropic/claude-opus-4-5`（max） | 不适合其他类别的任务，高工作量要求 |
| `writing` | `google/gemini-3-flash-preview` | 文档、散文、技术写作 |

### ⚠️ 关键：模型解析优先级

**类别除非配置，否则不使用其内置默认值。** 模型解析遵循此优先级：

```
1. 用户配置的模型（在 oh-my-opencode.json 中）
2. 类别的内置默认值（如果您将类别添加到配置中）
3. 系统默认模型（来自 opencode.json）
```

**问题示例：**

```json
// opencode.json
{ "model": "anthropic/claude-sonnet-4-5" }

// oh-my-opencode.json（空类别部分）
{}

// 结果：所有类别都使用 claude-sonnet-4-5（浪费！）
// - 简单任务使用 Sonnet 而不是 Haiku（昂贵）
// - ultrabrain 使用 Sonnet 而不是 GPT-5.2（推理能力较差）
// - 视觉任务使用 Sonnet 而不是 Gemini（UI 不最优）
```

### 推荐配置

**要使用每个类别的最佳模型，请将它们添加到您的配置中：**

```json
{
  "categories": {
    "visual-engineering": { 
      "model": "google/gemini-3-pro-preview"
    },
    "ultrabrain": { 
      "model": "openai/gpt-5.2-codex",
      "variant": "xhigh"
    },
    "artistry": { 
      "model": "google/gemini-3-pro-preview",
      "variant": "max"
    },
    "quick": { 
      "model": "anthropic/claude-haiku-4-5"  // 快速 + 便宜处理简单任务
    },
    "unspecified-low": { 
      "model": "anthropic/claude-sonnet-4-5"
    },
    "unspecified-high": { 
      "model": "anthropic/claude-opus-4-5",
      "variant": "max"
    },
    "writing": { 
      "model": "google/gemini-3-flash-preview"
    }
  }
}
```

**只配置您有权访问的类别。** 未配置的类别会回退到您的系统默认模型。

### 使用方法

```javascript
// 通过 delegate_task 工具
delegate_task(category="visual-engineering", prompt="Create a responsive dashboard component")
delegate_task(category="ultrabrain", prompt="Design the payment processing flow")

// 或直接定位特定代理（绕过类别）
delegate_task(agent="oracle", prompt="Review this architecture")
```

### 自定义类别

添加您自己的类别或覆盖内置类别：

```json
{
  "categories": {
    "data-science": {
      "model": "anthropic/claude-sonnet-4-5",
      "temperature": 0.2,
      "prompt_append": "Focus on data analysis, ML pipelines, and statistical methods."
    },
    "visual-engineering": {
      "model": "google/gemini-3-pro-preview",
      "prompt_append": "Use shadcn/ui components and Tailwind CSS."
    }
  }
}
```

每个类别支持：`model`、`temperature`、`top_p`、`maxTokens`、`thinking`、`reasoningEffort`、`textVerbosity`、`tools`、`prompt_append`、`variant`、`description`、`is_unstable_agent`。

### 附加类别选项

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `description` | string | - | 类别用途的人工可读描述。在 delegate_task 提示中显示。 |
| `is_unstable_agent` | boolean | `false` | 将代理标记为不稳定 - 强制后台模式进行监控。Gemini 模型自动启用。 |

## 模型解析系统

在运行时，Oh My OpenCode 使用 3 步解析过程来确定每个代理和类别使用哪个模型。这根据您的配置和支持的模型动态发生。

### 概述

**问题**：用户有不同的提供商配置。系统需要在运行时为每个任务选择最佳可用模型。

**解决方案**：简单的 3 步解析流程：
1. **步骤 1：用户覆盖** — 如果您在 `oh-my-opencode.json` 中指定模型，则精确使用该模型
2. **步骤 2：提供商回退** — 按要求优先级顺序尝试每个提供商，直到找到一个可用的
3. **步骤 3：系统默认** — 回退到 OpenCode 配置的默认模型

### 解析流程

```
┌─────────────────────────────────────────────────────────────────┐
│                     MODEL RESOLUTION FLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Step 1: USER OVERRIDE                                         │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ User specified model in oh-my-opencode.json?            │   │
│   │         YES → Use exactly as specified                  │   │
│   │         NO  → Continue to Step 2                        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│   Step 2: PROVIDER PRIORITY FALLBACK                            │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ For each provider in requirement.providers order:       │   │
│   │                                                         │   │
│   │ Example for Sisyphus:                                   │   │
│   │ anthropic → github-copilot → opencode → antigravity     │   │
│   │     │            │              │            │          │   │
│   │     ▼            ▼              ▼            ▼          │   │
│   │ Try: anthropic/claude-opus-4-5                          │   │
│   │ Try: github-copilot/claude-opus-4-5                     │   │
│   │ Try: opencode/claude-opus-4-5                           │   │
│   │ ...                                                     │   │
│   │                                                         │   │
│   │ Found in available models? → Return matched model       │   │
│   │ Not found? → Try next provider                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼ (all providers exhausted)        │
│   Step 3: SYSTEM DEFAULT                                        │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ Return systemDefaultModel (from opencode.json)          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 代理提供商链

每个代理都有定义的提供商优先级链。系统按顺序尝试提供商，直到找到可用的模型：

| 代理 | 模型（无前缀） | 提供商优先级链 |
|------|----------------|----------------|
| **Sisyphus** | `claude-opus-4-5` | anthropic → kimi-for-coding → zai-coding-plan → openai → google |
| **oracle** | `gpt-5.2` | openai → google → anthropic |
| **librarian** | `glm-4-7` | zai-coding-plan → opencode → anthropic |
| **explore** | `claude-haiku-4-5` | anthropic → github-copilot → opencode |
| **multimodal-looker** | `gemini-3-flash` | google → openai → zai-coding-plan → kimi-for-coding → anthropic → opencode |
| **Prometheus（规划器）** | `claude-opus-4-5` | anthropic → kimi-for-coding → openai → google |
| **Metis（规划顾问）** | `claude-opus-4-5` | anthropic → kimi-for-coding → openai → google |
| **Momus（规划审查员）** | `gpt-5.2` | openai → anthropic → google |
| **Atlas** | `claude-sonnet-4-5` | anthropic → kimi-for-coding → openai → google |

### 类别提供商链

类别遵循相同的解析逻辑：

| 类别 | 模型（无前缀） | 提供商优先级链 |
|------|----------------|----------------|
| **visual-engineering** | `gemini-3-pro` | google → anthropic → zai-coding-plan |
| **ultrabrain** | `gpt-5.2-codex` | openai → google → anthropic |
| **deep** | `gpt-5.2-codex` | openai → anthropic → google |
| **artistry** | `gemini-3-pro` | google → anthropic → openai |
| **quick** | `claude-haiku-4-5` | anthropic → google → opencode |
| **unspecified-low** | `claude-sonnet-4-5` | anthropic → openai → google |
| **unspecified-high** | `claude-opus-4-5` | anthropic → openai → google |
| **writing** | `gemini-3-flash` | google → anthropic → zai-coding-plan → openai |

### 检查您的配置

使用 `doctor` 命令查看模型如何根据您的当前配置解析：

```bash
bunx oh-my-opencode doctor --verbose
```

"Model Resolution" 检查显示：
- 每个代理/类别的模型要求
- 提供商回退链
- 用户覆盖（如果已配置）
- 有效的解析路径

### 手动覆盖

在 `oh-my-opencode.json` 中覆盖任何代理或类别模型：

```json
{
  "agents": {
    "Sisyphus": {
      "model": "anthropic/claude-sonnet-4-5"
    },
    "oracle": {
      "model": "openai/o3"
    }
  },
  "categories": {
    "visual-engineering": {
      "model": "anthropic/claude-opus-4-5"
    }
  }
}
```

当您指定模型覆盖时，它优先（步骤 1），并且提供商回退链完全被跳过。

## 钩子

通过 `~/.config/opencode/oh-my-opencode.json` 或 `.opencode/oh-my-opencode.json` 中的 `disabled_hooks` 禁用特定内置钩子：

```json
{
  "disabled_hooks": ["comment-checker", "agent-usage-reminder"]
}
```

可用钩子：`todo-continuation-enforcer`、`context-window-monitor`、`session-recovery`、`session-notification`、`comment-checker`、`grep-output-truncator`、`tool-output-truncator`、`directory-agents-injector`、`directory-readme-injector`、`empty-task-response-detector`、`think-mode`、`anthropic-context-window-limit-recovery`、`rules-injector`、`background-notification`、`auto-update-checker`、`startup-toast`、`keyword-detector`、`agent-usage-reminder`、`non-interactive-env`、`interactive-bash-session`、`compaction-context-injector`、`thinking-block-validator`、`claude-code-hooks`、`ralph-loop`、`preemptive-compaction`、`auto-slash-command`、`sisyphus-junior-notepad`、`start-work`

**关于 `directory-agents-injector` 的说明**：此钩子在 OpenCode 1.1.37+ 上运行时**自动禁用**，因为 OpenCode 现在原生支持从子目录动态解析 AGENTS.md 文件（PR #10678）。这可以防止重复的 AGENTS.md 注入。对于较旧的 OpenCode 版本，钩子保持活动以提供相同的功能。

**关于 `auto-update-checker` 和 `startup-toast` 的说明**：`startup-toast` 钩子是 `auto-update-checker` 的子功能。要仅禁用启动提示通知而保持更新检查启用，请将 `"startup-toast"` 添加到 `disabled_hooks`。要禁用所有更新检查功能（包括提示），请将 `"auto-update-checker"` 添加到 `disabled_hooks`。

## 禁用命令

通过 `~/.config/opencode/oh-my-opencode.json` 或 `.opencode/oh-my-opencode.json` 中的 `disabled_commands` 禁用特定内置命令：

```json
{
  "disabled_commands": ["init-deep", "start-work"]
}
```

可用命令：`init-deep`、`start-work`

## 注释检查器

配置注释检查器钩子行为。当代码中添加过多注释时，注释检查器会发出警告。

```json
{
  "comment_checker": {
    "custom_prompt": "Your custom warning message. Use {{comments}} placeholder for detected comments XML."
  }
}
```

| 选项 | 默认 | 描述 |
|------|------|------|
| `custom_prompt` | - | 自定义警告消息以替换默认。使用 `{{comments}}` 占位符表示检测到的注释 XML。 |

## 通知

配置后台任务完成时的通知行为。

```json
{
  "notification": {
    "force_enable": true
  }
}
```

| 选项 | 默认 | 描述 |
|------|------|------|
| `force_enable` | `false` | 即使检测到外部通知插件也强制启用会话通知。默认：`false`。 |

## Sisyphus 任务与群集

配置 Sisyphus 任务和群集系统以进行高级任务管理和多代理编排。

```json
{
  "sisyphus": {
    "tasks": {
      "enabled": false,
      "storage_path": ".sisyphus/tasks",
      "claude_code_compat": false
    },
    "swarm": {
      "enabled": false,
      "storage_path": ".sisyphus/teams",
      "ui_mode": "toast"
    }
  }
}
```

### 任务配置

| 选项 | 默认 | 描述 |
|------|------|------|
| `enabled` | `false` | 启用 Sisyphus 任务系统 |
| `storage_path` | `.sisyphus/tasks` | 任务的存储路径（相对于项目根目录） |
| `claude_code_compat` | `false` | 启用 Claude Code 路径兼容性模式 |

### 群集配置

| 选项 | 默认 | 描述 |
|------|------|------|
| `enabled` | `false` | 启用 Sisyphus 群集系统进行多代理编排 |
| `storage_path` | `.sisyphus/teams` | 团队的存储路径（相对于项目根目录） |
| `ui_mode` | `toast` | UI 模式：`toast`（通知）、`tmux`（窗格）或 `both` |

## MCP

Exa、Context7 和 grep.app MCP 默认启用。

- **websearch**：由 [Exa AI](https://exa.ai) 提供支持的实时网络搜索 - 搜索网络并返回相关内容
- **context7**：获取库的最新官方文档
- **grep_app**：通过 [grep.app](https://grep.app) 在数百万个公共 GitHub 存储库中进行超快代码搜索

不想要它们？通过 `~/.config/opencode/oh-my-opencode.json` 或 `.opencode/oh-my-opencode.json` 中的 `disabled_mcps` 禁用：

```json
{
  "disabled_mcps": ["websearch", "context7", "grep_app"]
}
```

## LSP

OpenCode 提供用于分析的 LSP 工具。
Oh My OpenCode 添加了重构工具（重命名、代码操作）。
支持所有 OpenCode LSP 配置和自定义设置（来自 opencode.json），以及附加的 Oh My OpenCode 特定设置。

通过 `~/.config/opencode/oh-my-opencode.json` 或 `.opencode/oh-my-opencode.json` 中的 `lsp` 选项添加 LSP 服务器：

```json
{
  "lsp": {
    "typescript-language-server": {
      "command": ["typescript-language-server", "--stdio"],
      "extensions": [".ts", ".tsx"],
      "priority": 10
    },
    "pylsp": {
      "disabled": true
    }
  }
}
```

每个服务器支持：`command`、`extensions`、`priority`、`env`、`initialization`、`disabled`。

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `command` | array | - | 启动 LSP 服务器的命令（可执行文件 + 参数） |
| `extensions` | array | - | 此服务器处理的文件扩展名（例如 `[".ts", ".tsx"]`） |
| `priority` | number | - | 多个服务器匹配文件时的服务器优先级 |
| `env` | object | - | LSP 服务器的环境变量（键值对） |
| `initialization` | object | - | 传递给 LSP 服务器的自定义初始化选项 |
| `disabled` | boolean | `false` | 是否禁用此 LSP 服务器 |

**带有高级选项的示例：**

```json
{
  "lsp": {
    "typescript-language-server": {
      "command": ["typescript-language-server", "--stdio"],
      "extensions": [".ts", ".tsx"],
      "priority": 10,
      "env": {
        "NODE_OPTIONS": "--max-old-space-size=4096"
      },
      "initialization": {
        "preferences": {
          "includeInlayParameterNameHints": "all",
          "includeInlayFunctionParameterTypeHints": true
        }
      }
    }
  }
}
```

## 实验性

可选的实验性功能，可能会在未来的版本中更改或删除。请谨慎使用。

```json
{
  "experimental": {
    "truncate_all_tool_outputs": true,
    "aggressive_truncation": true,
    "auto_resume": true,
    "dynamic_context_pruning": {
      "enabled": false,
      "notification": "detailed",
      "turn_protection": {
        "enabled": true,
        "turns": 3
      },
      "protected_tools": ["task", "todowrite", "lsp_rename"],
      "strategies": {
        "deduplication": {
          "enabled": true
        },
        "supersede_writes": {
          "enabled": true,
          "aggressive": false
        },
        "purge_errors": {
          "enabled": true,
          "turns": 5
        }
      }
    }
  }
}
```

| 选项 | 默认 | 描述 |
|------|------|------|
| `truncate_all_tool_outputs` | `false` | 截断所有工具输出，而不仅仅是列入白名单的工具（Grep、Glob、LSP、AST-grep）。工具输出截断器默认启用 - 通过 `disabled_hooks` 禁用。 |
| `aggressive_truncation` | `false` | 当超出令牌限制时，激进地截断工具输出以适应限制。比默认截断行为更激进。如果不足则回退到总结/还原。 |
| `auto_resume` | `false` | 从思考块错误或思考禁用违规的成功恢复后自动恢复会话。提取最后一条用户消息并继续。 |
| `dynamic_context_pruning` | 见下文 | 动态上下文修剪配置，用于自动管理上下文窗口使用。请参阅下面的[动态上下文修剪](#动态上下文修剪)。 |

### 动态上下文修剪

动态上下文修剪通过智能修剪旧工具输出来自动管理上下文窗口。此功能有助于在长会话中保持性能。

```json
{
  "experimental": {
    "dynamic_context_pruning": {
      "enabled": false,
      "notification": "detailed",
      "turn_protection": {
        "enabled": true,
        "turns": 3
      },
      "protected_tools": ["task", "todowrite", "todoread", "lsp_rename", "session_read", "session_write", "session_search"],
      "strategies": {
        "deduplication": {
          "enabled": true
        },
        "supersede_writes": {
          "enabled": true,
          "aggressive": false
        },
        "purge_errors": {
          "enabled": true,
          "turns": 5
        }
      }
    }
  }
}
```

| 选项 | 默认 | 描述 |
|------|------|------|
| `enabled` | `false` | 启用动态上下文修剪 |
| `notification` | `detailed` | 通知级别：`off`、`minimal` 或 `detailed` |
| `turn_protection` | 见下文 | 轮次保护设置 - 防止修剪最近的工具输出 |

#### 轮次保护

| 选项 | 默认 | 描述 |
|------|------|------|
| `enabled` | `true` | 启用轮次保护 |
| `turns` | `3` | 要保护免受修剪的最近轮次数（1-10） |

#### 受保护的工具

永远不应修剪的工具（默认）：

```json
["task", "todowrite", "todoread", "lsp_rename", "session_read", "session_write", "session_search"]
```

#### 修剪策略

| 策略 | 选项 | 默认 | 描述 |
|------|------|------|------|
| **deduplication** | `enabled` | `true` | 删除重复的工具调用（相同的工具 + 相同的参数） |
| **supersede_writes** | `enabled` | `true` | 当文件随后被读取时修剪写入输入 |
| | `aggressive` | `false` | 激进模式：如果有任何后续读取，则修剪任何写入 |
| **purge_errors** | `enabled` | `true` | 在 N 轮后修剪错误的工具输入 |
| | `turns` | `5` | 修剪错误之前的轮次数（1-20） |

**警告**：这些功能是实验性的，可能会导致意外行为。仅在您理解其含义时才启用。

## 环境变量

| 变量 | 描述 |
|------|------|
| `OPENCODE_CONFIG_DIR` | 覆盖 OpenCode 配置目录。对于与 [OCX](https://github.com/kdcokenny/ocx) 鬼影模式等工具的配置文件隔离很有用。 |
