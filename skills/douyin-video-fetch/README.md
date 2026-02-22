# Douyin Video Fetch 集成指南

## 技能概述
douyin-video-fetch 是一个强大的抖音视频下载工具，使用Playwright浏览器自动化技术来绕过反爬虫机制，下载无水印的抖音视频。

## 与其他技能的关系

### 1. douyin-downloader (API方式)
- **优点**: 快速、简单
- **缺点**: 依赖第三方API，可能受限于速率限制或Token有效性
- **适用场景**: 快速获取视频元数据

### 2. douyin-video-fetch (浏览器自动化)
- **优点**: 不依赖第三方API，直接从抖音网站提取
- **缺点**: 较慢，需要更多系统资源
- **适用场景**: API不可用时的备用方案，需要下载完整视频文件

### 3. douyin-content-parser (内容分析)
- **优点**: 生成结构化的内容摘要
- **缺点**: 依赖前两个技能提供数据
- **适用场景**: 最终的内容分析和报告生成

## 推荐工作流程

```
用户输入抖音链接
        ↓
尝试 douyin-downloader (快速获取元数据)
        ↓
如果失败 → 尝试 douyin-video-fetch (下载视频文件)
        ↓
使用 douyin-content-parser 生成最终报告
```

## 配置要求

### 系统依赖
- Python 3.8+
- Playwright: `playwright install chromium`
- aiohttp: `pip install aiohttp`

### 使用示例
```bash
# 单个视频下载
python scripts/fetch_video.py "https://v.douyin.com/qchH_0YurEA/"

# 批量下载
echo "https://v.douyin.com/qchH_0YurEA/" > urls.txt
python scripts/fetch_video.py --file urls.txt --output-dir ./downloads

# 使用整合脚本
python scripts/douyin_master_parser.py "https://v.douyin.com/qchH_0YurEA/"
```

## 输出目录
- 默认下载目录: `./downloads/`
- 文件命名: `<video_id>.mp4`

## 注意事项
1. 由于使用浏览器自动化，执行时间较长（通常30-60秒）
2. 可能受到抖音反爬虫机制的影响
3. 建议在非高峰时段使用以获得更好的成功率