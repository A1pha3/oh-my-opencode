# Oh My OpenCode 最优模型配置策略指南

> 📖 **本文档适合**：希望根据自身模型资源定制配置的高级用户
> ⏱️ **预计阅读时间**：15 分钟
> ✅ **本文档目标**：帮助用户理解最优配置的设计原理，并提供可直接使用的配置模板

---


## 一、设计原则

### 1.1 核心理念：分层调度与并行分流

本配置策略的核心设计理念是「**分层调度**」与「**并行分流**」的有机结合。通过将不同复杂度的任务分配给最适合的模型，我们能够在保证任务质量的同时，最大化模型额度的利用效率。

```
┌─────────────────────────────────────────────────────────────────────┐
│              Claude Opus 4.5 Thinking (antigravity)                  │
│              Claude Opus 4.5 (github-copilot)                       │
│              GPT-5.2 (github-copilot)                               │
│              （最强推理 · 战略储备 - 多账户/订阅充足）                  │
├─────────────────────────────────────────────────────────────────────┤
│  GPT-5.2-codex (github-copilot) ←→ MiniMax-M2.1 (会员充足)          │
│  （Hephaestus 强制）         （主力开发）                             │
├─────────────────────────────────────────────────────────────────────┤
│  GLM-4.7 (会员充足) ←→ Claude Haiku 4.5 (订阅充足)                   │
│  （中文/文档）              （快速响应 · explore 最佳）               │
├─────────────────────────────────────────────────────────────────────┤
│  Gemini 3 Pro/Flash (github-copilot)                               │
│  （前端专用 · 多模态专用）                                           │
└─────────────────────────────────────────────────────────────────────┘
```

分层调度的核心思想是将模型按照能力强度分为多个层级：

- **战略储备层**：Claude Opus 4.5 / GPT-5.2，仅用于最关键的决策场景（Hephaestus、oracle、ultrabrain）
- **核心执行层**：GPT-5.2-codex + MiniMax-M2.1，承担日常开发的主体任务
- **并行辅助层**：GLM-4.7 + Claude Haiku 4.5，与核心模型分担不同类型的任务
- **专业职能层**：Gemini 系列，专注于前端和多模态任务

这种分层设计确保了「杀鸡不用牛刀」的资源配置原则，避免将强大的模型浪费在简单任务上，同时也避免了让弱小的模型承担无法胜任的工作。

### 1.2 四大设计原则

本配置策略遵循以下四大设计原则，这些原则共同构成了最优配置的理论基础。

| 原则 | 说明 | 实践方式 |
|------|------|----------|
| **能力匹配** | 任务复杂度与模型能力对应 | 简单任务用轻量模型，复杂任务用强模型 |
| **额度保护** | 稀缺资源只用于关键决策点 | Claude/GPT-5 只用于 Hephaestus、ultrabrain 和 oracle |
| **并行分流** | MiniMax、GLM、Haiku 分担不同类型任务 | librarian 用 GLM，explore 用 Haiku，核心开发用 MiniMax |
| **专长发挥** | 利用各模型特长 | Gemini 做前端，GLM 做中文，Haiku 做快速搜索 |

**能力匹配原则**体现在每个 Agent 和 Category 的配置上。我们根据任务的实际复杂度来选择模型，而不是简单地使用最强的模型。例如，代码搜索任务（explore）使用轻量级的 Claude Haiku 4.5，而架构咨询任务（oracle）则使用最强的 Claude Opus 4.5。这种差异化的配置确保了资源的最优利用。

**额度保护原则**是本配置策略的核心考量之一。Claude Opus 和 GPT-5.2 作为最强模型，其额度需要精打细算，因此我们将其使用范围严格限制在真正需要最强推理能力的场景（Hephaestus、ultrabrain、oracle）。通过精确的场景定义，我们确保每一次强模型调用都是值得的。

