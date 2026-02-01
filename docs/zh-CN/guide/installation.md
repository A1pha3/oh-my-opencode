# 安装指南

> 📖 **本文档适合**：需要安装 Oh My OpenCode 的所有用户
>
> 🎯 **目标**：完成安装、配置身份验证、准备开始使用

---

## 目录

- [前准备](#前准备)
- [方式一：让 AI 助手安装（推荐）](#方式一让ai助手安装推荐)
- [方式二：手动安装](#方式二手动安装)
- [身份验证配置](#身份验证配置)
- [安装后验证](#安装后验证)
- [常见安装问题](#常见安装问题)

---

## 前准备

### 检查系统要求

#### OpenCode 版本

Oh My OpenCode 需要 **OpenCode >= 1.0.150**

```bash
# 检查版本
opencode --version

# 如果版本过低，更新
npm install -g opencode@latest
# 或
bun install -g opencode@latest
```

#### 必需工具

```bash
# Bun（推荐用于 CLI）
bun --version  # 需要 >= 1.0.0

# Git
git --version  # 任意版本

# Node.js（可选，用于某些 MCP）
node --version  # 需要 >= 18.0.0
```

### 选择 AI 提供者

Oh My OpenCode 支持多个 AI 提供者。选择你拥有的：

| 提供者 | 推荐模型 | 适用场景 |
|---------|---------|---------|
| **Anthropic (Claude)** | Opus 4.5 | 所有任务，特别是复杂推理 |
| **OpenAI (ChatGPT)** | GPT-5.2 | 架构设计、复杂调试 |
| **Google Gemini** | Gemini 3 Pro/Flash | 前端 UI、多媒体分析 |
| **GitHub Copilot** | Claude/GPT/Gemini | 无直接订阅的备选方案 |
| **OpenCode Zen** | Claude/GPT/Gemini | OpenCode 生态内的模型 |
| **Z.ai Coding Plan** | GLM-4.7 | 低成本方案、Librarian 专用 |

**建议：** 拥有 Claude Pro/Max 订阅，Sisyphus 代理（主协调器）的体验最佳。使用其他模型可能会显著降低质量。

---

## 方式一：让 AI 助手安装（推荐）

这是最简单、最推荐的方式。让 AI 帮你处理所有细节。

### 步骤 1: 准备提示词

将以下提示词复制到你的 AI 工具中（Claude Code、Cursor、AmpCode、Factory Droid 等）：

```
请按照这里的说明安装并配置 oh-my-opencode：
https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/guide/installation.md
```

### 步骤 2: AI 助手会自动执行

AI 助手会：

1. **检查环境**：
   - 验证 OpenCode 版本（>= 1.0.150）
   - 检查 Bun、Git 等依赖是否安装

2. **运行交互式安装程序**：
   ```bash
   bunx oh-my-opencode install
   ```

3. **引导你回答问题**：
   AI 会问你关于订阅情况的问题

4. **配置模型**：
   - 根据你的回答自动生成最优配置
   - 注册插件到 OpenCode 设置

5. **指引身份验证**：
   - 提供每个提供者的认证步骤
   - 帮助完成登录流程

6. **验证安装**：
   - 确认插件已正确注册
   - 检查配置文件是否有效

### 步骤 3: 体验无缝安装

整个过程完成后，你就可以直接开始使用：

```bash
# 启动 OpenCode
opencode

# 尝试第一个任务
ulw 添加用户认证功能
```

---

## 方式二：手动安装

如果你希望自己控制整个过程，可以手动安装。

### 步骤 1: 运行安装程序

```bash
# 使用 Bun（推荐）
bunx oh-my-opencode install

# 或使用 npx（备选）
npx oh-my-opencode install
```

### 步骤 2: 回答安装问题

安装程序会问你以下问题：

#### 问题 1: 你有 Claude Pro/Max 订阅吗？

**选项：**
- ✅ Yes（是）- max20（20 倍模式）或正常模式
- ❌ No（否）

**如果选择 Yes**：
- Sisyphus 和 Prometheus 优先使用 `anthropic/claude-opus-4-5`
- 如果是 max20，使用 Opus 4.5 max variant

**模型分配：**
- **Sisyphus**: `anthropic/claude-opus-4-5`
- **Prometheus**: `anthropic/claude-opus-4-5`
- **Atlas**: `anthropic/claude-sonnet-4-5`

#### 问题 2: 你有 OpenAI/ChatGPT Plus 订阅吗？

**选项：**
- ✅ Yes（是）
- ❌ No（否）

**如果选择 Yes**：
- Oracle 代理使用 `openai/gpt-5.2`
- Ultrabrain Category 使用 GPT-5.2 Codex

**模型分配：**
- **Oracle**: `openai/gpt-5.2`
- **Momus**: `openai/gpt-5.2`

#### 问题 3: 你要集成 Gemini 模型吗？

**选项：**
- ✅ Yes（是）- 使用 Google Antigravity
- ❌ No（否）

**如果选择 Yes**：
- Frontend Agent 和 Category 使用 Google 模型
- Multimodal Looker 使用 Gemini 3 Flash

**注意：** Gemini 需要额外的身份验证步骤（见后文）。

**模型分配：**
- **Frontend Engineer**: `google/antigravity-gemini-3-pro`
- **visual-engineering Category**: `google/antigravity-gemini-3-pro`
- **multimodal-looker**: `google/antigravity-gemini-3-flash`

#### 问题 4: 你有 GitHub Copilot 订阅吗？

**选项：**
- ✅ Yes（是）
- ❌ No（否）

**如果选择 Yes**：
- GitHub Copilot 作为备用提供者
- 当原生提供者不可用时，使用 Copilot

**模型分配：**
- **Sisyphus** (fallback): `github-copilot/claude-opus-4-5`
- **Oracle** (fallback): `github-copilot/gpt-5.2`

#### 问题 5: 你有 OpenCode Zen 访问权限吗？

**选项：**
- ✅ Yes（是）
- ❌ No（否）

**如果选择 Yes**：
- 可以使用 `opencode/` 前缀的模型

**模型分配：**
- **Explore** (fallback): `opencode/claude-haiku-4-5`
- **Librarian** (fallback): `opencode/glm-4.7-free`

#### 问题 6: 你有 Z.ai Coding Plan 订阅吗？

**选项：**
- ✅ Yes（是）
- ❌ No（否）

**如果选择 Yes**：
- Librarian 优先使用 GLM-4.7

**模型分配：**
- **Librarian**: `zai-coding-plan/glm-4.7`
- 如果只有 Z.ai，所有代理都使用 GLM 模型

### 步骤 3: 安装完成

安装程序会：

1. **生成配置文件**：`~/.config/opencode/oh-my-opencode.json`
2. **注册插件**：添加到 `~/.config/opencode/opencode.json` 的插件数组
3. **显示摘要**：总结配置和下一步操作

### 步骤 4: 配置文件结构

生成的配置文件结构：

```jsonc
{
  "$schema": "https://github.com/code-yeongyu/oh-my-opencode/raw/master/assets/oh-my-opencode.schema.json",

  // 代理配置（根据你的回答）
  "agents": {
    "Sisyphus": { "model": "anthropic/claude-opus-4-5" },
    "oracle": { "model": "openai/gpt-5.2" },
    "librarian": { "model": "zai-coding-plan/glm-4.7" },
    ...
  },

  // Category 配置（优化成本）
  "categories": {
    "quick": { "model": "anthropic/claude-haiku-4-5" },
    "ultrabrain": { "model": "openai/gpt-5.2-codex" },
    "visual-engineering": { "model": "google/antigravity-gemini-3-pro" },
    ...
  },

  // 技能配置
  "skills": { ... },

  // 实验性功能
  "experimental": { ... }
}
```

---

## 身份验证配置

安装完成后，需要为你使用的提供者配置身份验证。

### Anthropic (Claude)

#### 使用 Antigravity OAuth（推荐）

安装 `opencode-antigravity-auth` 插件：

```json
{
  "plugin": [
    "oh-my-opencode",
    "opencode-antigravity-auth@latest"
  ]
}
```

配置模型：
```json
{
  "agents": {
    "Sisyphus": { "model": "antigravity-claude-opus-4-5" }
  }
}
```

完成身份验证：
```bash
opencode auth login
# 交互式终端中选择：
# Provider: Anthropic
# Login method: OAuth with Antigravity
# 按照浏览器指引完成登录
```

**Antigravity 优势：**
- ✅ 更稳定的连接
- ✅ 多账户负载均衡
- ✅ Variant 系统（支持 max/high/low）

#### 使用原生 OAuth

```bash
opencode auth login
# 交互式终端中选择：
# Provider: Anthropic
# Login method: Claude Pro/Max
# 按照浏览器指引完成登录
```

### OpenAI (ChatGPT)

```bash
opencode auth login
# 交互式终端中选择：
# Provider: OpenAI
# Login method: API Key 或 OAuth
# 按照指引完成
```

### Google Gemini

**重要：** Gemini 推荐使用 Antigravity OAuth（见上文）。

如果使用 Antigravity，配置已在安装步骤中处理。

### GitHub Copilot

```bash
opencode auth login
# 交互式终端中选择：
# Provider: GitHub
# Login method: OAuth
# 按照浏览器指引完成
```

### OpenCode Zen

```bash
# 确保 opencode 模型可用
opencode models | grep opencode/

# 在配置中使用
opencode auth login
# 按照指引完成
```

### Z.ai Coding Plan

Z.ai Coding Plan 的 API 密钥通常需要单独在 Z.ai 平台获取。

```bash
# 在配置中添加 API 密钥
cat ~/.config/opencode/opencode.json | grep zai-coding-plan
```

---

## 安装后验证

### 步骤 1: 验证版本

```bash
# 检查 OpenCode 版本
opencode --version
# 应该 >= 1.0.150

# 检查 Oh My OpenCode 版本（如果已安装）
bunx oh-my-opencode version
```

### 步骤 2: 验证插件注册

```bash
# 查看配置文件
cat ~/.config/opencode/opencode.json

# 应该包含：
{
  "plugin": [
    "oh-my-opencode",  // ← 必须存在
    ...
  ]
}
```

### 步骤 3: 运行诊断

```bash
# 运行完整诊断
bunx oh-my-opencode doctor

# 或查看特定类别
bunx oh-my-opencode doctor --category authentication
```

诊断会检查：
- ✅ OpenCode 版本（>= 1.0.150）
- ✅ 插件注册状态
- ✅ 配置文件有效性（JSONC 解析）
- ✅ API 密钥有效性
- ✅ 依赖安装状态（Bun、Git、Node.js）
- ✅ LSP 服务器状态
- ✅ MCP 服务器状态

### 步骤 4: 测试基本功能

```bash
# 启动 OpenCode
opencode

# 尝试简单任务
"ulw say hello"
```

如果看到 Oh My OpenCode 的代理响应，安装成功！

---

## 常见安装问题

### 问题 1: "Oh My OpenCode not registered" 错误

**现象：** OpenCode 找不到插件。

**解决方案：**

1. **检查配置文件位置：**
   ```bash
   # 应该存在
   ls -la ~/.config/opencode/oh-my-opencode.json
   ```

2. **重新安装插件：**
   ```bash
   bunx oh-my-opencode install
   ```

3. **手动注册：**
   ```json
   // 编辑 ~/.config/opencode/opencode.json
   {
     "plugin": [
       "oh-my-opencode"
     ]
   }
   ```

### 问题 2: JSONC 解析错误

**现象：** 配置文件格式错误。

**常见原因：**
- 缺少引号
- 多余的逗号（没有 JSONC 支持）
- 嵌套对象错误

**解决方案：**

```bash
# 运行诊断查看详细错误
bunx oh-my-opencode doctor --verbose

# 使用 JSON 验证器
cat ~/.config/opencode/oh-my-opencode.json | jq '.'
```

### 问题 3: API 密钥无效

**现象：** 代理调用失败，提示"API key invalid"。

**解决方案：**

1. **重新验证密钥：**
   - 访问提供者平台检查 API 密钥状态
   - 确认密钥未过期或撤销

2. **重新认证：**
   ```bash
   opencode auth login
   # 按照指引重新登录
   ```

3. **检查网络连接：**
   ```bash
   # 测试 API 连接
   curl https://api.anthropic.com/v1/models -H "x-api-key: YOUR_KEY"
   ```

### 问题 4: Gemini 集成问题

**现象：** Gemini 模型无法使用。

**解决方案：**

1. **确认 Antigravity 安装：**
   ```bash
   cat ~/.config/opencode/opencode.json | grep opencode-antigravity-auth
   # 应该看到插件
   ```

2. **完成 Antigravity 登录：**
   ```bash
   opencode auth login
   # 选择 Google → OAuth with Google (Antigravity)
   ```

3. **配置模型映射：**
   ```json
   {
     "agents": {
       "multimodal-looker": {
         "model": "google/antigravity-gemini-3-flash"
       }
     }
   }
   ```

### 问题 5: Ollama 流式传输错误

**现象：** 使用 Ollama 时出现 "JSON Parse error: Unexpected EOF"。

**原因：** Ollama 返回 NDJSON（换行分隔的 JSON），但 Claude Code SDK 期望单个 JSON 对象。

**解决方案：**

```json
{
  "agents": {
    "explore": {
      "model": "ollama/qwen3-coder",
      "stream": false  // ← 必须！
    }
  }
}
```

**为什么需要 `stream: false`？**

```
Ollama 启用流式传输（默认）：
{"message": {...}, "done": false}
{"message": "", "done": true}
// ← Claude Code SDK 无法解析

Ollama 禁用流式传输（stream: false）：
{"message": {..., "done": true}
// ← 正确的 JSON 格式
```

---

## 进阶配置

### 项目级配置

创建项目特定的配置：

```bash
# 在项目根目录创建
mkdir -p .opencode
touch .opencode/oh-my-opencode.json
```

**项目配置优先级更高**，会覆盖用户级配置。

### 配置模板

#### 基础配置（最小化）

```jsonc
{
  "$schema": "https://github.com/code-yeongyu/oh-my-opencode/raw/master/assets/oh-my-opencode.schema.json",

  // 只配置必要的代理
  "agents": {
    "oracle": { "model": "openai/gpt-5.2" }
  }
}
```

#### 优化成本配置

```jsonc
{
  "$schema": "...",

  // Category 成本优化
  "categories": {
    "quick": {
      "model": "anthropic/claude-haiku-4-5",
      "description": "Trivial tasks - use fastest/cheapest"
    },
    "unspecified-low": {
      "model": "anthropic/claude-sonnet-4-5",
      "description": "Medium complexity - use balanced model"
    },
    "visual-engineering": {
      "model": "google/antigravity-gemini-3-pro",
      "description": "UI/UX - use visual specialist"
    },
    "ultrabrain": {
      "model": "openai/gpt-5.2-codex",
      "variant": "xhigh",
      "description": "Complex logic - use most capable"
    }
  },

  // 背景任务并发控制
  "background_task": {
    "defaultConcurrency": 3,
    "providerConcurrency": {
      "anthropic": 2,
      "openai": 3,
      "google": 5
    }
  }
}
```

#### 性能优化配置

```jsonc
{
  "$schema": "...",

  "experimental": {
    // 激进上下文修剪
    "dynamic_context_pruning": {
      "enabled": true,
      "turn_protection": {
        "enabled": true,
        "turns": 3
      }
    },

    // 激进输出截断
    "aggressive_truncation": true,
    "truncate_all_tool_outputs": true
  },

  // LSP 配置
  "lsp": {
    "typescript-language-server": {
      "command": ["typescript-language-server", "--stdio"],
      "extensions": [".ts", ".tsx"],
      "priority": 10,
      "initialization": {
        "preferences": {
          "includeInlayParameterNameHints": "all"
        }
      }
    }
  }
}
```

---

## 更新和卸载

### 更新 Oh My OpenCode

```bash
# 检查更新
bunx oh-my-opencode doctor --category updates

# 重新安装最新版本
bunx oh-my-opencode@latest install
```

### 卸载

```bash
# 1. 移除插件注册
# 编辑 ~/.config/opencode/opencode.json
# 删除 "oh-my-opencode" 从 plugin 数组

# 2. 删除配置文件（可选）
rm ~/.config/opencode/oh-my-opencode.json
rm .opencode/oh-my-opencode.json  # 项目配置

# 3. 删除数据（可选）
rm -rf ~/.claude/todos/
rm -rf .sisyphus/

# 4. 验证卸载
opencode --version
# 应该不再加载 oh-my-opencode
```

---

## 下一步

安装完成后，建议的学习路径：

### 新手路径

```
安装完成
  ↓
[快速入门指南](./quickstart.md)
  ↓
[架构原理深度解析](../architecture/core-principles.md)
  ↓
[尝试第一个任务]
```

### 进阶路径

```
安装完成
  ↓
[功能完整参考](../features/complete-reference.md)
  ↓
[配置完整指南](../configuration/complete-guide.md)
  ↓
[高级主题](../advanced/)
  ↓
[最佳实践](../best-practices/development.md)
```

---

## 📖 相关文档

- [快速入门指南](./quickstart.md) - 从零开始使用
- [常见问题解答](../troubleshooting/faq.md) - 解决问题
- [配置完整指南](../configuration/complete-guide.md) - 深度定制
- [功能完整参考](../features/complete-reference.md) - 了解所有功能

---

**祝你安装顺利！** 🎉
