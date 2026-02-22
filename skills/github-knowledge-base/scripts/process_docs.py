#!/usr/bin/env python3
"""
Process GitHub repository files into a knowledge base format.
Converts code, markdown, and documentation files into searchable text.
"""
import os
import re
from pathlib import Path
from typing import List, Dict

def is_text_file(filepath: str) -> bool:
    """Check if file is likely a text file based on extension."""
    text_extensions = {
        '.md', '.txt', '.py', '.js', '.ts', '.java', '.cpp', '.h', 
        '.c', '.go', '.rs', '.rb', '.php', '.html', '.css', '.json',
        '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.sh',
        '.bash', '.zsh', '.fish', '.sql', '.xml', '.csv'
    }
    return Path(filepath).suffix.lower() in text_extensions

def should_skip_file(filepath: str) -> bool:
    """Check if file should be skipped (binary, large, or irrelevant)."""
    skip_patterns = [
        '__pycache__/', '.git/', 'node_modules/', 'dist/', 'build/',
        '.venv/', 'venv/', '.env', '.DS_Store', '.vscode/', '.idea/',
        '*.min.js', '*.min.css', '*.map', '*.lock', '*.log', '*.tmp',
        '*.bin', '*.exe', '*.dll', '*.so', '*.dylib', '*.o', '*.obj'
    ]
    
    filepath_str = str(filepath).replace('\\', '/')
    for pattern in skip_patterns:
        if pattern.endswith('/'):
            if pattern[:-1] in filepath_str.split('/'):
                return True
        elif '*' in pattern:
            # Simple glob matching
            regex_pattern = pattern.replace('*', '.*').replace('.', r'\.')
            if re.search(regex_pattern, filepath_str):
                return True
        else:
            if pattern == os.path.basename(filepath_str):
                return True
    
    # Skip very large files (>1MB)
    try:
        if os.path.getsize(filepath) > 1024 * 1024:
            return True
    except OSError:
        pass
    
    return False

def process_repository(repo_path: str, output_file: str = None) -> str:
    """
    Process all relevant files in a repository into a knowledge base format.
    
    Args:
        repo_path: Path to cloned repository
        output_file: Optional output file path. If None, returns content as string.
    
    Returns:
        Path to output file or processed content string
    """
    repo_path = Path(repo_path)
    processed_content = []
    
    for filepath in repo_path.rglob('*'):
        if filepath.is_file() and not should_skip_file(filepath):
            if is_text_file(str(filepath)):
                try:
                    relative_path = filepath.relative_to(repo_path)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Add file header
                    processed_content.append(f"\n{'='*80}\n")
                    processed_content.append(f"File: {relative_path}\n")
                    processed_content.append(f"{'='*80}\n")
                    processed_content.append(content)
                    processed_content.append(f"\n{'-'*80}\n")
                    
                except Exception as e:
                    print(f"⚠️  Skipping {filepath}: {e}")
    
    final_content = "".join(processed_content)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"✅ Knowledge base created: {output_file}")
        return output_file
    else:
        return final_content

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python process_docs.py <repo_path> [output_file]")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = process_repository(repo_path, output_file)
    if not output_file:
        print(result)