**并行分流原则**解决了单一模型可能面临的过载问题。通过将不同类型的任务分配给不同的主力模型，我们实现了任务的并行处理，避免了任何单一模型的额度被快速耗尽。MiniMax 负责日常开发，GLM 负责中文和文档任务，Claude Haiku 负责快速搜索，三者相互补充，形成了稳定的多核心架构。

**专长发挥原则**要求我们深入理解每个模型的特长，并在最适合的场景中使用它们。Gemini 系列在视觉任务和多模态处理方面具有明显优势，因此我们将其专门用于前端开发和图片分析场景。GLM 在中文理解和文档写作方面表现出色，因此我们将其用于中文文档搜索和写作任务。Claude Haiku 4.5 在响应速度上具有优势，因此我们将其用于高频的代码搜索场景。

### 1.3 设计原理的底层逻辑

本配置策略的设计并非凭空想象，而是基于对底层代码机制的深入理解。Oh My OpenCode 的模型调度系统包含三个核心组件：Agent 配置系统、Category 配置系统和 Fallback 链机制。

Agent 配置系统控制着内置 Agent（Sisyphus、Oracle、Librarian 等）的模型选择。系统允许用户通过配置文件覆盖默认模型，但某些 Agent（如 Hephaestus）具有强制性的模型要求，无法通过配置修改。Category 配置系统则控制着 `delegate_task(category="xxx")` 的模型选择，两者相互独立。

Fallback 链机制是系统弹性的关键。每个 Agent 和 Category 都定义了 Fallback 链，当首选模型不可用时，系统会自动降级到备选模型。理解这一机制对于配置优化至关重要，因为它决定了配置在异常情况下的行为。

---


## 二、模型资源清单

### 2.1 用户可用模型资源

根据您提供的模型资源情况，以下是完整的可用模型清单及其定位。

| 模型 | Provider | 额度情况 | 用途定位 | 特长 |
|------|----------|----------|----------|------|
| Claude Opus 4.5 Thinking | google/antigravity | 充足（多账户轮换） | 最强推理 | 复杂架构设计、深度逻辑推理 |
| Claude Opus 4.5 | github-copilot | 充足（订阅） | 最强推理 | 复杂架构设计、深度逻辑推理 |
| GPT-5.2 | github-copilot | 充足（订阅） | 强力推理 | 深度编码、复杂调试 |
| GPT-5.2-codex | github-copilot | 充足（订阅） | 深度编码 | **Hephaestus 强制要求**、自主编码 |
| MiniMax-M2.1 | minimax-cn-coding-plan | 充足（会员） | 主力开发 | 通用代码生成、快速响应 |
| GLM-4.7 | zhipuai-coding-plan | 充足（会员） | 并行辅助 | 中文理解、文档写作 |
| Claude Haiku 4.5 | github-copilot | 充足（订阅） | 快速搜索 | 快速响应、轻量级代码搜索 |
| Gemini 3 Pro Preview | github-copilot | 充足（订阅） | 专业职能 | 前端/UI、创意设计 |
| Gemini 3 Flash Preview | github-copilot | 充足（订阅） | 专业职能 | 图片分析、快速响应 |

### 2.2 模型能力评估

为了更好地理解不同模型的适用场景，我们从多个维度对可用模型进行了能力评估。

```
推理能力：Claude Opus ≈ GPT-5.2 > MiniMax-M2.1 ≈ GLM-4.7 > Claude Haiku > Gemini
代码能力：GPT-5.2-codex > Claude Opus > MiniMax-M2.1 > GLM-4.7 > Claude Haiku
前端能力：Gemini 3 Pro > Claude Opus > MiniMax-M2.1 > GLM-4.7
中文能力：GLM-4.7 > MiniMax-M2.1 > Claude Opus
多模态能力：Gemini 3 Flash > Gemini 3 Pro > GLM-4.7 > Claude Opus
响应速度：Claude Haiku > Gemini 3 Flash > MiniMax-M2.1 > GLM-4.7 > Claude Opus
额度充裕度：MiniMax ≈ GLM ≈ Claude Haiku ≈ Gemini > Claude/GPT-5（需轮换）
```

