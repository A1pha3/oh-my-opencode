---
summary: 全面介绍 Category（分类）和 Skill（技能）系统，包括内置分类说明、技能配置、委托机制和最佳实践
read_when:
  - 需要了解如何选择合适的代理类型
  - 配置自定义分类和技能时
  - 优化委托任务以获得最佳结果时
title: 分类与技能系统指南
---

# 分类与技能系统指南

本文档全面介绍 **Category（分类）** 和 **Skill（技能）** 系统，它们构成了 Oh-My-OpenCode 的扩展核心。

## 1. 概述

与其将所有工作委托给单个 AI 代理，不如根据任务的性质调用**专家**要高效得多。

- **Category**："这是什么类型的工作？"（确定模型、温度、提示心态）
- **Skill**："需要什么工具和知识？"（注入专业知识、MCP 工具、工作流）

通过结合这两个概念，您可以通过 `delegate_task` 生成最优代理。

---

## 2. 分类系统

Category 是针对特定领域优化的代理配置预设。

### 可用的内置分类

 | 类别 | 默认模型 | 用例 |
|------|----------|------|
| `visual-engineering` | `google/gemini-3-pro` | 前端、UI/UX、设计、样式、动画 |
| `ultrabrain` | `openai/gpt-5.2-codex`（xhigh） | 深度逻辑推理、需要广泛分析复杂架构决策 |
| `deep` | `openai/gpt-5.2-codex`（medium） | 目标导向的自主问题解决。行动前进行彻底研究。用于需要深度理解的棘手问题。 |
| `artistry` | `google/gemini-3-pro`（max） | 高度创意/艺术任务、新想法 |
| `quick` | `anthropic/claude-haiku-4-5` | 简单任务 - 单文件更改、拼写错误修复、简单修改 |
| `unspecified-low` | `anthropic/claude-sonnet-4-5` | 不适合其他分类的任务，低工作量要求 |
| `unspecified-high` | `anthropic/claude-opus-4-5`（max） | 不适合其他分类的任务，高工作量要求 |
| `writing` | `google/gemini-3-flash` | 文档、散文、技术写作 |

### 使用方法

调用 `delegate_task` 工具时指定 `category` 参数。

```typescript
delegate_task(
  category="visual-engineering",
  prompt="Add a responsive chart component to the dashboard page"
)
```

### Sisyphus-Junior（委托执行器）

当您使用 Category 时，一个名为 **Sisyphus-Junior** 的特殊代理执行工作。
- **特点**：不能将任务**重新委托**给其他代理。
- **目的**：防止无限委托循环，确保专注于分配的任务。

---

## 3. 技能系统

Skill 是一种机制，用于向代理注入特定领域的**专业知识（Context）**和**工具（MCP）**。

### 内置技能

1. **`git-master`**
   - **能力**：Git 专家。检测提交风格、拆分原子提交、制定 rebase 策略。
   - **MCP**：无（使用 Git 命令）
   - **使用**：对于提交、历史搜索、分支管理至关重要。

2. **`playwright`**
   - **能力**：浏览器自动化。网页测试、截图、抓取。
   - **MCP**：`@playwright/mcp`（自动执行）
   - **使用**：用于实现后的 UI 验证、E2E 测试编写。

3. **`frontend-ui-ux`**
   - **能力**：注入设计师心态。色彩、字体、动效指南。
   - **使用**：用于超越简单实现的美学 UI 工作。

### 使用方法

将所需的技能名称添加到 `load_skills` 数组中。

```typescript
delegate_task(
  category="quick",
  load_skills=["git-master"],
  prompt="Commit current changes. Follow commit message style."
)
```

### 技能自定义（SKILL.md）

您可以直接在项目根目录的 `.opencode/skills/` 或 home 目录的 `~/.claude/skills/` 中添加自定义技能。

**示例：`.opencode/skills/my-skill/SKILL.md`**

```markdown
---
name: my-skill
description: My special custom skill
mcp:
  my-mcp:
    command: npx
    args: ["-y", "my-mcp-server"]
---

# My Skill Prompt

This content will be injected into the agent's system prompt.
...
```

