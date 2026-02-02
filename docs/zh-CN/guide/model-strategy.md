# Oh My OpenCode 模型配置策略指南

> 最后更新: 2026-02-02
> 配置文件: `~/.config/opencode/oh-my-opencode.json`

---

## 一、设计原则

### 1.1 核心理念：分层调度

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Opus 4.5 Thinking                  │
│                    (最强推理 · 稀缺资源)                      │
│                         ↑ 仅在必要时                          │
├─────────────────────────────────────────────────────────────┤
│     MiniMax-M2.1          ←→          GLM-4.7               │
│     (主力开发)                        (并行辅助)             │
│                      并行分工                                │
├─────────────────────────────────────────────────────────────┤
│              Gemini 3 Pro / Flash                           │
│              (前端专用 · 多模态专用)                         │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 四大设计原则

| 原则 | 说明 |
|------|------|
| **能力匹配** | 任务复杂度与模型能力对应，杀鸡不用牛刀 |
| **额度保护** | 稀缺资源（Claude Opus）只用于关键决策点 |
| **并行分流** | MiniMax 和 GLM 分担不同类型任务，避免单点过载 |
| **专长发挥** | 利用各模型特长：Gemini 做前端，GLM 做中文 |

---

## 二、模型资源清单

### 2.1 可用模型

| 模型 | Provider | 额度情况 | 特长 |
|------|----------|----------|------|
| Claude Opus 4.5 Thinking | google/antigravity | 有限（多账户轮换） | 最强推理、复杂架构 |
| MiniMax-M2.1 | minimax-cn-coding-plan | 充足（会员） | 通用开发、代码生成 |
| GLM-4.7 | zhipuai-coding-plan | 充足（会员） | 中文理解、文档写作 |
| Gemini 3 Pro | google | 充足 | 前端/UI、创意设计 |
| Gemini 3 Flash | google | 充足 | 图片分析、快速响应 |

### 2.2 模型能力评估

```
推理能力:  Claude Opus > MiniMax-M2.1 ≈ GLM-4.7 > Gemini Pro > Gemini Flash
代码能力:  Claude Opus > MiniMax-M2.1 > GLM-4.7 > Gemini Pro
前端能力:  Gemini Pro > Claude Opus > MiniMax-M2.1 > GLM-4.7
中文能力:  GLM-4.7 > MiniMax-M2.1 > Claude Opus > Gemini
多模态:    Gemini Flash > Gemini Pro > GLM-4.7 > 其他
```

---

## 三、Agent 分工策略

### 3.1 Agent 职责与模型分配

| Agent | 职责 | 分配模型 | 分配理由 |
|-------|------|----------|----------|
| **sisyphus** | 主 orchestrator，协调全局 | MiniMax-M2.1 | 调用最频繁，需要充足额度 |
| **explore** | 代码库快速搜索 | MiniMax-M2.1 | 高频调用，与主模型一致减少切换 |
| **librarian** | 外部文档/GitHub 搜索 | GLM-4.7 | 分流到 GLM，中文文档优势 |
| **oracle** | 架构咨询、复杂调试 | Claude Opus Thinking | 关键决策点，需要最强推理 |
| **hephaestus** | 深度自主编码 | MiniMax-M2.1 | 长时间运行，需要充足额度 |
| **prometheus** | 任务规划 | MiniMax-M2.1 | 规划流程核心 |
| **metis** | 规划前分析 | GLM-4.7 | 与 prometheus 并行，分流到 GLM |
| **momus** | 规划审核 | GLM-4.7 | 与 prometheus 并行，分流到 GLM |
| **atlas** | TODO 管理 | MiniMax-M2.1 | 项目管理核心 |
| **multimodal-looker** | 图片/PDF 分析 | Gemini 3 Flash | 多模态专长 |

### 3.2 并行执行示例

```
用户: "ultrawork 完成用户认证功能"

sisyphus (MiniMax) ─────────────────────────────────────────────────►
    │
    ├── explore (MiniMax) ──► 搜索现有代码 ──┐
    │                                        │
    ├── librarian (GLM) ────► 查找 JWT 文档 ─┼─► 并行执行
    │                                        │
    └── oracle (Claude) ────► 架构建议 ─────┘
                                    │
                                    ▼
                          hephaestus (MiniMax) ──► 编码实现
```

---

## 四、Category 分工策略

### 4.1 Category 职责与模型分配

| Category | 复杂度 | 分配模型 | 使用场景 |
|----------|--------|----------|----------|
| **quick** | 低 | MiniMax-M2.1 | 单文件修改、typo 修复 |
| **unspecified-low** | 中低 | MiniMax-M2.1 | 通用小任务 |
| **unspecified-high** | 中高 | MiniMax-M2.1 | 通用大任务 |
| **ultrabrain** | 极高 | Claude Opus Thinking | 复杂逻辑、算法设计 |
| **deep** | 高 | MiniMax-M2.1 | 深度自主任务 |
| **visual-engineering** | 中 | Gemini 3 Pro | 前端/UI/动画 |
| **artistry** | 中高 | GLM-4.7 | 创意写作、非常规方案 |
| **writing** | 中 | GLM-4.7 | 文档、README |

### 4.2 为什么 deep 用 MiniMax 而不是 Claude？