从推理能力来看，Claude Opus 和 GPT-5.2 处于同一水平，但这并不意味着所有任务都应该使用它们。MiniMax-M2.1 在代码能力上表现出色，足以应对绝大多数日常开发任务。Claude Haiku 4.5 虽然推理能力较弱，但在响应速度和轻量级任务（如代码搜索）上具有明显优势。GLM-4.7 在中文能力上的优势使其成为处理中文文档和搜索任务的最佳选择。Gemini Pro 在前端能力上的优势则使其成为 UI/UX 开发的不二之选。

### 2.3 特殊模型要求说明

在配置模型时，需要特别注意以下特殊要求，这些要求来自底层代码的强制约束。

**强制模型要求**（无法通过配置修改）：

| 组件 | 强制要求 | 影响 |
|------|----------|------|
| **Hephaestus** | `openai/gpt-5.2-codex` | 无 Fallback 链，必须有该模型才能使用 |
| **Category deep** | `openai/gpt-5.2-codex` | 无此模型则 Category 不激活 |
| **Category artistry** | `google/gemini-3-pro` | 无此模型则 Category 不激活 |

**无 Fallback 链的 Agent**（主模型不可用则任务失败）：

| Agent | 影响 |
|-------|------|
| oracle | 无 Fallback 链，配置的主模型必须可用 |
| multimodal-looker | 无 Fallback 链，配置的主模型必须可用 |

理解这些特殊要求对于避免配置陷阱至关重要。您拥有 gpt-5.2-codex 的访问权限，因此 Hephaestus 和 deep Category 可以正常使用。gemini-3-pro-preview 满足 artistry 的强制要求，因此该 Category 也可正常使用。

---


## 三、Agent 分工策略

### 3.1 Agent 职责与模型分配

以下是针对您的模型资源情况设计的 Agent 最优配置方案。

| Agent | 职责 | 推荐模型 | 分配理由 |
|-------|------|----------|----------|
| **sisyphus** | 主 orchestrator，协调全局 | MiniMax-M2.1 | 调用最频繁，需要充足额度，主力模型首选 |
| **explore** | 代码库快速搜索 | Claude Haiku 4.5 | 高频调用，需要快速响应，Haiku 轻量且高效 |
| **librarian** | 外部文档/GitHub 搜索 | GLM-4.7 | 中文文档搜索优势，分流 MiniMax 压力 |
| **oracle** | 架构咨询、复杂调试 | Claude Opus 4.5 (antigravity) | 关键决策点，需要最强推理能力，多账户保障可用性 |
| **hephaestus** | 深度自主编码 | GPT-5.2-codex | **强制要求**，无 Fallback，代码能力最强 |
| **prometheus** | 任务规划 | MiniMax-M2.1 | 规划流程核心，需要稳定响应 |
| **metis** | 规划前分析 | GLM-4.7 | 与 prometheus 并行，分流到 GLM 减少主模型压力 |
| **momus** | 规划审核 | Claude Haiku 4.5 | 快速审核反馈，需要即时响应 |
| **atlas** | TODO 管理 | MiniMax-M2.1 | 项目管理核心，稳定可靠 |
| **multimodal-looker** | 图片/PDF 分析 | Gemini 3 Flash | 多模态专长，快速响应 |

### 3.2 Hephaestus 配置说明

Hephaestus 是一个特殊的 Agent，其代码中强制要求使用 `openai/gpt-5.2-codex` 模型，且无 Fallback 链。这意味着：

- 如果您没有 gpt-5.2-codex 的访问权限，Hephaestus 将无法工作
- 配置文件中对 Hephaestus 的模型覆盖不会生效
- 系统会自动检测并仅在 gpt-5.2-codex 可用时启用 Hephaestus

