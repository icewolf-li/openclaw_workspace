#!/usr/bin/env python3
"""
跨平台技能转换器
将通用技能格式转换为各平台特定格式
"""

import os
import sys
import json
import yaml
import shutil
from pathlib import Path

def load_universal_skill(skill_path):
    """加载通用技能定义"""
    skill_file = Path(skill_path) / "SKILL.md"
    if not skill_file.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")
    
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分离 frontmatter 和内容
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2]
            return frontmatter, body
    return {}, content

def convert_to_openclaw(frontmatter, body, output_path):
    """转换为 OpenClaw 格式"""
    # OpenClaw 使用标准的 SKILL.md 格式
    openclaw_frontmatter = {
        'name': frontmatter.get('name'),
        'description': frontmatter.get('description'),
        'metadata': {
            'openclaw': {
                'universal_source': True,
                'original_version': frontmatter.get('universal_version', '1.0.0')
            }
        }
    }
    
    # 添加平台特定的元数据
    if 'platforms' in frontmatter and 'openclaw' in frontmatter['platforms']:
        openclaw_frontmatter['metadata']['openclaw']['supported'] = True
    
    write_skill_file(output_path, openclaw_frontmatter, body)

def convert_to_iflow(frontmatter, body, output_path):
    """转换为 iFlow 格式"""
    # iFlow 可能需要不同的结构
    iflow_content = f"""# {frontmatter.get('name', 'Unknown Skill')}
{body}

## iFlow 配置
```json
{{
  "name": "{frontmatter.get('name')}",
  "description": "{frontmatter.get('description', '')}",
  "version": "{frontmatter.get('universal_version', '1.0.0')}",
  "platform": "iflow",
  "universal_source": true
}}
```
"""
    (Path(output_path) / "SKILL.md").write_text(iflow_content, encoding='utf-8')

def write_skill_file(output_path, frontmatter, body):
    """写入技能文件"""
    Path(output_path).mkdir(parents=True, exist_ok=True)
    content = f"""---
{yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True).strip()}
---
{body}"""
    (Path(output_path) / "SKILL.md").write_text(content, encoding='utf-8')

def main():
    if len(sys.argv) != 4:
        print("Usage: python convert.py --input <input_path> --output <output_path> --platform <platform>")
        sys.exit(1)
    
    input_path = sys.argv[2]
    output_path = sys.argv[4]
    platform = sys.argv[6]
    
    frontmatter, body = load_universal_skill(input_path)
    
    if platform == 'openclaw':
        convert_to_openclaw(frontmatter, body, output_path)
    elif platform == 'iflow':
        convert_to_iflow(frontmatter, body, output_path)
    else:
        print(f"Unsupported platform: {platform}")
        sys.exit(1)
    
    print(f"Converted {input_path} to {platform} format at {output_path}")

if __name__ == "__main__":
    main()