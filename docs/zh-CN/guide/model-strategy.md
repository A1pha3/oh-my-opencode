# Oh My OpenCode 最优模型配置策略指南

> 📖 **本文档适合**：追求经济实惠、高性价比配置的高级用户
> ⏱️ **预计阅读时间**：20 分钟
> ✅ **本文档目标**：综合最优配置，实现成本与能力的最佳平衡
> 📅 **最后更新**：2026-02-03
> ⚡ **核心原则**：GitHub Copilot 额度严格保护 + 充足额度模型最大化利用

---

## 一、设计原则

### 1.1 核心理念：额度充足模型最大化 + 免费模型辅助

```
┌─────────────────────────────────────────────────────────────────────┐
│                   GitHub Copilot 额度保护区                          │
│               (仅 hephaestus 深度编码使用 - 硬编码限制)               │
│                         ↑ 严格限制                                   │
├─────────────────────────────────────────────────────────────────────┤
│              MiniMax-M2.1 (每5小时恢复，额度充足)                    │
│              GLM-4.7 (每5小时恢复，额度充足)                         │
│              （主力开发 · 最大化利用）                               │
├─────────────────────────────────────────────────────────────────────┤
│              Claude Haiku 4.5 (github-copilot 免费充足)              │
│              Kimi 2.5 Free (免费充足)                                │
│              (高频轻量任务分流)                                      │
├─────────────────────────────────────────────────────────────────────┤
│              antigravity-claude-opus-4-5-thinking                    │
│              (最强推理 · 仅 oracle/ultrabrain 关键场景使用)          │
│                         ↑ 极少使用                                   │
├─────────────────────────────────────────────────────────────────────┤
│              antigravity-gemini-3-flash                              │
│              (多模态专用)                                            │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 核心理念

**你的模型资源特点**：
- ✅ **MiniMax-M2.1**：额度每 5 小时恢复，**极其充足**
- ✅ **GLM-4.7**：额度每 5 小时恢复，**极其充足**
- ✅ **Claude Haiku 4.5**：GitHub Copilot 免费订阅，**充足**
- ✅ **Kimi 2.5 Free**：完全免费，**无限使用**
- ⚠️ **antigravity**：付费额度有限，**谨慎使用**
- ⚠️ **GitHub Copilot**：额度有限，**严格保护**

**设计原则**：
| 原则 | 说明 | 实践方式 |
|------|------|----------|
| **额度最大化** | 充足额度的模型优先使用 | MiniMax/GLM 承担 70%+ 任务 |
| **免费辅助** | 免费模型分流高频轻量任务 | Claude Haiku/Kimi 用于搜索、审核 |
| **Copilot 保护** | GitHub Copilot 仅用于 hephaestus | 其他全用替代模型 |
| ** antigravity 最小化** | 付费模型仅用于关键场景 | 仅 oracle/ultrabrain 使用 |

### 1.3 GitHub Copilot 额度保护策略（核心！）

**核心原则**：GitHub Copilot 额度非常有限，必须严格保护。

| 场景 | 使用情况 | 模型选择 |
|------|----------|----------|
| **hephaestus 深度编码** | ✅ **必须使用** | `github-copilot/gpt-5.2-codex`（硬编码限制） |
| 其他所有 agent | ❌ **禁止使用** | 使用替代模型（见下表） |
| 其他所有 category | ❌ **禁止使用** | 使用替代模型（见下表） |

---

## 二、模型资源清单

### 2.1 可用模型总览（你的资源情况）

| 模型 | Provider | 额度情况 | 费用 | 恢复周期 | 特长 | 用途 |
|------|----------|----------|------|----------|------|------|
| **MiniMax-M2.1** | minimax-cn-coding-plan | **极其充足** | 💰 | 每 5 小时恢复 | 通用开发、代码生成 | 主力开发、探索、规划 |
| **GLM-4.7** | zhipuai-coding-plan | **极其充足** | 💰 | 每 5 小时恢复 | 中文理解、文档写作 | 文档、中文、规划辅助 |
| **Claude Haiku 4.5** | github-copilot/claude-haiku-4.5 | **充足（免费订阅）** | ✅ 免费 | 无限 | 快速响应、轻量搜索 | explore、quick、momus |
| **Kimi 2.5 Free** | moonshotai/kimi2.5free | **无限** | ✅ 免费 | 无限 | 中文理解、轻量任务 | momus、中文审核 |
| **antigravity-claude-opus-4-5-thinking** | google/antigravity | 有限 | 💰 | 有限 | 最强推理、复杂架构 | oracle、ultrabrain（极少使用） |
| **antigravity-gemini-3-flash** | google/antigravity | 有限 | 💰 | 有限 | 快速响应、多模态 | 多模态 |
| **GitHub Copilot GPT-5.2** | github-copilot/gpt-5.2-codex | **极其有限** | 💰💰 | 有限 | 深度编码 | **仅 hephaestus** |

### 2.2 模型能力评估

```
推理能力:    antigravity Claude > MiniMax-M2.1 ≈ GLM-4.7 > Claude Haiku > Kimi
代码能力:    antigravity Claude > MiniMax-M2.1 > GLM-4.7 > Claude Haiku
前端能力:    Gemini > antigravity Claude > MiniMax-M2.1 > GLM-4.7
中文能力:    GLM-4.7 > Kimi > MiniMax-M2.1 > antigravity Claude
多模态:      antigravity Gemini Flash > GLM-4.7 > 其他
响应速度:    Claude Haiku > antigravity Gemini Flash > MiniMax-M2.1 > GLM-4.7
额度充裕度:  ✅ MiniMax ≈ ✅ GLM ≈ ✅ Claude Haiku ≈ ✅ Kimi >> antigravity >> Copilot
```

### 2.3 你的模型使用策略

**最大化利用的模型（额度充足）**：

| 模型 | 使用比例 | 任务类型 |
|------|----------|----------|
| **MiniMax-M2.1** | 50% | 主力开发、探索、规划、管理 |
| **GLM-4.7** | 20% | 中文文档、写作、规划辅助 |
| **Claude Haiku** | 15% | 快速搜索、轻量任务 |
| **Kimi** | 5% | 中文审核、轻量任务 |

**谨慎使用的模型（付费有限）**：

| 模型 | 使用比例 | 任务类型 |
|------|----------|----------|
| **antigravity Claude** | 5% | oracle、ultrabrain 关键决策 |
| **antigravity Gemini** | 5% | 多模态任务 |

**严格保护的模型**：

| 模型 | 使用比例 | 任务类型 |
|------|----------|----------|
| **GitHub Copilot** | <1% | 仅 hephaestus 深度编码 |

---

## 三、Agent 分工策略（最大化利用版）

### 3.1 Agent 职责与模型分配

| Agent | 职责 | 分配模型 | 费用 | 分配理由 | GitHub Copilot |
|-------|------|----------|------|----------|----------------|
| **sisyphus** | 主 orchestrator，协调全局 | MiniMax-M2.1 | 💰 | 调用最频繁，额度充足 | ❌ |
| **explore** | 代码库快速搜索 | MiniMax-M2.1 | 💰 | 高频调用，额度充足，能力强 | ❌ |
| **librarian** | 外部文档/GitHub 搜索 | GLM-4.7 | 💰 | 中文文档优势，额度充足 | ❌ |
| **oracle** | 架构咨询、复杂调试 | antigravity-claude-opus-4-5-thinking | 💰 | 关键决策点，需要最强推理 | ❌ 使用 antigravity |
| **hephaestus** | 深度自主编码 | github-copilot/gpt-5.2-codex | 💰💰 | **硬编码限制，必须使用** | ✅ **独享额度** |
| **prometheus** | 任务规划 | MiniMax-M2.1 | 💰 | 规划流程核心，额度充足 | ❌ |
| **metis** | 规划前分析 | GLM-4.7 | 💰 | 与 prometheus 并行，额度充足 | ❌ |
| **momus** | 规划审核 | GLM-4.7 | 💰 | 快速审核，额度充足，中文友好 | ❌ |
| **atlas** | TODO 管理 | MiniMax-M2.1 | 💰 | 项目管理核心，额度充足 | ❌ |
| **multimodal-looker** | 图片/PDF 分析 | antigravity-gemini-3-flash | 💰 | 多模态专长 | ❌ 使用 antigravity |

### 3.2 为什么 explore 用 MiniMax 而不是 Claude Haiku？

**针对你的情况优化**：

| 考量 | explore 用 MiniMax | explore 用 Claude Haiku |
|------|-------------------|------------------------|
| **额度情况** | ✅ 极其充足（每5小时恢复） | ✅ 免费充足 |
| **任务复杂度** | 代码搜索可能涉及复杂逻辑 | 简单搜索任务足够 |
| **响应质量** | MiniMax 代码能力更强 | Haiku 响应更快但能力有限 |
| **额度压力** | 额度充足，不用浪费 | 节省免费额度用于其他场景 |
| **你的最佳选择** | **MiniMax** | 作为备选或轻量任务 |

**结论**：既然 MiniMax 额度每 5 小时就恢复，**不用就浪费**，所以让 MiniMax 承担更多任务，包括 explore。

### 3.3 为什么 momus 用 GLM 而不是 Kimi？

| 考量 | momus 用 GLM | momus 用 Kimi |
|------|--------------|---------------|
| **额度情况** | ✅ 极其充足（每5小时恢复） | ✅ 完全免费 |
| **中文能力** | GLM 中文理解优秀 | Kimi 中文能力也强 |
| **审核质量** | GLM-4.7 能力更强 | Kimi 足够但稍弱 |
| **你的最佳选择** | **GLM** | 作为备选或 Kimi 专长场景 |

**结论**：既然 GLM 额度充足，让 GLM 承担 momus 审核任务，能力更强，质量更高。

### 3.4 GitHub Copilot 保护机制

```
✅ 仅 hephaestus 独享 GitHub Copilot 额度