| 考量 | deep 用 MiniMax | deep 用 Claude |
|------|-----------------|----------------|
| 额度消耗 | 低（会员充足） | 高（有限额度） |
| 运行时间 | 长时间自主运行 | 可能中途额度耗尽 |
| 中断风险 | 低 | 高 |
| 能力差距 | MiniMax 足以胜任 | 过度配置 |

**结论**: deep 任务需要长时间自主运行，优先保证稳定性和额度充足。

---

## 五、额度分配预估

### 5.1 按模型分配

```
MiniMax-M2.1:     55% (主开发流程)
GLM-4.7:          25% (文档/规划辅助)
Gemini:           15% (前端/多模态)
Claude Opus:       5% (关键决策点)
```

### 5.2 按场景分配

| 场景 | 触发条件 | 使用模型 |
|------|----------|----------|
| 日常开发 | 默认 | MiniMax-M2.1 |
| 代码搜索 | explore agent | MiniMax-M2.1 |
| 文档搜索 | librarian agent | GLM-4.7 |
| 规划分析 | metis/momus agent | GLM-4.7 |
| 架构咨询 | oracle agent | Claude Opus |
| 逻辑难题 | ultrabrain category | Claude Opus |
| 前端任务 | visual-engineering | Gemini 3 Pro |
| 图片分析 | multimodal-looker | Gemini 3 Flash |
| 文档写作 | writing category | GLM-4.7 |

---

## 六、配置文件详解

### 6.1 完整配置

```json
{
  "agents": {
    "sisyphus":         { "model": "minimax-cn-coding-plan/MiniMax-M2.1" },
    "explore":          { "model": "minimax-cn-coding-plan/MiniMax-M2.1" },
    "librarian":        { "model": "zhipuai-coding-plan/glm-4.7" },
    "oracle":           { "model": "google/antigravity-claude-opus-4-5-thinking" },
    "hephaestus":       { "model": "minimax-cn-coding-plan/MiniMax-M2.1" },
    "prometheus":       { "model": "minimax-cn-coding-plan/MiniMax-M2.1" },
    "metis":            { "model": "zhipuai-coding-plan/glm-4.7" },
    "momus":            { "model": "zhipuai-coding-plan/glm-4.7" },
    "atlas":            { "model": "minimax-cn-coding-plan/MiniMax-M2.1" },
    "multimodal-looker": { "model": "google/gemini-3-flash" }
  },
  "categories": {
    "quick":              { "model": "minimax-cn-coding-plan/MiniMax-M2.1" },
    "unspecified-low":    { "model": "minimax-cn-coding-plan/MiniMax-M2.1" },
    "unspecified-high":   { "model": "minimax-cn-coding-plan/MiniMax-M2.1" },
    "ultrabrain":         { "model": "google/antigravity-claude-opus-4-5-thinking" },
    "deep":               { "model": "minimax-cn-coding-plan/MiniMax-M2.1" },
    "visual-engineering": { "model": "google/gemini-3-pro" },
    "artistry":           { "model": "zhipuai-coding-plan/glm-4.7" },
    "writing":            { "model": "zhipuai-coding-plan/glm-4.7" }
  }
}
```

### 6.2 配置说明

- **agents**: 控制内置 agent 使用的模型
- **categories**: 控制 `delegate_task(category="xxx")` 使用的模型
- 配置会覆盖内置回退链，直接使用指定模型

---

## 七、调优建议

### 7.1 如果 MiniMax 额度紧张

将部分任务分流到 GLM：

```json
"explore": { "model": "zhipuai-coding-plan/glm-4.7" },
"quick": { "model": "zhipuai-coding-plan/glm-4.7" }
```

### 7.2 如果需要更强的 deep 能力

将 deep 切换到 Claude（但注意额度消耗）：

```json
"deep": { "model": "google/antigravity-claude-opus-4-5-thinking" }
```

### 7.3 如果 Claude 额度充裕

可以将更多关键 agent 切换到 Claude：

```json
"hephaestus": { "model": "google/antigravity-claude-opus-4-5-thinking" },
"prometheus": { "model": "google/antigravity-claude-opus-4-5-thinking" }
```

---

## 八、最佳实践

### 8.1 日常使用

1. **简单任务**: 直接执行，sisyphus 使用 MiniMax
2. **需要搜索**: explore + librarian 并行，分流到 MiniMax + GLM
3. **复杂架构**: 手动调用 oracle，使用 Claude
4. **前端任务**: 使用 `delegate_task(category="visual-engineering")`
5. **文档任务**: 使用 `delegate_task(category="writing")`

### 8.2 ultrawork 模式

当输入 `ultrawork` 或 `ulw` 时：
- sisyphus 自动协调多个 agent
- explore (MiniMax) 和 librarian (GLM) 并行搜索
- 复杂问题自动调用 oracle (Claude)
- 编码任务分配给 hephaestus (MiniMax)

### 8.3 监控额度

定期检查各模型额度消耗：
- MiniMax 控制台
- 智谱 AI 控制台
- Google Cloud 控制台

---

## 九、总结

本配置策略的核心是**分层调度 + 并行分流**：

1. **Claude Opus** 作为"战略储备"，只在关键决策点使用
2. **MiniMax** 作为"主力军"，承担日常开发任务
3. **GLM** 作为"辅助队"，与 MiniMax 并行分担任务
4. **Gemini** 作为"专业队"，专注前端和多模态任务

这样既能在需要时使用最强模型，又能保证额度可持续使用。

---

*文档由 Sisyphus 生成，根据用户模型资源情况定制优化。*
