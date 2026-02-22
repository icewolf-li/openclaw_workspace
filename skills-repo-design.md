# 跨平台 Skills 仓库系统设计方案

## 目标
创建一个统一的 GitHub 仓库，能够同时支持 OpenClaw、iFlow、OpenCode、ClaudeCode 等多个 AI Agent 平台的技能分发。

## 仓库结构

```
ai-agent-skills/
├── README.md                 # 项目总览和使用指南
├── LICENSE                   # 开源许可证
├── universal/               # 通用技能定义
│   ├── template/            # 通用技能模板
│   │   └── SKILL.md
│   ├── weather/             # 示例技能：天气查询
│   │   └── SKILL.md
│   └── github-kb/           # 示例技能：GitHub 知识库
│       └── SKILL.md
├── adapters/                # 平台适配器
│   ├── openclaw/            # OpenClaw 适配器
│   │   ├── convert.js
│   │   └── validate.js
│   ├── iflow/               # iFlow 适配器
│   │   ├── convert.py
│   │   └── validate.py
│   └── common/              # 通用转换工具
│       └── base-converter.js
├── platforms/               # 平台特定输出
│   ├── openclaw/            # OpenClaw 格式技能
│   ├── iflow/               # iFlow 格式技能
│   └── ...
├── tools/                   # 开发工具
│   ├── publish.sh           # 发布脚本
│   ├── sync.sh              # 同步脚本
│   └── test/                # 测试工具
└── docs/                    # 文档
    ├── CONTRIBUTING.md      # 贡献指南
    └── PLATFORMS.md         # 各平台兼容性说明
```

## 通用技能格式规范

### SKILL.md 通用结构

```markdown
---
name: skill-name
description: Brief description of the skill
version: 1.0.0
universal: true
platforms:
  - openclaw
  - iflow
  - opencode
  - claudecode
requires:
  bins: []
  env: []
  config: []
---

# Skill Name

## Description
Detailed description of what this skill does.

## Universal Tool Definition
```json
{
  "tools": [
    {
      "name": "tool_name",
      "description": "Tool description",
      "parameters": {
        "type": "object",
        "properties": {
          "param1": {
            "type": "string",
            "description": "Parameter description"
          }
        },
        "required": ["param1"]
      }
    }
  ]
}
```

## Platform-Specific Notes
### OpenClaw
- Uses standard OpenClaw tool calling
- Supports {baseDir} variable

### iFlow
- Requires function-style tool definition
- Parameter mapping: param1 -> argument1

### Other Platforms
- Add platform-specific notes here
```

## 转换流程

1. **开发通用技能**：在 `universal/` 目录下创建技能
2. **运行转换器**：执行适配器脚本生成各平台版本
3. **验证输出**：确保各平台版本符合规范
4. **发布分发**：推送到各平台的技能仓库或注册表

## OpenClaw 集成

对于 OpenClaw，可以直接使用 ClawHub 进行分发：

```bash
# 安装 ClawHub CLI
npm install -g clawhub

# 发布技能到 ClawHub
clawhub publish platforms/openclaw/weather --slug weather-skill --name "Weather Skill"
```

## 贡献流程

1. Fork 仓库
2. 在 `universal/` 目录下创建新技能
3. 运行转换脚本生成各平台版本
4. 提交 Pull Request
5. 维护者审核并合并

## 未来扩展

- 添加更多平台适配器
- 实现自动化 CI/CD 流程
- 创建 Web 界面用于技能管理
- 集成技能测试框架