hephaestus (GPT-5.2-Codex) ──► 深度编码实现
                                      │
                                      │ 严格限制：其他 agent 无法使用
                                      ▼
  ✅ MiniMax-M2.1 (额度充足) → sisyphus/explore/prometheus/atlas
  ✅ GLM-4.7 (额度充足) → librarian/metis/momus/writing
  ✅ Claude Haiku (免费) → quick/轻量任务分流
  ✅ Kimi (免费) → 中文轻量任务
  ✅ antigravity Claude → oracle/ultrabrain (极少)
  ✅ antigravity Gemini → multimodal-looker (极少)
```

### 3.5 并行执行示例（额度最大化版）

```
用户: "ultrawork 完成用户认证功能"

sisyphus (MiniMax) ─────────────────────────────────────────────────►
    │
    ├── explore (MiniMax 充足) ──► 搜索现有代码 ──┐
    │                                            │
    ├── librarian (GLM 充足) ──► 查找 JWT 文档 ──┼─► 并行执行
    │                                            │
    └── oracle (Claude antigravity) ──► 架构建议 ┘
                                              │
                                              ▼
                                    hephaestus (Copilot) ──► 编码实现
                                              │
                                              │ ⚠️ 仅此 agent 使用 Copilot
                                              ▼
                                    其他 agent 全部使用充足额度模型
                                              │
                                              │ ✅ 额度充分利用
                                              ▼
                                    95%+ 任务使用 MiniMax/GLM/免费模型
