# 跨平台 AI 技能仓库

这是一个通用的 AI 技能仓库，支持多个平台：
- ✅ OpenClaw
- 🔄 iFlow  
- 🔄 OpenCode
- 🔄 ClaudeCode

## 仓库结构

```
skills-repo/
├── cross-platform/          # 通用技能（主开发目录）
├── platform-specific/       # 各平台特定版本
├── shared-resources/        # 共享资源和工具
└── tools/                   # 转换和验证工具
```

## 使用方法

### 1. 开发新技能
在 `cross-platform/` 目录下创建新的技能文件夹，使用通用 SKILL.md 模板。

### 2. 转换为特定平台
```bash
# 转换为 OpenClaw 格式
python tools/converter/convert.py --input cross-platform/weather --output platform-specific/openclaw/weather --platform openclaw

# 转换为 iFlow 格式  
python tools/converter/convert.py --input cross-platform/weather --output platform-specific/iflow/weather --platform iflow
```

### 3. 发布到各平台
- **OpenClaw**: 使用 ClawHub 发布 `platform-specific/openclaw/` 目录
- **其他平台**: 按照各自平台的发布流程操作

## 贡献指南

1. 所有新技能必须首先在 `cross-platform/` 目录中开发
2. 确保 SKILL.md 包含所有必要字段
3. 测试通用功能后再进行平台转换
4. 提交 PR 时包含所有平台的转换结果

## 支持的平台特性

| 平台 | 工具调用 | 文件系统 | 网络访问 | 安全模型 |
|------|----------|----------|----------|----------|
| OpenClaw | ✅ 完整支持 | ✅ 读写 | ✅ HTTP/Web | ✅ 沙箱可选 |
| iFlow | 🔄 待确认 | 🔄 待确认 | 🔄 待确认 | 🔄 待确认 |
| OpenCode | 🔄 待确认 | 🔄 待确认 | 🔄 待确认 | 🔄 待确认 |
| ClaudeCode | 🔄 待确认 | 🔄 待确认 | 🔄 待确认 | 🔄 待确认 |

> 注意：其他平台的具体支持情况需要进一步调研和测试。

## 许可证

MIT License - 自由使用、修改和分发。