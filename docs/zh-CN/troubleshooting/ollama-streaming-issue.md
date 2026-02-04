---
summary: Ollama 流式传输问题的解决方案，详解 JSON 解析错误的原因和修复方法
read_when:
  - 使用 Ollama 提供商遇到 JSON 解析错误时
  - 需要配置 stream: false 选项时
  - 排查 NDJSON 格式问题时
  - 了解 SDK 兼容性问题时
title: Ollama 流式传输问题
---

# Ollama 流式传输问题 - JSON 解析错误

## 问题

当使用 Ollama 作为提供商时，你可能会遇到以下错误：

```
JSON Parse error: Unexpected EOF
```

---

## 根本原因

Ollama 返回 **NDJSON**（换行分隔的 JSON）格式的响应，而 Claude Code SDK 期望单个 JSON 对象。

### NDJSON 示例（错误格式）

```json
{"message":{"tool_calls":[...]}, "done":false}
{"message":{"content":""}, "done":true}
```

### Claude Code SDK 期望（正确格式）

```json
{"message":{"tool_calls":[...], "content":""}, "done":true}
```

---

## 解决方案

### 方案 1：禁用流式传输（推荐）

在 `oh-my-opencode.json` 配置中为 Ollama 模型设置 `stream: false`：

```jsonc
{
  "agents": {
    "explore": {
      "model": "ollama/qwen3-coder",
      "stream": false  // ← 必须设置为 false
    }
  }
}
```

#### 为什么需要 `stream: false`？

Ollama 启用流式传输（默认）：
- 返回多行 NDJSON
- Claude Code SDK 无法正确解析多行 NDJSON
- 导致工具调用时出现 `JSON Parse error: Unexpected EOF`

Ollama 禁用流式传输（`stream: false`）：
- 返回单个 JSON 对象
- Claude Code SDK 可以正确解析
- 问题解决

---

### 方案 2：验证配置

检查你的当前配置：

```bash
# 查看配置文件
cat ~/.config/opencode/oh-my-opencode.json | grep -A 3 ollama

# 应该看到：
"stream": false
```

如果没有看到 `"stream": false`，需要手动添加到配置中。

---

### 方案 3：测试 Ollama 连接

验证 Ollama 是否正常工作：

```bash
# 测试 Ollama 是否在运行
curl http://localhost:11434/api/tags

# 测试 API 调用
curl -s http://localhost:11434/api/chat \
  -d '{
      "model": "qwen3-coder",
      "messages": [{"role": "user", "content": "Hello"}],
      "stream": false
    }'
```

如果测试成功返回单个 JSON 对象，说明修复有效。

---

## 支持的 Ollama 模型

以下是与 oh-my-opencode 配合良好的常见 Ollama 模型：

| 模型 | 最适合用途 | 推荐配置 |
|--------|----------|----------|
| `ollama/qwen3-coder` | 代码生成、构建修复 | `{"model": "ollama/qwen3-coder", "stream": false}` |
| `ollama/ministral-3:14b` | 探索、代码库搜索 | `{"model": "ollama/ministral-3:14b", "stream": false}` |
| `ollama/lfm2.5-thinking` | 文档、写作 | `{"model": "ollama/lfm2.5-thinking", "stream": false}` |

---

## 常见错误信息

| 错误信息 | 可能原因 | 解决方案 |
|----------|----------|----------|
| `JSON Parse error: Unexpected EOF` | Ollama 流式传输未禁用 | 在配置中添加 `"stream": false` |
| `Connection refused` | Ollama 未运行 | 启动 Ollama 服务：`ollama serve` |
| `Model not found` | 模型名称错误 | 检查模型名称是否正确 |
| `Timeout` | 响应超时 | 增加 API 调用的超时时间 |

---

## 相关文档

- [配置指南](../configurations.md) - 完整的 Ollama 配置说明
- [常见问题解答](../faq.md) - 其他常见问题的解决方案
- [故障排查](../troubleshooting/ollama-streaming-issue.md) - 报告此问题的链接

---

## 长期解决方案

这是一个已知问题，由 Claude Code SDK 的限制引起。正确的修复需要：

1. **Claude Code SDK 更新**：支持解析 NDJSON 响应
2. **Oh My OpenCode 更新**：自动检测并合并 NDJSON 响应

跟踪此问题的 GitHub Issue：
- https://github.com/code-yeongyu/oh-my-opencode/issues/1124

---

## 快速修复总结

```bash
# 1. 编辑配置文件
vim ~/.config/opencode/oh-my-opencode.json

# 2. 添加 stream: false
# 在使用 Ollama 的代理配置中添加：
"stream": false

# 3. 验证修复
curl -s http://localhost:11434/api/chat \
  -d '{"model":"qwen3-coder","messages":[{"role":"user","content":"Hello"}],"stream":false}'
```
