---
summary: Oh-My-OpenCode 编排系统详解，介绍 Prometheus→Atlas→Junior 三层架构、规划与执行分离的设计哲学和工作流程
read_when:
  - 理解系统如何协调多个代理协同工作
  - 使用 Prometheus 规划复杂任务时
  - 优化多代理协作流程时
  - 需要精确控制任务执行流程时
title: 编排系统详解
---

# Oh-My-OpenCode 编排系统指南

## TL;DR - 何时使用什么

| 复杂度 | 方法 | 使用时机 |
|--------|------|----------|
| **简单** | 直接提示 | 简单任务、快速修复、单文件更改 |
| **复杂 + 懒** | 只需输入 `ulw` 或 `ultrawork` | 解释上下文繁琐的复杂任务。代理会自动搞清楚。 |
| **复杂 + 精确** | `@plan` → `/start-work` | 需要真正编排的精确、多步骤工作。Prometheus 制定计划，Atlas 执行。 |

**决策流程：**

```
这是快速修复还是简单任务？
  └─ 是 → 直接正常提示
  └─ 否  → 解释完整上下文是否繁琐？
             └─ 是 → 输入 "ulw" 让代理搞清楚
             └─ 否  → 是否需要精确、可验证的执行？
                        └─ 是 → 使用 @plan 进行 Prometheus 规划，然后 /start-work
                        └─ 否  → 只使用 "ulw"
```

---

本文档全面介绍实现 Oh-My-OpenCode 核心哲学的编排系统：**"规划与执行分离"**。

## 1. 概述

传统 AI 代理经常混合规划和执行，导致上下文污染、目标漂移和 AI 垃圾（低质量代码）。

Oh-My-OpenCode 通过清晰分离两个角色来解决这个问题：

1. **Prometheus（规划师）**：纯战略家，从不写代码。通过采访和分析建立完美的计划。
2. **Atlas（执行器）**：编排器，执行计划。将工作委托给专业代理，永不停止直到完成。

---

## 2. 整体架构

```mermaid
flowchart TD
    User[用户请求] --> Prometheus
    
    subgraph 规划阶段
        Prometheus[Prometheus<br>规划器] --> Metis[Metis<br>顾问]
        Metis --> Prometheus
        Prometheus --> Momus[Momus<br>审查员]
        Momus --> Prometheus
        Prometheus --> PlanFile["/.sisyphus/plans/{name}.md"]
    end
    
    PlanFile --> StartWork[//start-work/]
    StartWork --> BoulderState[boulder.json]
    
    subgraph 执行阶段
        BoulderState --> Atlas[Atlas<br>编排器]
        Atlas --> Oracle[Oracle]
        Atlas --> Frontend[前端<br>工程师]
        Atlas --> Explore[Explore]
    end
```

---

## 3. 关键组件

### 🔮 Prometheus（规划器）

- **模型**：`anthropic/claude-opus-4-5`
- **角色**：战略规划、需求采访、工作计划创建
- **约束**：**只读**。只能创建/修改 `.sisyphus/` 目录内的 markdown 文件。
- **特点**：从不直接写代码，专注于"怎么做"。

### 🦉 Metis（规划顾问）

- **角色**：预先分析和差距检测
- **功能**：识别隐藏的用户意图，防止 AI 过度工程，消除歧义。
- **工作流**：在创建计划之前必须进行 Metis 咨询。

### ⚖️ Momus（规划审查员）

- **角色**：高精度计划验证（高精度模式）
- **功能**：拒绝并要求修订，直到计划完美。
- **触发**：当用户请求"高精度"时激活。

### ⚡ Atlas（计划执行器）

- **模型**：`anthropic/claude-opus-4-5`（扩展思考 32k）
- **角色**：执行和委托
- **特点**：不直接做所有事情，积极将工作委托给专业代理（前端、Librarian 等）。

---

## 4. 工作流

### 第一阶段：采访和规划（采访模式）

Prometheus 默认以**采访模式**启动。它不会立即创建计划，而是收集足够的上下文。

1. **意图识别**：分类用户的请求是重构还是新功能。
2. **上下文收集**：通过 `explore` 和 `librarian` 代理调查代码库和外部文档。
3. **草稿创建**：不断将讨论内容记录到 `.sisyphus/drafts/` 中。

### 第二阶段：计划生成

当用户请求"生成计划"时，开始生成计划。

1. **Metis 咨询**：确认任何遗漏的需求或风险因素。
2. **计划创建**：在 `.sisyphus/plans/{name}.md` 文件中编写单个计划。
3. **交接**：计划创建完成后，指导用户使用 `/start-work` 命令。

### 第三阶段：执行

当用户输入 `/start-work` 时，执行阶段开始。

1. **状态管理**：创建 `boulder.json` 文件以跟踪当前计划和会话 ID。
2. **任务执行**：Atlas 读取计划并逐个处理 TODO。
3. **委托**：UI 工作委托给 Frontend 代理，复杂逻辑委托给 Oracle。
4. **连续性**：即使会话中断，工作也会通过 `boulder.json` 在下一个会话中继续。

---

## 5. 命令和使用

### `@plan [request]`

调用 Prometheus 开始规划会话。

- 示例：`@plan "我想将认证系统重构为 NextAuth"`

### `/start-work`

执行生成的计划。

- 功能：在 `.sisyphus/plans/` 中查找计划并进入执行模式。
- 如果有中断的工作，会自动从上次中断的地方继续。

---

## 6. 配置指南

您可以在 `oh-my-opencode.json` 中控制相关功能。

```jsonc
{
  "sisyphus_agent": {
    "disabled": false,           // 启用 Atlas 编排（默认：false）
    "planner_enabled": true,     // 启用 Prometheus（默认：true）
    "replace_plan": true         // 用 Prometheus 替换默认计划代理（默认：true）
  },
   
  // 钩子设置（添加到禁用列表）
  "disabled_hooks": [
    // "start-work",             // 禁用执行触发器
    // "prometheus-md-only"      // 移除 Prometheus 写入限制（不推荐）
  ]
}
```

## 7. 最佳实践

1. **不要着急**：在 Prometheus 的采访中投入足够的时间。计划越完美，执行越快。
2. **单一计划原则**：无论任务多大，将所有 TODO 包含在一个计划文件（`.md`）中。这可以防止上下文碎片化。
3. **积极委托**：在执行过程中，通过 `delegate_task` 将工作委托给专业代理，而不是直接修改代码。