**好消息**：您拥有 gpt-5.2-codex，因此 Hephaestus 可以正常使用。

**建议**：由于 Hephaestus 是唯一使用 gpt-5.2-codex 的组件，建议在 ultrawork 模式的高复杂度任务中优先使用 Hephaestus，以充分利用这一最强编码模型的能力。

### 3.3 Oracle 配置说明

Oracle 用于架构咨询和复杂调试，是本配置策略中最重要的决策支持 Agent。

选择 Claude Opus 4.5 (antigravity) 基于以下考量：

- 架构决策对项目成功至关重要，需要最强推理能力
- Oracle 的调用频率相对较低，多账户轮换机制确保额度充足
- 复杂调试场景通常涉及多层次逻辑推理，Claude 的深度思考能力最为适合
- 多账户机制提供了额外的可用性保障

**备选方案**：如果 antigravity 账户出现额度问题，可以临时切换到 github-copilot 的 Claude Opus 4.5。

### 3.4 Explore Agent 的最佳选择：Claude Haiku 4.5

在本配置中，我们将 explore Agent 分配给 Claude Haiku 4.5 而不是 MiniMax-M2.1，这是基于以下考量：

- **高频调用**：explore 是最高频调用的 Agent 之一，每次代码搜索都会触发
- **响应速度**：Haiku 响应速度最快，适合「搜索-查看-再搜索」的快速迭代模式
- **轻量级任务**：代码搜索不需要深度推理，Haiku 的能力完全足够
- **额度保护**：将 Haiku 用于搜索，释放 MiniMax 额度用于更重要的开发任务

**配置优势**：
```
explore (Claude Haiku): 快速响应，额度充足
sisyphus/prometheus (MiniMax): 深度开发，充足额度
librarian (GLM): 中文文档，分流压力
```

### 3.5 并行执行示例

以下展示 ultrawork 模式下多 Agent 并行执行的实际流程：

```
用户："ultrawork 完成用户认证功能"

sisyphus (MiniMax) ─────────────────────────────────────────────────►
    │
    ├── explore (Claude Haiku) ──► 搜索现有代码 ──┐
    │                                           │
    ├── librarian (GLM) ────► 查找 JWT 文档 ─────┼─► 并行执行
    │                                           │
    └── oracle (Claude Opus) ──► 架构建议 ───────┘
                                      │
                                      ▼
                            hephaestus (GPT-5.2-codex) ──► 编码实现
```

此流程展示了并行分流的实际效果：explore 和 librarian 同时进行代码库搜索和文档研究，oracle 提供架构建议，最后由 hephaestus 完成编码实现。这种并行模式大大提高了执行效率。

---


## 四、Category 分工策略

### 4.1 Category 职责与模型分配

Category 用于 `delegate_task(category="xxx")` 的任务分发，与 Agent 配置相互独立。

| Category | 复杂度 | 推荐模型 | 使用场景 |
|----------|--------|----------|----------|
| **quick** | 低 | Claude Haiku 4.5 | 单文件修改、typo 修复、简单重构 |
| **unspecified-low** | 中低 | MiniMax-M2.1 | 不适合其他 Category 的小任务 |
| **unspecified-high** | 中高 | MiniMax-M2.1 | 不适合其他 Category 的大任务 |
| **ultrabrain** | 极高 | Claude Opus 4.5 (antigravity) | 复杂逻辑、算法设计、系统架构 |
| **deep** | 高 | GPT-5.2-codex | 深度自主任务，**强制要求** |
| **visual-engineering** | 中 | Gemini 3 Pro Preview | 前端/UI/动画、设计相关任务 |
| **artistry** | 中高 | Gemini 3 Pro Preview | 创意写作、非常规解决方案 |
| **writing** | 中 | GLM-4.7 | 文档、README、技术文章 |

### 4.2 deep Category 与 ultrabrain Category 的区别

deep 和 ultrabrain 都是用于复杂任务的 Category，但它们的定位有所不同：