```

---

## 四、Category 分工策略

### 4.1 Category 职责与模型分配（最大化利用版）

| Category | 复杂度 | 分配模型 | 费用 | 使用场景 | GitHub Copilot |
|----------|--------|----------|------|----------|----------------|
| **quick** | 低 | MiniMax-M2.1 | 💰 | 单文件修改、typo 修复、简单重构 | ❌ |
| **unspecified-low** | 中低 | MiniMax-M2.1 | 💰 | 通用小任务 | ❌ |
| **unspecified-high** | 中高 | MiniMax-M2.1 | 💰 | 通用大任务 | ❌ |
| **ultrabrain** | 极高 | antigravity-claude-opus-4-5-thinking | 💰 | 复杂逻辑、算法设计、系统架构 | ❌ 使用 antigravity |
| **deep** | 高 | MiniMax-M2.1 | 💰 | 深度自主任务 | ❌ |
| **visual-engineering** | 中 | MiniMax-M2.1 | 💰 | 前端/UI/动画、设计相关任务 | ❌ |
| **artistry** | 中高 | GLM-4.7 | 💰 | 创意写作、非常规解决方案 | ❌ |
| **writing** | 中 | GLM-4.7 | 💰 | 文档、README、技术文章 | ❌ |

### 4.2 为什么 quick 也用 MiniMax？

**针对你的情况优化**：

| 考量 | quick 用 MiniMax | quick 用 Claude Haiku |
|------|-----------------|----------------------|
| **额度情况** | ✅ 极其充足，不用浪费 | ✅ 免费充足 |
| **任务复杂度** | 简单修复任务 | 简单修复任务足够 |
| **质量差异** | MiniMax 质量更高 | Haiku 足够但稍弱 |
| **响应速度** | MiniMax 足够快 | Haiku 更快但差异不大 |
| **你的最佳选择** | **MiniMax** | 作为备选 |

**结论**：既然 MiniMax 额度每 5 小时恢复，quick 这种高频任务也用 MiniMax，提升质量。

### 4.3 deep Category → MiniMax-M2.1（额度充足！）

deep 任务使用 MiniMax-M2.1：

| 考量 | deep 用 MiniMax | deep 用 Copilot |
|------|-----------------|-----------------|
| **额度消耗** | 低（每5小时恢复，充足） | 高（极其有限） |
| **运行时间** | 长时间自主运行，稳定 | 可能中途额度耗尽 |
| **中断风险** | 低 | 高 |
| **GitHub Copilot** | 不使用，保护额度 | 禁止使用 |
| **能力差距** | MiniMax 足以胜任 | 过度配置，浪费资源 |
| **额度利用** | ✅ 充分使用，不用浪费 | ❌ 消耗有限额度 |

**结论**：既然 MiniMax 额度充足且每 5 小时恢复，deep 任务用 MiniMax 既能保证质量，又能充分利用额度。

### 4.4 visual-engineering → MiniMax-M2.1（额度充足！）

前端任务也使用 MiniMax-M2.1：

| 考量 | visual 用 MiniMax | visual 用 Gemini |
|------|------------------|------------------|
| **额度情况** | ✅ 极其充足，不用浪费 | ⚠️ antigravity 有限 |
| **前端能力** | MiniMax 前端能力足够 | Gemini 稍强但差异不大 |
| **任务复杂度** | 前端任务不需要最强视觉能力 | 过度配置 |
| **你的最佳选择** | **MiniMax** | 作为备选 |

**结论**：既然 MiniMax 额度充足，visual-engineering 也用 MiniMax，释放 antigravity Gemini 额度给真正的多模态任务。

---

## 五、额度分配预估

### 5.1 按模型分配（额度最大化版）

```
MiniMax-M2.1:       60% (主开发流程 - 额度充足！)
GLM-4.7:            20% (文档/规划辅助 - 额度充足！)
Claude Haiku:       10% (免费分流 - 轻量任务)
Kimi:                5% (免费分流 - 中文轻量任务)
antigravity:         5% (关键决策 - oracle/ultrabrain/多模态)
GitHub Copilot:     <1% (仅 hephaestus - 严格控制)