---

## 4. 组合策略（组合技）

您可以通过结合分类和技能来创建强大的专业代理。

### 🎨 设计师（UI 实现）
- **分类**：`visual-engineering`
- **load_skills**：`["frontend-ui-ux", "playwright"]`
- **效果**：实现美学 UI 并直接在浏览器中验证渲染结果。

### 🏗️ 架构师（设计审查）
- **分类**：`ultrabrain`
- **load_skills**：`[]`（纯推理）
- **效果**：利用 GPT-5.2 的逻辑推理进行深入系统架构分析。

### ⚡ 维护者（快速修复）
- **分类**：`quick`
- **load_skills**：`["git-master"]`
- **效果**：使用具有成本效益的模型快速修复代码并生成干净的提交。

---

## 5. delegate_task 提示指南

委托时，**清晰具体**的提示至关重要。包括这 7 个要素：

1. **TASK**：需要做什么？（单一目标）
2. **EXPECTED OUTCOME**：可交付成果是什么？
3. **REQUIRED SKILLS**：应该通过 `load_skills` 加载哪些技能？
4. **REQUIRED TOOLS**：必须使用哪些工具？（白名单）
5. **MUST DO**：必须做什么（约束）
6. **MUST NOT DO**：绝对不能做什么
7. **CONTEXT**：文件路径、现有模式、参考资料

**不良示例**：
> "修复这个"

**良好示例**：
> **TASK**：修复 `LoginButton.tsx` 中的移动端布局破坏问题
> **CONTEXT**：`src/components/LoginButton.tsx`，使用 Tailwind CSS
> **MUST DO**：在 `md:` 断点处更改 flex-direction
> **MUST NOT DO**：修改现有的桌面布局
> **EXPECTED**：按钮在移动端垂直对齐

---

## 6. 配置指南（oh-my-opencode.json）

您可以在 `oh-my-opencode.json` 中微调分类。

### 分类配置架构（CategoryConfig）

| 字段 | 类型 | 描述 |
|------|------|------|
| `description` | string | 分类用途的人工可读描述。在 delegate_task 提示中显示。 |
| `model` | string | 要使用的 AI 模型 ID（例如 `anthropic/claude-opus-4-5`） |
| `variant` | string | 模型变体（例如 `max`、`xhigh`） |
| `temperature` | number | 创造力级别（0.0 ~ 2.0）。越低越确定。 |
| `top_p` | number | 核采样参数（0.0 ~ 1.0） |
| `prompt_append` | string | 选择此分类时附加到系统提示的内容 |
| `thinking` | object | 思考模型配置（`{ type: "enabled", budgetTokens: 16000 }`） |
| `reasoningEffort` | string | 推理工作级别（`low`、`medium`、`high`） |
| `textVerbosity` | string | 文本详细程度级别（`low`、`medium`、`high`） |
| `tools` | object | 工具使用控制（用 `{ "tool_name": false }` 禁用） |
| `maxTokens` | number | 最大响应令牌数 |
| `is_unstable_agent` | boolean | 将代理标记为不稳定 - 强制后台模式进行监控 |

### 配置示例

```jsonc
{
  "categories": {
    // 1. 定义新的自定义分类
    "korean-writer": {
      "model": "google/gemini-3-flash",
      "temperature": 0.5,
      "prompt_append": "You are a Korean technical writer. Maintain a friendly and clear tone."
    },
    
    // 2. 覆盖现有分类（更改模型）
    "visual-engineering": {
      "model": "openai/gpt-5.2", // 可以更改模型
      "temperature": 0.8
    },

    // 3. 配置思考模型并限制工具
    "deep-reasoning": {
      "model": "anthropic/claude-opus-4-5",
      "thinking": {
        "type": "enabled",
        "budgetTokens": 32000
      },
      "tools": {
        "websearch_web_search_exa": false // 禁用网络搜索
      }
    }
  },
   
  // 禁用技能
  "disabled_skills": ["playwright"]
}
```