- **ultrabrain**：用于「极高复杂度」任务，如复杂算法设计、系统架构决策、跨模块重构等。默认使用 Claude Opus 4.5 (antigravity)，确保最强推理能力。适用于需要深度思考的战略性问题。

- **deep**：用于「高复杂度」任务，如需要深度自主研究的 bug 修复、特性实现等。默认使用 GPT-5.2-codex，这是代码能力最强的模型。适用于需要自主研究和实现的编码任务。

**选择建议**：

- 对于需要深度思考的架构问题，选择 ultrabrain
- 对于需要自主研究的实现问题，选择 deep
- **您同时拥有两种模型，因此可以充分发挥各自优势**

### 4.3 visual-engineering 与 artistry 的区别

visual-engineering 和 artistry 都与创意相关，但适用场景不同：

- **visual-engineering**：专门用于前端开发、UI 设计、动画实现等需要视觉输出的任务。默认使用 Gemini 3 Pro Preview，充分发挥其在视觉任务上的优势。

- **artistry**：用于创意写作、非常规解决方案探索等非视觉创意任务。默认使用 Gemini 3 Pro Preview（满足强制要求），也可用于需要创意视角的技术问题解决。

**选择建议**：

- 前端/CSS/UI 任务选择 visual-engineering
- 需要创意视角的问题解决选择 artistry

### 4.4 quick Category 的最佳选择：Claude Haiku 4.5

quick Category 用于最简单的任务，如单文件修改、typo 修复、简单重构等。使用 Claude Haiku 4.5 是最佳选择：

- **任务简单**：quick 任务不需要深度推理，Haiku 能力完全足够
- **高频使用**：quick 是最常用的 Category，Haiku 的快速响应优势明显
- **额度保护**：使用 Haiku 可以节省 MiniMax 额度用于更重要的任务

---


## 五、完整配置示例

### 5.1 推荐配置文件

以下配置直接复制到 `~/.config/opencode/oh-my-opencode.json` 或 `.opencode/oh-my-opencode.json` 即可使用：

```json
{
  "agents": {
    "sisyphus": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "explore": {
      "model": "github-copilot/claude-haiku-4.5"
    },
    "librarian": {
      "model": "zhipuai-coding-plan/glm-4.7"
    },
    "oracle": {
      "model": "google/antigravity/claude-opus-4-5-thinking"
    },
    "hephaestus": {
      "model": "github-copilot/gpt-5.2-codex"
    },
    "prometheus": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "metis": {
      "model": "zhipuai-coding-plan/glm-4.7"
    },
    "momus": {
      "model": "github-copilot/claude-haiku-4.5"
    },
    "atlas": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "multimodal-looker": {
      "model": "github-copilot/gemini-3-flash-preview"
    }
  },
  "categories": {
    "quick": {
      "model": "github-copilot/claude-haiku-4.5"
    },
    "unspecified-low": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "unspecified-high": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "ultrabrain": {
      "model": "google/antigravity/claude-opus-4-5-thinking"
    },
    "deep": {
      "model": "github-copilot/gpt-5.2-codex"
    },
    "visual-engineering": {
      "model": "github-copilot/gemini-3-pro-preview"
    },
    "artistry": {
      "model": "github-copilot/gemini-3-pro-preview"
    },
    "writing": {
      "model": "zhipuai-coding-plan/glm-4.7"
    }
  }
}
```

### 5.2 配置说明

**agents 配置段**控制内置 Agent 的模型选择，**categories 配置段**控制 Category 任务的模型分配。两者相互独立，分别作用于不同的任务分发场景。

配置覆盖规则：

- 配置文件中的设置会覆盖内置的 Fallback 链
- 优先使用配置中指定的模型
- 如果配置模型不可用，Fallback 链才会生效（部分 Agent 无 Fallback）

**关键配置说明**：

