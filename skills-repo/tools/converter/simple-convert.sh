#!/bin/bash

# 简单的技能转换脚本
# 用法: ./simple-convert.sh <input_dir> <output_dir> <platform>

if [ $# -ne 3 ]; then
    echo "Usage: $0 <input_dir> <output_dir> <platform>"
    echo "Platform: openclaw, iflow"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"
PLATFORM="$3"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 复制所有文件
cp -r "$INPUT_DIR"/* "$OUTPUT_DIR"/

# 根据平台修改 SKILL.md
if [ "$PLATFORM" = "openclaw" ]; then
    # 为 OpenClaw 添加特定元数据
    SKILL_FILE="$OUTPUT_DIR/SKILL.md"
    if [ -f "$SKILL_FILE" ]; then
        # 在 frontmatter 中添加 OpenClaw 特定字段
        sed -i 's/---/---\nmetadata:\n  openclaw:\n    universal_source: true\n    supported: true\n---/' "$SKILL_FILE"
        echo "Converted to OpenClaw format"
    fi
elif [ "$PLATFORM" = "iflow" ]; then
    # 为 iFlow 创建简化版本
    SKILL_FILE="$OUTPUT_DIR/SKILL.md"
    if [ -f "$SKILL_FILE" ]; then
        # 添加 iFlow 标识
        sed -i "s/description:/description: [iFlow Compatible] &/" "$SKILL_FILE"
        echo "Converted to iFlow format"
    fi
else
    echo "Unsupported platform: $PLATFORM"
    exit 1
fi

echo "Conversion completed: $INPUT_DIR -> $OUTPUT_DIR ($PLATFORM)"