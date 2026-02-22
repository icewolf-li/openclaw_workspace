# 抖音内容解析器

这是一个结合douyin-downloader和ffmpeg的技能，用于解析抖音视频内容。

## 功能

- 解析抖音链接获取视频信息
- 下载视频文件（如果API可用）
- 提取音频（使用ffmpeg）
- 生成内容摘要

## 使用方法

1. 确保已配置TikHub API Token在 `~/.openclaw/config.json`
2. 调用脚本: `python3 scripts/douyin_content_parser.py <抖音链接或ID> <API_Token>`

## 注意事项

- 如果TikHub API不可用，技能将尝试从页面标题和描述中提取基本信息
- 视频下载功能依赖于API的可用性
- 音频提取需要ffmpeg已安装