| 配置项 | 模型 | 说明 |
|--------|------|------|
| explore | claude-haiku-4.5 | 快速搜索，高频调用首选 |
| oracle | claude-opus-4-5-thinking (antigravity) | 战略决策，多账户保障 |
| hephaestus | gpt-5.2-codex | 强制要求，深度编码 |
| deep | gpt-5.2-codex | 强制要求，深度任务 |
| quick | claude-haiku-4.5 | 轻量任务，快速响应 |
| multimodal-looker | gemini-3-flash-preview | 多模态，快速响应 |

---


## 六、调优建议

### 6.1 额度分配预估

根据上述配置，各模型的使用比例预估如下：

```
MiniMax-M2.1:      35% （核心开发、规划、管理）
Claude Haiku:      25% （搜索、审核、轻量任务 - 新增！）
GLM-4.7:           15% （文档、规划辅助、中文任务）
GPT-5.2-codex:     10% （Hephaestus、deep - 强制使用）
Claude Opus:        5% （ultrabrain、oracle - 战略储备）
Gemini:            10% （前端、多模态）
```

此分配比例基于以下假设：

- Claude Haiku 的加入显著降低了 MiniMax 的压力，用于高频的搜索和轻量任务
- Hephaestus 和 deep 固定使用 gpt-5.2-codex，占用 10% 额度
- 中文文档和写作任务由 GLM 承担
- 前端和多模态任务由 Gemini 系列承担
- 最强模型 Claude 仅用于真正需要深度推理的场景

### 6.2 场景化使用建议

| 场景 | 触发条件 | 使用模型 | 说明 |
|------|----------|----------|------|
| 日常开发 | 默认 | MiniMax-M2.1 | sisyphus 自动使用 |
| 代码搜索 | explore agent | Claude Haiku 4.5 | 快速响应，新增推荐 |
| 文档搜索 | librarian agent | GLM-4.7 | 中文优势 |
| 规划分析 | metis/momus agent | GLM-4.7 / Claude Haiku | 并行分工 |
| 架构咨询 | oracle agent | Claude Opus (antigravity) | 关键决策 |
| 逻辑难题 | ultrabrain category | Claude Opus (antigravity) | 深度推理 |
| 深度编码 | hephaestus/deep | GPT-5.2-codex | 强制使用 |
| 前端任务 | visual-engineering | Gemini 3 Pro | 视觉专长 |
| 图片分析 | multimodal-looker | Gemini 3 Flash | 多模态专长 |
| 文档写作 | writing category | GLM-4.7 | 中文写作 |
| 快速修复 | quick category | Claude Haiku 4.5 | 轻量任务 |

### 6.3 常见调优场景

**场景一：Claude Haiku 表现不佳**

如果发现 explore 或 quick 任务质量不理想，可以将部分任务切换到 MiniMax：

```json
"explore": { "model": "minimax-cn-coding-plan/MiniMax-M2.1" },
"quick": { "model": "minimax-cn-coding-plan/MiniMax-M2.1" }
```

**场景二：antigravity 额度紧张**

如果 antigravity 账户额度告急，可以切换到 github-copilot 的 Claude Opus：

```json
"oracle": { "model": "github-copilot/claude-opus-4.5" },
"ultrabrain": { "model": "github-copilot/claude-opus-4.5" }
```

**场景三：需要更强的 deep 能力**

如果 deep 任务需要更强的推理能力（使用 Claude 替代）：

```json
"deep": { "model": "google/antigravity/claude-opus-4-5-thinking" }
```

注意：此配置会显著增加 Claude 额度消耗，且 deep 任务的 gpt-5.2-codex 强制要求可能不生效。

**场景四：Gemini Pro 额度紧张**

如果 Gemini 3 Pro 额度告急，可以将 visual-engineering 切换到 Claude：

```json
"visual-engineering": { "model": "github-copilot/claude-opus-4.5" }
```

但请注意：artistry 需要 gemini-3-pro，切换后可能影响该 Category 的可用性。

