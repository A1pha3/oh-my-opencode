# 常见问题解答

> 📖 **本文档适合**：遇到问题需要快速解决方案的开发者
>
> 🎯 **快速查找**：使用 `Ctrl+F` 或 `Cmd+F` 搜索关键词

---

## 目录

- [安装相关问题](#安装相关问题)
- [使用问题](#使用问题)
- [性能和成本](#性能和成本)
- [模型和配置](#模型和配置)
- [错误和故障](#错误和故障)
- [高级使用](#高级使用)

---

## 安装相关问题

### Q1: "OpenCode version too old" 错误

**问题描述：** 安装或运行时出现错误提示 OpenCode 版本太旧。

**原因：** Oh My OpenCode 需要 OpenCode >= 1.0.150 版本。

**解决方案：**
```bash
# 更新 OpenCode
npm install -g opencode@latest
# 或
bun install -g opencode@latest

# 验证版本
opencode --version  # 应该 >= 1.0.150
```

---

### Q2: "Plugin not registered" 错误

**问题描述：** 插件未在 OpenCode 中正确注册。

**原因：** 安装过程中断开或配置文件损坏。

**解决方案：**
```bash
# 重新安装插件
bunx oh-my-opencode install

# 检查配置文件
cat ~/.config/opencode/opencode.json  # 应该包含 "oh-my-opencode"
```

---

### Q3: API 密钥无效或认证失败

**问题描述：** API 密钥被拒绝或无法完成 OAuth 流程。

**可能原因：**
1. API 密钥过期或撤销
2. OAuth 令牌失效
3. 网络连接问题

**解决方案：**

**对于 Anthropic (Claude)：**
```bash
# 重新认证
opencode auth login
# 选择 Anthropic → Claude Pro/Max
# 在浏览器中完成 OAuth
```

**对于 OpenAI (ChatGPT)：**
```bash
# 检查 API 密钥
opencode auth login
# 输入新的 API 密钥或完成 OAuth
```

**对于 Google Gemini：**
```bash
# 确保安装了 opencode-antigravity-auth
cat ~/.config/opencode/opencode.json | grep opencode-antigravity-auth

# 重新认证
opencode auth login
# 选择 Google → OAuth with Google (Antigravity)
```

---

### Q4: 安装程序不启动

**问题描述：** 运行 `bunx oh-my-opencode install` 没有反应或报错。

**解决方案：**

1. **检查 Bun 版本：**
```bash
bun --version  # 需要 >= 1.0.0
```

2. **手动安装（非交互模式）：**
```bash
bunx oh-my-opencode install --no-tui --verbose
```

3. **查看详细日志：**
```bash
bunx oh-my-opencode install --verbose 2>&1 | tee install.log
```

---

## 使用问题

### Q5: Ultrawork 模式不工作

**问题描述：** 在提示词中包含 `ultrawork` 或 `ulw` 没有任何反应。

**可能原因：**

1. **关键词检测器被禁用**
2. **Sisyphus 代理被禁用**
3. **提示词格式问题**

**解决方案：**

**检查钩子是否被禁用：**
```bash
cat ~/.config/opencode/oh-my-opencode.json | grep keyword-detector
# 如果在 disabled_hooks 中，移除它
```

**检查 Sisyphus 是否启用：**
```bash
cat ~/.config/opencode/oh-my-opencode.json | grep sisyphus_agent
# 确保 "disabled": false
```

**正确的提示词格式：**
```
✅ 正确：
ulw 添加用户认证功能

✅ 正确：
ultrawork: implement authentication

❌ 错误：
ulw implement authentication
# ↑ "ulw" 后需要冒号或空格
```

---

### Q6: Prometheus 计划不生成

**问题描述：** 按 Tab 进入 Prometheus 模式后没有生成计划。

**可能原因：**

1. **Prometheus 被禁用**
2. **规划器功能关闭**
3. **Prometheus 模式未激活**

**解决方案：**

**检查配置：**
```bash
cat ~/.config/opencode/oh-my-opencode.json | grep -A 5 sisyphus_agent
```

**确保：**
```json
{
  "sisyphus_agent": {
    "disabled": false,          // ← 必须是 false
    "planner_enabled": true      // ← 必须是 true
  }
}
```

**激活 Prometheus 模式：**
- 在 OpenCode 提示符中按 **Tab** 键
- 或使用 `/plan` 命令

---

### Q7: /start-work 命令不工作

**问题描述：** 输入 `/start-work` 没有反应或报错"找不到计划"。

**可能原因：**

1. **没有生成的计划**
2. **计划文件损坏**
3. **Atlas 协调器被禁用**

**解决方案：**

**检查计划文件：**
```bash
ls -la .sisyphus/plans/
# 应该看到 .md 文件
```

**检查 Atlas 配置：**
```bash
cat ~/.config/opencode/oh-my-opencode.json | grep -A 3 sisyphus_agent
# 确保 planner_enabled: true
```

**手动指定计划名：**
```bash
/start-work my-plan-name
```

---

### Q8: 任务卡住不前进

**问题描述：** 任务执行中途停止，代理说"完成"但实际没有完成。

**可能原因：**

1. **Todo Continuation Hook 被禁用**
2. **代理达到 token 限制**
3. **验证失败但未重试**

**解决方案：**

**检查 Todo Continuation Hook：**
```bash
cat ~/.config/opencode/oh-my-opencode.json | grep todo-continuation
# 不应该在 disabled_hooks 中
```

**手动恢复：**
```bash
# 查看当前状态
cat .sisyphus/boulder.json

# 继续执行
/start-work
# 会从上次停止的地方恢复
```

---

## 性能和成本

### Q9: Token 消耗过快

**问题描述：** 使用过程中 token 消耗速度异常快。

**可能原因：**

1. **使用昂贵模型做简单任务**
2. **没有正确配置 Category**
3. **背景代理并行度过高**
4. **没有启用截断优化**

**解决方案：**

**检查 Category 配置：**
```json
{
  "categories": {
    "quick": {
      "model": "anthropic/claude-haiku-4-5"  // ← 简单任务用便宜模型
    },
    "unspecified-low": {
      "model": "anthropic/claude-sonnet-4-5"  // ← 日常任务用中等模型
    }
  }
}
```

**启用输出截断：**
```json
{
  "experimental": {
    "truncate_all_tool_outputs": true,  // ← 截断所有工具输出
    "aggressive_truncation": true          // ← 激进截断模式
  }
}
```

**限制背景代理并发：**
```json
{
  "background_task": {
    "defaultConcurrency": 3,  // ← 降低默认并发数
    "providerConcurrency": {
      "anthropic": 2,  // ← 限制昂贵模型的并发
      "google": 5       // ← 允许便宜模型更高并发
    }
  }
}
```

---

### Q10: 成本优化技巧

**问题：** 希望降低 Oh My OpenCode 的使用成本。

**最佳实践：**

1. **正确使用 Category：**
```typescript
// ❌ 不好：所有任务都用 Opus
delegate_task(category="unspecified-high", prompt="fix typo")

// ✅ 好：简单任务用 Haiku
delegate_task(category="quick", prompt="fix typo")
```

2. **启用背景代理但控制并发：**
```json
{
  "background_task": {
    "defaultConcurrency": 3,  // 适度的并行
    "staleTimeoutMs": 300000  // ← 超时任务自动取消（5 分钟）
  }
}
```

3. **使用实验性优化：**
```json
{
  "experimental": {
    "dynamic_context_pruning": {
      "enabled": true,  // ← 自动清理旧上下文
      "turn_protection": {
        "enabled": true,
        "turns": 3  // ← 保护最近 3 轮对话
      }
    }
  }
}
```

4. **批量处理：**
```typescript
// ❌ 不好：每个小任务都启动一个会话
for (const file of files) {
  // 新会话... 高成本
}

// ✅ 好：在一个会话中批量处理
delegate_task(category="quick", prompt="Process all these files: " + files.join(", "))
```

---

## 模型和配置

### Q11: 如何切换不同 AI 提供者？

**问题：** 想从 Claude 切换到 OpenAI 或其他提供者。

**解决方案：**

**方法一：修改配置文件**
```json
{
  "agents": {
    "oracle": {
      "model": "openai/gpt-5.2"  // ← 切换到 OpenAI
    },
    "librarian": {
      "model": "glm-4.7"  // ← 切换到其他模型
    }
  }
}
```

**方法二：重新安装**
```bash
bunx oh-my-opencode install
# 在交互式安装中选择新的提供者
```

**重要提示：** 不需要重新认证，只要配置中指定的模型你有权限访问即可。

---

### Q12: Category 模型未生效

**问题描述：** 配置了 Category 的模型，但仍然使用默认模型。

**原因：** Category 需要明确添加到配置中，否则会使用系统默认模型。

**解决方案：**

**查看当前配置：**
```bash
cat ~/.config/opencode/oh-my-opencode.json | grep -A 10 categories
```

**添加 Category 配置：**
```json
{
  "categories": {
    "visual-engineering": {
      "model": "google/gemini-3-pro"  // ← 必须明确指定
    },
    "ultrabrain": {
      "model": "openai/gpt-5.2-codex",
      "variant": "xhigh"  // ← 可选：variant
    }
  }
}
```

**验证配置：**
```bash
bunx oh-my-opencode doctor --verbose
# 查看每个 Category 的实际解析模型
```

---

### Q13: 使用 Ollama 本地模型

**问题：** 想使用 Ollama 本地部署的模型。

**关键要求：** 对于 Ollama，**必须禁用流式传输**。

**配置示例：**
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

**为什么 `stream: false` 是必须的？**

Ollama 启用流式传输时返回 NDJSON（换行分隔的 JSON），但 Claude Code SDK 期望单个 JSON 对象。这导致 `JSON Parse error: Unexpected EOF` 错误。

**支持的 Ollama 模型：**

| 模型 | 最适合 | 配置 |
|-------|--------|--------|
| `ollama/qwen3-coder` | 代码生成、构建修复 | `{"model": "ollama/qwen3-coder", "stream": false}` |
| `ollama/ministral-3:14b` | 探索、代码库搜索 | `{"model": "ollama/ministral-3:14b", "stream": false}` |
| `ollama/lfm2.5-thinking` | 文档、写作 | `{"model": "ollama/lfm2.5-thinking", "stream": false}` |

---

## 错误和故障

### Q14: "JSON Parse error: Unexpected EOF"

**问题描述：** 代理尝试调用工具时出现 JSON 解析错误。

**可能原因：**

1. **使用 Ollama 但未禁用流式传输**
2. **模型输出损坏的 JSON**
3. **API 返回格式不正确**

**解决方案：**

**对于 Ollama：**
```bash
# 确保配置了 stream: false
cat ~/.config/opencode/oh-my-opencode.json | grep -A 3 ollama
```

**测试模型输出：**
```bash
curl -s http://localhost:11434/api/chat \
  -d '{"model": "qwen3-coder", "messages": [{"role": "user", "content": "Hello"}], "stream": false}'
```

**查看详细错误日志：**
```bash
# OpenCode 中运行时添加详细标志
opencode --verbose
```

---

### Q15: LSP 服务器不启动

**问题描述：** `lsp_diagnostics` 返回错误或没有结果。

**可能原因：**

1. **LSP 服务器未安装**
2. **配置文件错误**
3. **端口被占用**

**解决方案：**

**检查 LSP 状态：**
```bash
# 运行诊断
bunx oh-my-opencode doctor --category tools

# 或手动测试
typescript-language-server --stdio
```

**检查 LSP 配置：**
```bash
cat ~/.config/opencode/oh-my-opencode.json | grep -A 20 lsp
```

**常见的 LSP 配置问题：**
```json
// ❌ 错误：command 不是数组
{
  "lsp": {
    "typescript-language-server": "typescript-language-server --stdio"
  }
}

// ✅ 正确：command 是数组
{
  "lsp": {
    "typescript-language-server": {
      "command": ["typescript-language-server", "--stdio"],  // ← 必须是数组
      "extensions": [".ts", ".tsx"]
    }
  }
}
```

---

### Q16: 后台代理任务失败

**问题描述：** `delegate_task(background=true)` 任务失败或超时。

**可能原因：**

1. **超时设置过短**
2. **模型 API 问题**
3. **并发限制达到**

**解决方案：**

**调整超时设置：**
```json
{
  "background_task": {
    "staleTimeoutMs": 600000  // ← 增加到 10 分钟
  }
}
```

**检查任务状态：**
```bash
# 查看任务信息
background_output(task_id="bg_abc123")

# 如果失败，查看错误
```

**降低并发：**
```json
{
  "background_task": {
    "providerConcurrency": {
      "anthropic": 1,  // ← 严格限制
      "openai": 2
    }
  }
}
```

---

### Q17: Git Master 技能不工作

**问题描述：** Git 操作失败或不符合预期。

**可能原因：**

1. **技能被禁用**
2. **Git 未安装或配置错误**
3. **工作目录不是 Git 仓库**

**解决方案：**

**检查 Git 安装：**
```bash
git --version

# 配置 Git（如果需要）
git config --global user.email "your@email.com"
git config --global user.name "Your Name"
```

**检查技能配置：**
```bash
cat ~/.config/opencode/oh-my-opencode.json | grep disabled_skills
# 确保 "git-master" 不在禁用列表中
```

**确保在 Git 仓库中：**
```bash
# 检查当前目录
git status

# 如果不是仓库，初始化
git init
```

**手动测试 Git：**
```bash
# 测试基本操作
git add .
git commit -m "test commit"
git log -1
```

---

## 高级使用

### Q18: 如何自定义 Agent？

**问题：** 想添加自己的专业代理。

**解决方案：**

**方法一：修改配置文件**
```json
{
  "agents": {
    "my-custom-agent": {
      "model": "openai/gpt-5.2",
      "temperature": 0.3,
      "prompt": "You are a database expert...",
      "tools": {
        "bash": true,
        "read": true
      }
    }
  }
}
```

**方法二：使用 Category 系统**
```json
{
  "categories": {
    "database-expert": {
      "model": "openai/gpt-5.2",
      "prompt_append": "Focus on database design and optimization.",
      "description": "Database-related tasks"
    }
  }
}
```

**调用自定义代理：**
```typescript
// 通过委托工具
delegate_task(agent="my-custom-agent", prompt="...")

// 或通过 Category
delegate_task(category="database-expert", prompt="...")
```

---

### Q19: 如何创建自定义 Skill？

**问题：** 想添加自己的领域专业知识。

**解决方案：**

**创建 Skill 文件：**
```bash
# 在项目中创建技能
mkdir -p .opencode/skills/my-skill
touch .opencode/skills/my-skill/SKILL.md

# 或在用户目录中
mkdir -p ~/.claude/skills/my-skill
touch ~/.claude/skills/my-skill/SKILL.md
```

**Skill 文件格式：**
```markdown
---
name: my-skill
description: My custom skill description
mcp:
  my-mcp-server:
    command: npx
    args: ["-y", "my-mcp-server"]
---

# Skill Prompt Content

This content will be injected into agent's system prompt when this skill is loaded.

## Special Instructions

- Always follow these patterns...
- Never do this...
- Always verify...
```

**使用自定义 Skill：**
```typescript
delegate_task(
  category="visual-engineering",
  load_skills=["my-skill", "playwright"],
  prompt="Implement UI for..."
)
```

---

### Q20: 如何调试代理行为？

**问题：** 想了解代理在做什么以及为什么。

**解决方案：**

**方法一：使用诊断工具**
```bash
# 运行完整诊断
bunx oh-my-opencode doctor --verbose
```

**方法二：查看会话历史**
```bash
# 列出所有会话
session_list

# 读取特定会话
session_read --session_id=ses_abc123 --include_transcript
```

**方法三：检查学习记录**
```bash
# 查看累积的学习内容
cat .sisyphus/notepads/{plan-name}/learnings.md
```

**方法四：启用详细日志**
```json
{
  // 在 oh-my-opencode.json 中
  "agents": {
    "oracle": {
      "temperature": 0.3,
      "debug": true  // ← 如果代理支持
    }
  }
}
```

---

### Q21: 多项目如何管理配置？

**问题：** 有多个项目，需要不同的配置。

**解决方案：**

**配置优先级（从高到低）：**

1. **项目级配置：** `.opencode/oh-my-opencode.json`
2. **用户级配置：** `~/.config/opencode/oh-my-opencode.json`

**示例：**

**项目 A：**
```json
// .opencode/oh-my-opencode.json
{
  "categories": {
    "visual-engineering": {
      "model": "google/gemini-3-pro"  // ← 项目特定配置
    }
  }
}
```

**项目 B：**
```json
// .opencode/oh-my-opencode.json
{
  "categories": {
    "visual-engineering": {
      "model": "openai/gpt-5.2"  // ← 不同的配置
    }
  }
}
```

**全局配置：**
```json
// ~/.config/opencode/oh-my-opencode.json
{
  "agents": {
    "oracle": {
      "model": "openai/gpt-5.2"  // ← 所有项目共享
    }
  }
}
```

**项目 A 的实际配置：**
- Category: `google/gemini-3-pro`（项目特定）
- Oracle: `openai/gpt-5.2`（全局）

---

### Q22: 如何迁移配置到新机器？

**问题：** 在新机器上设置 Oh My OpenCode。

**解决方案：**

**方法一：复制配置文件**
```bash
# 从旧机器复制
scp ~/.config/opencode/oh-my-opencode.json user@new-machine:~/.config/opencode/

# 在新机器上
opencode --version  # 验证配置加载
```

**方法二：版本控制配置**
```bash
# 将配置添加到 Git 仓库
git init ~/.config/opencode
git add ~/.config/opencode/oh-my-opencode.json
git commit -m "Add oh-my-opencode config"

# 在新机器上克隆
git clone user@server:~/config-opencode.git
cp config-opencode/oh-my-opencode.json ~/.config/opencode/
```

**方法三：使用配置管理工具**
```bash
# 使用 stow 或类似的工具
stow --dotfiles -R ~/.config/opencode/oh-my-opencode ~

# 创建可分享的配置包
tar -czf oh-my-opencode-config.tar.gz .opencode/
```

---

## 其他常见问题

### Q23: 与其他 OpenCode 插件的兼容性

**问题：** Oh My OpenCode 是否与其他插件兼容？

**答案：** 大部分兼容，但需要注意：

**兼容：**
- ✅ MCP 服务器可以共存
- ✅ Claude Code 兼容的命令/技能/代理可以一起使用
- ✅ 钩子系统可以组合

**需要注意：**
- ⚠️ 不要使用多个"主协调器"插件
- ⚠️ 某些钩子可能冲突（如多个 Todo 管理器）

**建议配置：**
```json
{
  "claude_code": {
    "plugins_override": {
      "some-plugin": false  // ← 禁用冲突插件
    }
  }
}
```

---

### Q24: 如何报告 Bug 或请求功能？

**方法：**

1. **GitHub Issues：**
   - 提交到：https://github.com/code-yeongyu/oh-my-opencode/issues
   - 使用模板提供详细信息

2. **Discord 社区：**
   - 加入：https://discord.gg/PUwSMR9XNk
   - 获得快速帮助和讨论

3. **Twitter：**
   - 提及：@justsisyphus

**报告问题时请包括：**

- Oh My OpenCode 版本
- OpenCode 版本
- 操作系统
- 复现步骤
- 错误日志
- 配置文件（敏感信息可以移除）

---

### Q25: 如何保持系统更新？

**方法：**

**检查更新：**
```bash
# 使用诊断工具检查
bunx oh-my-opencode doctor --category updates
```

**自动更新通知：**
```json
{
  // 确保 auto-update-checker 钩子未被禁用
  "disabled_hooks": []
  // startup-toast 是 auto-update-checker 的子功能
  // 不要禁用 auto-update-checker，否则通知也会被禁用
}
```

**手动更新：**
```bash
# 更新 Oh My OpenCode
bunx oh-my-opencode@latest install

# 更新 OpenCode
npm install -g opencode@latest
# 或
bun install -g opencode@latest
```

---

## 总结

这个 FAQ 涵盖了 Oh My OpenCode 使用中最常见的问题：

- ✅ 安装和配置问题
- ✅ 使用模式和功能问题
- ✅ 性能和成本优化
- ✅ 模型和配置管理
- ✅ 错误排查和故障恢复
- ✅ 高级使用技巧

如果你遇到的问题不在这里：

1. **查看详细文档：**
   - [功能完整参考](../features/complete-reference.md)
   - [配置指南](../configurations.md)

2. **搜索 GitHub Issues：**
   - https://github.com/code-yeongyu/oh-my-opencode/issues?q=is%3Aissue

3. **加入社区：**
   - Discord: https://discord.gg/PUwSMR9XNk
   - 获得快速帮助

---

**祝你使用愉快！** 🚀
