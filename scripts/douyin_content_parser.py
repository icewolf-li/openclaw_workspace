#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import json
import time
import os
import tempfile
import subprocess
import requests
from urllib.parse import urlparse, parse_qs

def extract_modal_id_from_url(url):
    """从抖音链接中提取modal_id或video_id"""
    # 处理短链接重定向
    if 'v.douyin.com' in url:
        try:
            response = requests.head(url, allow_redirects=True, timeout=10)
            final_url = response.url
            print(f"重定向到: {final_url}", file=sys.stderr)
            
            # 从重定向URL中提取video_id
            video_match = re.search(r'/video/(\d+)', final_url)
            if video_match:
                return video_match.group(1)
                
            # 从查询参数中提取modal_id
            parsed = urlparse(final_url)
            query_params = parse_qs(parsed.query)
            if 'modal_id' in query_params:
                return query_params['modal_id'][0]
        except Exception as e:
            print(f"解析短链接失败: {e}", file=sys.stderr)
    
    # 直接从URL中提取video_id
    video_match = re.search(r'/video/(\d+)', url)
    if video_match:
        return video_match.group(1)
    
    # 从URL中提取modal_id
    modal_match = re.search(r'modal_id=(\d+)', url)
    if modal_match:
        return modal_match.group(1)
    
    # 如果输入本身就是数字ID
    if url.isdigit():
        return url
    
    return None

def get_douyin_video_info(video_id, api_token):
    """使用TikHub API获取抖音视频信息"""
    if not video_id:
        return None
    
    # 尝试不同的API端点
    api_endpoints = [
        f"https://api.tikhub.io/douyin/video_data?video_id={video_id}",
        f"https://api.tikhub.io/douyin/video_detail?video_id={video_id}"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    for api_url in api_endpoints:
        try:
            print(f"尝试API: {api_url}", file=sys.stderr)
            response = requests.get(api_url, headers=headers, timeout=30)
            print(f"API响应状态: {response.status_code}", file=sys.stderr)
            
            if response.status_code == 200:
                data = response.json()
                print(f"API响应数据: {json.dumps(data, ensure_ascii=False)}", file=sys.stderr)
                
                if data.get('status') == 'success' or 'data' in data:
                    video_info = data.get('data', {}) if isinstance(data.get('data'), dict) else {}
                    
                    # 处理不同格式的API响应
                    if 'title' in video_info:
                        return {
                            'title': video_info.get('title', '未知标题'),
                            'author': video_info.get('author', {}).get('nickname', '未知作者'),
                            'description': video_info.get('desc', '') or video_info.get('description', ''),
                            'cover_url': video_info.get('cover_url', '') or video_info.get('cover', ''),
                            'video_url': video_info.get('video_url', '') or video_info.get('play_addr', ''),
                            'duration': video_info.get('duration', 0),
                            'create_time': video_info.get('create_time', '')
                        }
                    elif 'aweme_detail' in video_info:
                        # 处理抖音原生API格式
                        aweme = video_info['aweme_detail']
                        return {
                            'title': aweme.get('desc', '未知标题'),
                            'author': aweme.get('author', {}).get('nickname', '未知作者'),
                            'description': aweme.get('desc', ''),
                            'cover_url': aweme.get('video', {}).get('cover', {}).get('url_list', [''])[0],
                            'video_url': aweme.get('video', {}).get('play_addr', {}).get('url_list', [''])[0],
                            'duration': aweme.get('video', {}).get('duration', 0) // 1000,  # 转换为秒
                            'create_time': aweme.get('create_time', '')
                        }
            else:
                print(f"HTTP错误: {response.status_code}", file=sys.stderr)
                if response.status_code == 404:
                    continue  # 尝试下一个端点
        except Exception as e:
            print(f"API请求异常: {e}", file=sys.stderr)
            continue
    
    return None

def generate_content_summary(video_info):
    """生成内容摘要"""
    if not video_info:
        return {"error": "无法获取视频信息"}
    
    summary = {
        'title': video_info.get('title', '未知标题'),
        'author': video_info.get('author', '未知作者'),
        'description': video_info.get('description', ''),
        'duration': video_info.get('duration', 0),
        'create_time': video_info.get('create_time', ''),
        'summary_text': f"视频标题: {video_info.get('title', '未知标题')}\n"
                       f"作者: {video_info.get('author', '未知作者')}\n"
                       f"描述: {video_info.get('description', '')}\n"
                       f"时长: {video_info.get('duration', 0)}秒"
    }
    return summary

def main():
    if len(sys.argv) < 3:
        print("用法: python douyin_content_parser.py <抖音链接或modal_id> <api_token>", file=sys.stderr)
        sys.exit(1)
    
    input_arg = sys.argv[1]
    api_token = sys.argv[2]
    
    print(f"输入参数: {input_arg}", file=sys.stderr)
    
    # 提取视频ID
    video_id = extract_modal_id_from_url(input_arg)
    print(f"提取的视频ID: {video_id}", file=sys.stderr)
    
    if not video_id:
        print("无法从输入中提取视频ID", file=sys.stderr)
        sys.exit(1)
    
    # 获取视频信息
    video_info = get_douyin_video_info(video_id, api_token)
    
    if not video_info:
        print("无法获取视频信息", file=sys.stderr)
        sys.exit(1)
    
    # 生成内容摘要
    summary = generate_content_summary(video_info)
    
    # 输出JSON结果
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()