---


## 七、重要限制说明

### 7.1 强制模型要求

以下 Agent/Category 具有强制性的模型要求，无法通过配置覆盖：

| 名称 | 强制要求 | 您的资源情况 |
|------|----------|--------------|
| Hephaestus | gpt-5.2-codex | ✅ 拥有，可正常使用 |
| Category deep | gpt-5.2-codex | ✅ 拥有，可正常使用 |
| Category artistry | gemini-3-pro | ✅ 拥有 gemini-3-pro-preview，满足要求 |

### 7.2 无 Fallback 的组件

以下组件在配置模型不可用时任务会直接失败，无自动降级：

| 组件 | 影响 | 建议 |
|------|------|------|
| oracle | 如果配置模型不可用，咨询任务失败 | 保持 antigravity 和 github-copilot 双配置 |
| multimodal-looker | 如果配置模型不可用，图片分析任务失败 | Gemini Flash 有备用可用性 |
| Hephaestus | 无 gpt-5.2-codex 则完全不可用 | 您已拥有，无需担心 |
| deep | 无 gpt-5.2-codex 则 Category 不激活 | 您已拥有，无需担心 |

### 7.3 配置优先级

模型选择的优先级顺序如下：

1. **Category 优先**：如果任务通过 Category 分发，先使用 Category 配置
2. **Agent 覆盖**：Agent 配置会覆盖 Category 的默认模型
3. **Fallback 链**：如果配置模型不可用，尝试 Fallback 链中的备选模型
4. **系统默认**：如果 Fallback 链全部不可用，使用系统默认模型

理解这一优先级顺序对于调试配置问题至关重要。

---


## 八、监控与调整

### 8.1 额度监控建议

定期检查各模型额度消耗情况：

- **MiniMax 控制台**：查看 MiniMax-M2.1 使用量
- **智谱 AI 控制台**：查看 GLM-4.7 使用量
- **Google Cloud 控制台**：查看 Claude（Antigravity）和 Gemini 使用量
- **GitHub Copilot 控制台**：查看 Claude Opus/GPT-5.2/Claude Haiku 使用量

### 8.2 配置调整周期

建议每两周审视一次配置效果，关注以下指标：

- Claude Haiku 的使用频率是否符合预期（explore/quick）
- Hephaestus 的调用是否正常（Hephaestus 必须使用 gpt-5.2-codex）
- 是否有任务因模型不可用而失败
- 是否有模型额度出现异常消耗

根据实际使用情况，适时调整配置以达到最优效果。

---


## 九、总结

本配置策略的核心是「**分层调度 + 并行分流 + 强制要求适配**」：

1. **Claude Opus** 作为「战略储备」，只在 ultrabrain 和 oracle 场景使用，通过 antigravity 多账户保障可用性
2. **GPT-5.2-codex** 作为「深度编码核心」，Hephaestus 和 deep Category 的强制要求
3. **MiniMax** 作为「主力军」，承担日常开发任务的主体
4. **Claude Haiku 4.5** 作为「快速响应引擎」，专用于 explore、quick 等高频轻量任务（新增优化）
5. **GLM** 作为「辅助队」，与 MiniMax 并行分担中文和文档任务
6. **Gemini** 作为「专业队」，专注前端和多模态任务

**您的模型资源组合优势**：

- ✅ 拥有 gpt-5.2-codex → Hephaestus 和 deep 可正常使用
- ✅ 拥有 claude-haiku-4.5 → explore 和 quick 任务可以更快速、更省额度
- ✅ 拥有 claude-opus-4-5-thinking (antigravity) → 多账户保障战略储备可用性
- ✅ 拥有 claude-opus-4.5 (github-copilot) → 备用最强推理能力

遵循本文档的配置策略，您可以在保证任务质量的同时，最大化模型额度的利用效率，实现可持续的高效开发流程。

---


*本文档根据用户模型资源情况定制优化。*
