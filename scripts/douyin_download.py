#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import json
import time
import requests
from urllib.parse import urlparse, parse_qs

def extract_modal_id(url):
    """从抖音链接中提取modal_id"""
    # 处理短链接
    if 'v.douyin.com' in url:
        try:
            response = requests.head(url, allow_redirects=True, timeout=10)
            final_url = response.url
            parsed = urlparse(final_url)
            query_params = parse_qs(parsed.query)
            if 'modal_id' in query_params:
                return query_params['modal_id'][0]
        except Exception as e:
            print(f"解析短链接失败: {e}", file=sys.stderr)
    
    # 直接从URL中提取modal_id
    modal_match = re.search(r'modal_id=(\d+)', url)
    if modal_match:
        return modal_match.group(1)
    
    # 尝试从其他格式中提取
    video_id_match = re.search(r'/video/(\d+)', url)
    if video_id_match:
        return video_id_match.group(1)
    
    return None

def download_douyin_video(modal_id, api_token):
    """使用TikHub API下载抖音视频"""
    if not modal_id:
        print("无法提取视频ID", file=sys.stderr)
        return None
    
    # TikHub API endpoint
    api_url = f"https://api.tikhub.io/douyin/video_data?video_id={modal_id}"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                video_info = data.get('data', {})
                return {
                    'title': video_info.get('title', '未知标题'),
                    'author': video_info.get('author', {}).get('nickname', '未知作者'),
                    'description': video_info.get('desc', ''),
                    'cover_url': video_info.get('cover_url', ''),
                    'video_url': video_info.get('video_url', ''),
                    'duration': video_info.get('duration', 0),
                    'create_time': video_info.get('create_time', '')
                }
            else:
                print(f"API返回错误: {data.get('message', '未知错误')}", file=sys.stderr)
        else:
            print(f"HTTP错误: {response.status_code}", file=sys.stderr)
    except Exception as e:
        print(f"下载失败: {e}", file=sys.stderr)
    
    return None

def main():
    if len(sys.argv) < 3:
        print("用法: python douyin_download.py <抖音链接或modal_id> <api_token>", file=sys.stderr)
        sys.exit(1)
    
    input_arg = sys.argv[1]
    api_token = sys.argv[2]
    
    # 提取modal_id
    if input_arg.isdigit():
        modal_id = input_arg
    else:
        modal_id = extract_modal_id(input_arg)
    
    if not modal_id:
        print("无法从输入中提取视频ID", file=sys.stderr)
        sys.exit(1)
    
    # 下载视频信息
    video_info = download_douyin_video(modal_id, api_token)
    
    if video_info:
        print(json.dumps(video_info, ensure_ascii=False, indent=2))
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()