#!/usr/bin/env node
/**
 * 跨平台技能转换器
 * 将通用技能格式转换为各平台特定格式
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

function loadUniversalSkill(skillPath) {
    const skillFile = path.join(skillPath, 'SKILL.md');
    if (!fs.existsSync(skillFile)) {
        throw new Error(`SKILL.md not found in ${skillPath}`);
    }
    
    const content = fs.readFileSync(skillFile, 'utf8');
    
    // 分离 frontmatter 和内容
    if (content.startsWith('---')) {
        const parts = content.split('---', 3);
        if (parts.length >= 3) {
            const frontmatter = yaml.load(parts[1]);
            const body = parts[2];
            return { frontmatter, body };
        }
    }
    return { frontmatter: {}, body: content };
}

function convertToOpenClaw(frontmatter, body, outputPath) {
    // OpenClaw 使用标准的 SKILL.md 格式
    const openclawFrontmatter = {
        name: frontmatter.name,
        description: frontmatter.description,
        metadata: {
            openclaw: {
                universal_source: true,
                original_version: frontmatter.universal_version || '1.0.0'
            }
        }
    };
    
    // 添加平台特定的元数据
    if (frontmatter.platforms && frontmatter.platforms.includes('openclaw')) {
        openclawFrontmatter.metadata.openclaw.supported = true;
    }
    
    writeSkillFile(outputPath, openclawFrontmatter, body);
}

function convertToIFlow(frontmatter, body, outputPath) {
    // iFlow 可能需要不同的结构
    const iflowContent = `# ${frontmatter.name || 'Unknown Skill'}
${body}

## iFlow 配置
\`\`\`json
{
  "name": "${frontmatter.name}",
  "description": "${frontmatter.description || ''}",
  "version": "${frontmatter.universal_version || '1.0.0'}",
  "platform": "iflow",
  "universal_source": true
}
\`\`\`
`;
    fs.mkdirSync(outputPath, { recursive: true });
    fs.writeFileSync(path.join(outputPath, 'SKILL.md'), iflowContent, 'utf8');
}

function writeSkillFile(outputPath, frontmatter, body) {
    fs.mkdirSync(outputPath, { recursive: true });
    const content = `---
${yaml.dump(frontmatter, { noRefs: true }).trim()}
---
${body}`;
    fs.writeFileSync(path.join(outputPath, 'SKILL.md'), content, 'utf8');
}

function main() {
    const args = process.argv.slice(2);
    if (args.length !== 6 || 
        args[0] !== '--input' || 
        args[2] !== '--output' || 
        args[4] !== '--platform') {
        console.log('Usage: node convert.js --input <input_path> --output <output_path> --platform <platform>');
        process.exit(1);
    }
    
    const inputPath = args[1];
    const outputPath = args[3];
    const platform = args[5];
    
    try {
        const { frontmatter, body } = loadUniversalSkill(inputPath);
        
        if (platform === 'openclaw') {
            convertToOpenClaw(frontmatter, body, outputPath);
        } else if (platform === 'iflow') {
            convertToIFlow(frontmatter, body, outputPath);
        } else {
            console.error(`Unsupported platform: ${platform}`);
            process.exit(1);
        }
        
        console.log(`Converted ${inputPath} to ${platform} format at ${outputPath}`);
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}