💰 成本优化: 最大化利用充足额度模型，减少付费 antigravity 使用
```

### 5.2 按场景分配

| 场景 | 触发条件 | 使用模型 | 费用 | GitHub Copilot |
|------|----------|----------|------|----------------|
| 日常开发 | 默认 | MiniMax-M2.1 | 💰 | ❌ |
| 代码搜索 | explore agent | MiniMax-M2.1 | 💰 | ❌ |
| 文档搜索 | librarian agent | GLM-4.7 | 💰 | ❌ |
| 规划分析 | metis/momus agent | GLM-4.7 | 💰 | ❌ |
| 架构咨询 | oracle agent | Claude antigravity | 💰 | ❌ (antigravity) |
| 逻辑难题 | ultrabrain category | Claude antigravity | 💰 | ❌ (antigravity) |
| 前端任务 | visual-engineering | MiniMax-M2.1 | 💰 | ❌ |
| 图片分析 | multimodal-looker | Gemini antigravity | 💰 | ❌ (antigravity) |
| 文档写作 | writing category | GLM-4.7 | 💰 | ❌ |
| 快速修复 | quick category | MiniMax-M2.1 | 💰 | ❌ |
| 深度编码 | hephaestus agent | GPT-5.2-Codex | 💰💰 | ✅ **仅此处使用** |

### 5.3 额度利用优化效果

**优化后额度使用**：

| 模型 | 使用比例 | 额度利用 | 效果 |
|------|----------|----------|------|
| **MiniMax-M2.1** | 60% | ✅ **充分使用** | 额度充足，不浪费 |
| **GLM-4.7** | 20% | ✅ **充分使用** | 额度充足，不浪费 |
| **Claude Haiku** | 10% | ✅ **免费使用** | 完全免费 |
| **Kimi** | 5% | ✅ **免费使用** | 完全免费 |
| **antigravity** | 5% | ⚠️ **谨慎使用** | 仅关键场景 |
| **GitHub Copilot** | <1% | ❌ **严格保护** | 仅 hephaestus |

---

## 六、完整配置示例

### 6.1 最优配置文件（额度最大化版）

以下配置直接复制到 `~/.config/opencode/oh-my-opencode.json` 即可使用：

```json
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json",
  "agents": {
    "sisyphus": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "explore": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "librarian": {
      "model": "zhipuai-coding-plan/glm-4.7"
    },
    "oracle": {
      "model": "google/antigravity-claude-opus-4-5-thinking"
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
      "model": "zhipuai-coding-plan/glm-4.7"
    },
    "atlas": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "multimodal-looker": {
      "model": "google/antigravity-gemini-3-flash"
    }
  },
  "categories": {
    "quick": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "unspecified-low": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "unspecified-high": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "ultrabrain": {
      "model": "google/antigravity-claude-opus-4-5-thinking"
    },
    "deep": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "visual-engineering": {
      "model": "minimax-cn-coding-plan/MiniMax-M2.1"
    },
    "artistry": {
      "model": "zhipuai-coding-plan/glm-4.7"
    },
    "writing": {
      "model": "zhipuai-coding-plan/glm-4.7"
    }
  }
}
```

### 6.2 配置说明

> ⚠️ **前置要求**：
> - 使用 `google/antigravity-*` 格式的模型需要先安装 [`opencode-antigravity-auth`](https://github.com/NoeFabris/opencode-antigravity-auth) 插件

**配置特点（针对你的情况优化）**：

| 配置项 | 模型 | 特点 |
|--------|------|------|
| sisyphus | MiniMax-M2.1 | ✅ 额度充足，主力 orchestrator |
| explore | MiniMax-M2.1 | ✅ 额度充足，能力强，代码搜索质量高 |
| librarian | GLM-4.7 | ✅ 额度充足，中文文档优势 |
| oracle | Claude antigravity | 💰 关键决策，谨慎使用 |
| hephaestus | GPT-5.2-Codex | 💰💰 强制使用，深度编码 |
| prometheus | MiniMax-M2.1 | ✅ 额度充足，规划核心 |
| metis | GLM-4.7 | ✅ 额度充足，与 prometheus 并行 |
| momus | GLM-4.7 | ✅ 额度充足，审核质量高 |
| atlas | MiniMax-M2.1 | ✅ 额度充足，项目管理 |
| multimodal-looker | Gemini antigravity | 💰 多模态专长 |
| quick | MiniMax-M2.1 | ✅ 额度充足，快速修复质量高 |
| unspecified-low | MiniMax-M2.1 | ✅ 额度充足，通用小任务 |
| unspecified-high | MiniMax-M2.1 | ✅ 额度充足，通用大任务 |
| ultrabrain | Claude antigravity | 💰 复杂逻辑，谨慎使用 |
| deep | MiniMax-M2.1 | ✅ 额度充足，深度任务 |
| visual-engineering | MiniMax-M2.1 | ✅ 额度充足，前端任务 |
| artistry | GLM-4.7 | ✅ 额度充足，创意任务 |
| writing | GLM-4.7 | ✅ 额度充足，文档写作 |

---

## 七、GitHub Copilot 额度保护策略

### 7.1 为什么严格限制 GitHub Copilot？

| 问题 | 影响 |
|------|------|
| 额度极其有限 | 频繁调用会快速耗尽额度 |
| 成本高昂 | 每次调用都有显著费用 |
| 难以监控 | 容易在不知不觉中消耗殆尽 |
| 影响 hephaestus | 深度编码任务可能因额度不足而中断 |

### 7.2 如何确保 Copilot 额度仅用于 hephaestus？

1. **配置层面**：
   - 配置文件中的 agent 和 category **严禁使用** `github-copilot/*` 模型（除 hephaestus 外）
   - 仅 `hephaestus` 保留 `github-copilot/gpt-5.2-codex`

2. **代码层面**：
   - hephaestus 的 Copilot 使用是**硬编码**，无法通过配置修改
   - 其他 agent 没有硬编码 Copilot 调用

3. **充足模型分流**：
   - 95%+ 任务使用 MiniMax/GLM（额度充足）
   - 减少对 Copilot 的依赖

---

## 八、调优建议

### 8.1 如果 MiniMax 额度紧张（极端情况）

将部分任务切换到免费模型：

```json
"explore": {
  "model": "github-copilot/claude-haiku-4.5"
},
"quick": {
  "model": "github-copilot/claude-haiku-4.5"
},
"momus": {
  "model": "moonshotai/kimi2.5free"
}
```

### 8.2 如果需要更强的 oracle 能力

确保 oracle 使用 antigravity Claude（已配置）：

```json
"oracle": {
  "model": "google/antigravity-claude-opus-4-5-thinking"
}
```

### 8.3 如果需要更强的 ultrabrain 能力

确保 ultrabrain 使用 antigravity Claude（已配置）：

```json
"ultrabrain": {
  "model": "google/antigravity-claude-opus-4-5-thinking"
}
```

### 8.4 如果 antigravity 额度紧张

将 antigravity 任务切换到 MiniMax/GLM：

```json
"oracle": {
  "model": "minimax-cn-coding-plan/MiniMax-M2.1"
},
"ultrabrain": {
  "model": "minimax-cn-coding-plan/MiniMax-M2.1"
},
"multimodal-looker": {
  "model": "zhipuai-coding-plan/glm-4.7"
}
```

> ⚠️ 注意：此配置会降低推理能力，仅在 antigravity 额度紧急时使用

---

## 九、最佳实践

### 9.1 日常使用（额度充分利用版）

1. **简单任务**: 直接执行，sisyphus 使用 MiniMax（额度充足）
2. **需要搜索**: explore (MiniMax) + librarian (GLM) 并行（额度充足）
3. **复杂架构**: 手动调用 oracle，使用 Claude（antigravity，谨慎使用）
4. **前端任务**: 使用 `delegate_task(category="visual-engineering")` → MiniMax
5. **文档任务**: 使用 `delegate_task(category="writing")` → GLM
6. **快速修复**: 使用 `delegate_task(category="quick")` → MiniMax（额度充足）
7. **规划审核**: 自动由 momus 使用 GLM（额度充足）
8. **深度编码**: 自动由 hephaestus 使用 GitHub Copilot（仅此处使用）

### 9.2 ultrawork 模式（额度保护版）

当输入 `ultrawork` 或 `ulw` 时：
- sisyphus 自动协调多个 agent
- explore (MiniMax) 和 librarian (GLM) 并行搜索（额度充足）
- 复杂问题自动调用 oracle (Claude antigravity)
- 编码任务分配给 hephaestus (Copilot，仅此使用)
- **额度保护**：所有其他 agent 使用 MiniMax/GLM（额度充足）
- **额度充分利用**：95%+ 任务使用充足额度模型

### 9.3 额度监控

定期检查额度消耗：

| 模型 | 费用 | 恢复周期 | 监控方式 |
|------|------|----------|----------|
| **MiniMax-M2.1** | 💰 | 每 5 小时恢复 | MiniMax 控制台（额度充足，关注恢复周期） |
| **GLM-4.7** | 💰 | 每 5 小时恢复 | 智谱 AI 控制台（额度充足，关注恢复周期） |
| **antigravity** | 💰 | 有限 | Google Cloud 控制台（谨慎使用） |
| **GitHub Copilot** | 💰💰 | 有限 | GitHub Copilot 控制台（重点关注 hephaestus） |
| **Claude Haiku** | ✅ 免费 | 无限 | 无需监控 |
| **Kimi** | ✅ 免费 | 无限 | 无需监控 |

### 9.4 额度利用最大化技巧

1. **优先使用充足额度模型**：
   - MiniMax/GLM 承担 80%+ 任务
   - 充分利用每 5 小时恢复的额度

2. **免费模型辅助分流**：
   - Claude Haiku 用于轻量任务
   - Kimi 用于中文轻量任务

3. **antigravity 谨慎使用**：
   - 仅 oracle/ultrabrain 关键场景使用
   - 减少 antigravity 消耗

4. **Copilot 严格保护**：
   - 仅 hephaestus 使用
   - 其他场景绝不调用

---

## 十、常见问题 FAQ

### Q1: MiniMax 和 GLM 额度每 5 小时恢复，用不完怎么办？

**答**: 这正是本配置的核心思路！
- **让 MiniMax/GLM 承担更多任务**（从 60% 提升到 80%+）
- explore、quick、visual-engineering 等都使用 MiniMax
- librarian、momus、artistry、writing 等都使用 GLM
- **用不完就浪费了**，所以要最大化利用

### Q2: 为什么 visual-engineering 也用 MiniMax 而不是 Gemini？

**答**: 针对你的情况优化：
- MiniMax 前端能力足够应对大多数任务
- antigravity Gemini 额度有限，留给真正的多模态任务
- 既然 MiniMax 额度充足，不用就浪费

### Q3: antigravity 额度这么少，会不会不够用？

**答**: 不会。antigravity 仅用于 oracle 和 ultrabrain 场景：
- oracle 调用频率很低（仅复杂架构决策时）
- ultrabrain 调用频率很低（仅复杂逻辑时）
- 5% 的使用比例完全足够

### Q4: 如果我想用更强的模型怎么办？

**答**: 可以临时切换：

```json
"oracle": {
  "model": "google/antigravity-claude-opus-4-5-thinking"  // 已配置最强
},
"ultrabrain": {
  "model": "google/antigravity-claude-opus-4-5-thinking"  // 已配置最强
}
```

### Q5: 如何验证配置是否生效？

**答**: 运行以下命令检查：

```bash
# 检查 agent 配置
oh-my-opencode config get agents

# 检查 category 配置
oh-my-opencode config get categories

# 测试 explore agent（应该使用 MiniMax）
oh-my-opencode "搜索代码中的 auth 函数"

# 测试 quick category（应该使用 MiniMax）
delegate_task(category="quick", prompt="修复这个拼写错误")

# 测试 momus agent（应该使用 GLM）
momus "审核这个开发计划"
```

---

## 十一、总结

本配置策略的核心是**额度充足模型最大化利用 + GitHub Copilot 严格保护**：

### 额度利用优化成果

| 指标 | 优化前 | 优化后 | 改善 |
|------|--------|--------|------|
| MiniMax/GLM 使用 | 60% | **80%+** | ✅ 充分使用，不浪费 |
| antigravity 使用 | 20% | **5%** | ⚠️ 谨慎使用，节省成本 |
| 免费模型使用 | 10% | **15%** | ✅ 辅助分流 |
| GitHub Copilot 使用 | 10% | **<1%** | ❌ 严格保护 |

### 核心原则

1. **MiniMax/GLM 作为"主力军"**，承担 80%+ 任务，充分利用每 5 小时恢复的额度
2. **免费模型（Claude Haiku/Kimi）作为"辅助队"**，分流轻量任务
3. **antigravity 作为"精锐部队"**，仅用于 oracle/ultrabrain 关键决策
4. **GitHub Copilot 作为"战略储备"**，仅用于 hephaestus 深度编码

### 模型使用优先级（你的情况）

```
✅ 额度充足（优先大量使用）：
   MiniMax-M2.1 → 80%+ 任务（explore/quick/visual/deep/unspecified）
   GLM-4.7 → 20% 任务（librarian/metis/momus/artistry/writing）

✅ 免费（辅助分流）：
   Claude Haiku → 轻量任务备选
   Kimi → 中文轻量任务备选

💰 付费有限（谨慎使用）：
   antigravity Claude → oracle/ultrabrain（极少）
   antigravity Gemini → multimodal-looker（极少）

💰💰 严格保护（仅必要时）：
   GitHub Copilot → 仅 hephaestus（<1%）
```

**最终效果**：
- ✅ **额度充分利用**：MiniMax/GLM 每 5 小时恢复的额度全部用上
- ✅ **成本最优**：antigravity 仅用于关键场景，减少付费消耗
- ✅ **能力保障**：关键决策使用最强模型（antigravity Claude）
- ✅ **Copilot 保护**：额度仅用于真正需要的场景（hephaestus）

这样配置既能让你的充足额度模型发挥最大价值，又能保护有限的付费额度，实现成本与能力的最佳平衡。

---

*文档由 Sisyphus 生成，根据用户模型资源情况定制优化。*
*最后更新: 2026-02-03 - 优化额度充足模型最大化利用策略*
