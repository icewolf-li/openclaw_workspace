#!/bin/bash

# 抖音内容解析器使用示例

echo "=== 抖音内容解析器使用示例 ==="

# 获取API token
API_TOKEN=$(jq -r '.tikhub_api_token' ~/.openclaw/config.json)

if [ "$API_TOKEN" = "null" ]; then
    echo "错误: 请在 ~/.openclaw/config.json 中配置 tikhub_api_token"
    exit 1
fi

# 示例1: 解析抖音链接
echo ""
echo "示例1: 解析抖音链接"
echo "链接: https://v.douyin.com/qchH_0YurEA/"
cd /root/.openclaw/workspace && python3 scripts/simple_douyin_parser.py "https://v.douyin.com/qchH_0YurEA/" "$API_TOKEN"

echo ""
echo "=== 使用说明 ==="
echo "基本用法:"
echo "python3 scripts/simple_douyin_parser.py <抖音链接或视频ID> <API_TOKEN>"
echo ""
echo "支持的输入格式:"
echo "- 短链接: https://v.douyin.com/xxxxx/"
echo "- 完整链接: https://www.douyin.com/video/1234567890"
echo "- 视频ID: 1234567890"