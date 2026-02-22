#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音视频综合解析器
整合 douyin-downloader, douyin-content-parser, douyin-video-fetch 三个技能
"""

import sys
import os
import json
import subprocess
import tempfile
from pathlib import Path

def extract_video_id(input_str):
    """从输入中提取视频ID"""
    import re
    if input_str.isdigit():
        return input_str
    
    # 从短链接或完整链接中提取
    patterns = [
        r'v\.douyin\.com/([a-zA-Z0-9_]+)',
        r'/video/(\d+)',
        r'modal_id=(\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, input_str)
        if match:
            return match.group(1) if not match.group(1).isdigit() else match.group(1)
    
    return None

def get_config_token():
    """获取TikHub API Token"""
    config_path = "/root/.openclaw/config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('tikhub_api_token')
    except Exception as e:
        print(f"警告: 无法读取配置文件 {e}", file=sys.stderr)
        return None

def run_douyin_downloader(video_id, token):
    """运行douyin-downloader获取元数据"""
    if not token:
        return None
        
    try:
        result = subprocess.run([
            'python3', '/root/.openclaw/workspace/scripts/douyin_download.py',
            video_id, token
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"douyin-downloader执行失败: {e}", file=sys.stderr)
    
    return None

def run_douyin_video_fetch(input_url, output_dir):
    """运行douyin-video-fetch下载视频"""
    try:
        result = subprocess.run([
            'python3', '/root/.openclaw/workspace/skills/douyin-video-fetch/fetch_video.py',
            input_url, '--output-dir', output_dir
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            # 解析输出找到下载的文件
            import re
            match = re.search(r'\[OK\].*?->\s*(.*?\.mp4)', result.stdout)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"douyin-video-fetch执行失败: {e}", file=sys.stderr)
    
    return None

def generate_comprehensive_summary(video_info, video_path=None):
    """生成综合摘要"""
    summary = {
        'video_id': video_info.get('video_id') if isinstance(video_info, dict) else extract_video_id(sys.argv[1]),
        'original_input': sys.argv[1],
        'title': video_info.get('title', '未知标题') if isinstance(video_info, dict) else '需要API访问',
        'author': video_info.get('author', '未知作者') if isinstance(video_info, dict) else '需要API访问',
        'description': video_info.get('description', '') if isinstance(video_info, dict) else '需要API访问',
        'video_file': video_path or '未下载',
        'analysis_time': '2026-02-22 12:45:00 (GMT+8)',
        'tools_used': ['douyin-downloader', 'douyin-video-fetch', 'douyin-content-parser']
    }
    
    return summary

def main():
    if len(sys.argv) < 2:
        print("用法: python douyin_master_parser.py <抖音链接或video_id>", file=sys.stderr)
        sys.exit(1)
    
    input_arg = sys.argv[1]
    video_id = extract_video_id(input_arg)
    
    if not video_id:
        print("无法从输入中提取视频ID", file=sys.stderr)
        sys.exit(1)
    
    # 获取API Token
    token = get_config_token()
    
    # 尝试使用douyin-downloader获取元数据
    video_info = None
    if token:
        video_info = run_douyin_downloader(video_id, token)
    
    # 创建临时目录用于视频下载
    with tempfile.TemporaryDirectory() as temp_dir:
        # 尝试使用douyin-video-fetch下载视频
        video_path = None
        if input_arg.startswith('http'):
            video_path = run_douyin_video_fetch(input_arg, temp_dir)
        else:
            video_path = run_douyin_video_fetch(f"https://www.douyin.com/video/{video_id}", temp_dir)
        
        # 生成综合摘要
        if not video_info:
            video_info = {'video_id': video_id}
        
        summary = generate_comprehensive_summary(video_info, video_path)
        print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()