---
name: douyin-content-parser
description: 抖音内容解析技能，结合douyin-downloader和ffmpeg进行视频下载、音频提取和内容分析。
---

# 抖音内容解析器

## 功能特性

- 自动解析抖音链接或modal_id
- 获取视频元数据（标题、作者、描述等）
- 下载视频并提取音频（需要有效API访问）
- 生成视频内容摘要
- 处理API限制情况下的降级方案

## 使用方式

### 示例命令

```
总结这个抖音视频：https://v.douyin.com/qchH_0YurEA/
```

```
分析视频内容 7580266475575905536
```

```
提取抖音视频的文字内容：https://www.douyin.com/video/7580266475575905536
```

## 触发方式

当用户请求：
- "总结抖音视频"
- "分析视频内容" 
- "提取抖音视频内容"
- "解析抖音链接"
- 提供抖音链接并要求内容分析

## 依赖要求

### 系统依赖
- ffmpeg (用于音频/视频处理)
- python3 (用于脚本执行)
- requests (Python库)

### 配置要求
需要在 `~/.openclaw/config.json` 中配置 TikHub API Token：

```json
{
    "tikhub_api_token": "您的Token"
}
```

### 脚本位置
- 主解析脚本: `scripts/douyin_content_parser.py`
- 简化解析脚本: `scripts/simple_douyin_parser.py`
- 下载脚本: `scripts/douyin_download.py` (复用现有douyin-downloader)

## 工作流程

1. 接收用户提供的抖音链接或modal_id
2. 尝试使用TikHub API获取完整视频信息
3. 如果API访问失败，使用简化模式提取基本信息
4. 生成结构化的JSON输出包含所有可用信息
5. 在API不可用时提供降级的摘要信息

## 降级策略

当API不可用或返回错误时：
- 从URL中提取视频ID
- 生成基本的元数据结构
- 提供用户友好的错误提示
- 建议手动查看或提供更多信息

## 输出格式

成功时返回JSON格式的视频信息：
```json
{
  "title": "视频标题",
  "author": "作者昵称", 
  "description": "视频描述",
  "video_id": "视频ID",
  "duration": 时长(秒),
  "create_time": "创建时间",
  "summary_text": "格式化的摘要文本"
}
```