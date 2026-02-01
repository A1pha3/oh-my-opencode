# Oh My OpenCode 中文文档索引

欢迎来到 Oh My OpenCode 中文文档中心！

> 💡 **新手提示**：如果你是第一次接触这个系统，建议从[快速入门指南](./guide/quickstart.md)开始。

---

## 📚 文档导航

### 🚀 新手入门

| 文档 | 描述 | 适合人群 |
|-------|------|---------|
| [快速入门指南](./guide/quickstart.md) | 从零开始安装并使用 Oh My OpenCode | 完全新手 |
| [安装指南](./guide/installation.md) | 完整安装和身份验证配置 | 需要详细安装步骤的开发者 |

### 🏗️ 深度原理理解

| 文档 | 描述 |
|-------|------|
| [架构原理深度解析](./architecture/core-principles.md) | 从底层原理讲解系统的设计思想和工作机制 |
| [编排系统详解](./orchestration-guide.md) | Prometheus → Atlas → Junior 工作流详解 |
| [分类与技能系统](./category-skill-guide.md) | Category 和 Skill 系统的深度理解 |

### ⚙️ 配置与使用

| 文档 | 描述 |
|-------|------|
| [配置说明](./configurations.md) | 所有配置选项的详细说明 |
| [CLI 指南](./cli-guide.md) | 命令行工具完整参考 |
| [Ultrawork 宣言](./ultrawork-manifesto.md) | 项目核心哲学与设计原则 |

### 🎯 功能详解

| 文档 | 描述 |
|-------|------|
| [功能完整参考](./features.md) | 10+ 代理、32 个钩子、20+ 工具的完整说明 |
| [功能完整参考（旧版）](./features/complete-reference.md) | 10+ 代理、32 个钩子、20+ 工具的完整说明（参考版本） |

### 🔧 高级主题

| 文档 | 描述 |
|-------|------|
| [多模型编排](./features/complete-reference.md) | 如何优雅地混合使用多个 AI 模型（见功能参考） |
| [自定义配置](./best-practices/development.md) | 扩展系统以满足你的需求（见最佳实践） |
| [性能优化](./best-practices/development.md) | 提升效率、降低成本的实用技巧（见最佳实践） |

### 📖 最佳实践

| 文档 | 描述 |
|-------|------|
| [开发最佳实践](./best-practices/development.md) | 如何最高效地使用 Oh My OpenCode |
| [团队协作指南](./best-practices/development.md) | 在团队环境中部署和使用（见开发最佳实践） |
| [生产环境使用](./best-practices/development.md) | 在实际项目中稳定运行的指南（见开发最佳实践） |

### 🛠️ 故障排查

| 文档 | 描述 |
|-------|------|
| [常见问题解答](./troubleshooting/faq.md) | 频繁遇到的问题和解决方案 |
| [故障排除](./troubleshooting/faq.md) | 如何调试和诊断系统问题（见常见问题解答） |

---

## 🎯 快速开始

### 1. 安装

```bash
# 让 AI 助手帮你安装
# 将以下提示词复制到 Claude Code、Cursor 等 AI 工具中：
```
请按照这里的说明安装并配置 oh-my-opencode：
https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/guide/installation.md
```

# 或者手动安装
bunx oh-my-opencode install
```

### 2. 三种使用方式

#### 方式一：Ultrawork 模式（懒人必备）

只需要在提示词中包含 `ultrawork` 或 `ulw`：

```
ulw 为我的 Next.js 应用添加用户认证功能
```

代理会自动：
1. 探索你的代码库，理解现有模式
2. 研究最佳实践
3. 按照你的约定实现功能
4. 运行测试验证
5. 持续工作直到完成

**这是"全自动"模式。你什么都不用想。代理会帮你思考。**

#### 方式二：Prometheus 规划模式（精确控制）

对于复杂或关键任务，按 **Tab** 键切换到 Prometheus（规划器）模式：

1. **Prometheus 采访你** - 作为你的私人顾问，通过提问来明确需求
2. **生成工作计划** - 基于采访生成详细的任务清单
3. **运行 `/start-work`** - Atlas 协调执行任务，直到完成

**何时使用 Prometheus：**
- 跨天或跨会话的项目
- 关键的生产环境变更
- 涉及多个文件的复杂重构

#### 方式三：直接对话（快速修复）

对于简单任务，直接描述即可：

```
修复 LoginButton.tsx 中的布局问题
```

---

## 🤔 核心理念

Oh My OpenCode 的核心设计哲学是：**规划与执行分离**

传统 AI 工具往往混淆这两者，导致：
- 上下文污染（规划细节混入执行）
- 目标漂移（执行过程中偏离原始需求）
- 质量参差不齐（没有验证机制）

Oh My OpenCode 通过清晰分离三个角色来解决这个问题：

1. **Prometheus（规划师）**：只负责"怎么做"
2. **Atlas（协调器）**：负责调度和验证
3. **Junior（执行者）**：只负责"把代码写出来"

更多关于设计哲学的内容，请阅读 [Ultrawork 宣言](../ultrawork-manifesto.md)。

---

## 🌟 核心特性

- 🤖 **10 个专业 AI 代理**：Sisyphus、Prometheus、Oracle、Librarian、Explore、Multimodal Looker 等
- 🧠 **32 个生命周期钩子**：在每个关键点注入自定义逻辑
- 🛠️ **20+ 专业工具**：LSP、AST-Grep、委托系统等
- 🎭 **完整 Claude Code 兼容**：命令、技能、代理、MCP、钩子
- ⚡ **后台代理系统**：并行运行多个代理，像真实开发团队一样工作
- 📋 **智能任务管理**：自动跟踪任务进度，强制完成

---

## 📖 推荐阅读路径

### 完全新手路径

```
1. 快速入门指南 → 了解基本安装和三种使用方式
2. 安装指南 → 理解系统能做什么
3. 功能详解 → 理解核心工作流
4. 配置指南 → 根据你的需求定制系统
```

### 想要深入理解

```
1. 架构原理深度解析 → 从底层理解设计思想
2. 功能完整参考 → 掌握委托机制
3. 最佳实践 → 学习自定义和扩展
```

### 实际项目使用

```
1. 最佳实践 → 学习高效工作流
2. 功能详解 → 了解所有可用工具
3. 故障排查 → 解决遇到的问题
```

---

## 💬 获取帮助

- **GitHub Issues**: [提交问题](https://github.com/code-yeongyu/oh-my-opencode/issues)
- **Discord 社区**: [加入讨论](https://discord.gg/PUwSMR9XNk)
- **Twitter**: [@justsisyphus](https://x.com/justsisyphus)

---

## 📄 许可证

本项目使用 [SUL-1.0](https://github.com/code-yeongyu/oh-my-opencode/blob/master/LICENSE.md) 许可证。

---

> **注意**：如果你发现文档有任何问题或有改进建议，欢迎提交 PR！
