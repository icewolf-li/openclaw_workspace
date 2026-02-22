---
name: universal-weather
description: 获取全球任何地点的天气信息，支持多平台通用接口
platforms:
  - openclaw
  - iflow
  - opencode
  - claudecode
universal_version: 1.0.0
---

# 通用天气技能

## 功能描述
提供统一的天气查询接口，支持：
- 当前天气状况
- 温度、湿度、风速等详细信息  
- 多地点支持（城市名、坐标）
- 自动处理不同平台的 API 调用差异

## 通用工具定义
```json
{
  "tools": [
    {
      "name": "get_weather",
      "description": "获取指定地点的当前天气信息",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string", 
            "description": "地点名称或坐标 (例如: '北京' 或 '39.9042,116.4074')"
          },
          "units": {
            "type": "string",
            "enum": ["metric", "imperial"],
            "description": "温度单位 (metric=Celsius, imperial=Fahrenheit)"
          }
        },
        "required": ["location"]
      }
    }
  ]
}
```

## 平台适配说明

### OpenClaw 实现
- 使用内置的 weather 技能或 web_fetch 工具
- 支持 wttr.in 和 Open-Meteo API
- 自动处理 JSON 响应解析

### iFlow 实现要求  
- 需要实现 get_weather 函数
- 返回标准化的天气对象格式
- 处理 API 密钥配置

### OpenCode/ClaudeCode 实现
- 注册相应的工具函数
- 确保返回格式与通用定义一致
- 处理平台特定的网络请求限制