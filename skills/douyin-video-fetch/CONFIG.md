# Douyin Video Fetch 配置指南

## 依赖要求

### 系统依赖
- Python 3.8+
- Playwright (已包含在脚本中)
- aiohttp

### 安装Playwright浏览器
```bash
playwright install chromium
```

## 使用配置

### 单视频下载
```bash
python scripts/fetch_video.py "https://v.douyin.com/qchH_0YurEA/"
```

### 批量下载
创建输入文件 `input.txt`:
```
https://v.douyin.com/qchH_0YurEA/
7580266475575905536
https://www.douyin.com/video/7599980362898427178
```

执行批量下载：
```bash
python scripts/fetch_video.py --file input.txt --output-dir ./downloads/douyin
```

## 输出目录结构
```
downloads/
├── 7580266475575905536.mp4
├── 7599980362898427178.mp4
└── ...
```

## 与现有技能集成

### 结合 douyin-content-parser
1. 先用 `douyin-video-fetch` 下载视频
2. 再用 `douyin-content-parser` 分析内容
3. 生成完整的Markdown报告

### 工作流程示例
```bash
# 1. 下载视频
python scripts/fetch_video.py "https://v.douyin.com/qchH_0YurEA/"

# 2. 提取视频ID并分析
VIDEO_ID="7580266475575905536"
python scripts/simple_douyin_parser.py $VIDEO_ID > analysis.json

# 3. 生成Markdown报告
# (使用之前创建的脚本)
```

## 注意事项

- **网络要求**: 需要能够访问抖音网站
- **反爬虫**: 抖音有WAF防护，脚本已包含挑战处理逻辑
- **存储空间**: 确保有足够的磁盘空间存储视频文件
- **速率限制**: 批量下载时建议添加延迟避免被封IP