#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import json
import requests
from urllib.parse import urlparse, parse_qs

def extract_video_id_from_url(url):
    """从抖音URL中提取视频ID"""
    # 处理短链接重定向
    if 'v.douyin.com' in url:
        try:
            response = requests.head(url, allow_redirects=True, timeout=10)
            final_url = response.url
            # 从重定向URL中提取视频ID
            video_id_match = re.search(r'/video/(\d+)', final_url)
            if video_id_match:
                return video_id_match.group(1)
        except Exception as e:
            print(f"解析短链接失败: {e}", file=sys.stderr)
    
    # 直接从URL中提取
    video_id_match = re.search(r'/video/(\d+)', url)
    if video_id_match:
        return video_id_match.group(1)
    
    # 从modal_id参数中提取
    modal_match = re.search(r'modal_id=(\d+)', url)
    if modal_match:
        return modal_match.group(1)
    
    # 如果输入本身就是数字ID
    if url.isdigit():
        return url
    
    return None

def parse_douyin_content(video_id, original_url):
    """解析抖音内容并生成摘要"""
    # 由于API可能不可用，我们基于已知信息生成摘要
    summary = {
        'video_id': video_id,
        'original_url': original_url,
        'title': '抖音视频内容分析',
        'author': '未知作者',
        'description': '该视频需要通过API获取详细信息，当前无法访问完整内容',
        'summary_text': f"视频ID: {video_id}\n"
                       f"原始链接: {original_url}\n"
                       f"注意: 由于API限制，无法获取完整的视频元数据。\n"
                       f"建议手动查看视频内容或提供更多信息。"
    }
    return summary

def main():
    if len(sys.argv) < 2:
        print("用法: python simple_douyin_parser.py <抖音链接或视频ID>", file=sys.stderr)
        sys.exit(1)
    
    input_arg = sys.argv[1]
    video_id = extract_video_id_from_url(input_arg)
    
    if not video_id:
        print("无法从输入中提取视频ID", file=sys.stderr)
        sys.exit(1)
    
    summary = parse_douyin_content(video_id, input_arg)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()