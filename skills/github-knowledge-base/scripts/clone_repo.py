#!/usr/bin/env python3
"""
Clone a GitHub repository to local workspace for knowledge base processing.
"""
import os
import sys
import subprocess
import tempfile
from pathlib import Path

def clone_github_repo(repo_url: str, target_dir: str = None) -> str:
    """
    Clone a GitHub repository to a local directory.
    
    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/user/repo)
        target_dir: Optional target directory. If None, uses temp directory.
    
    Returns:
        Path to cloned repository
    """
    if target_dir is None:
        target_dir = tempfile.mkdtemp(prefix="github_kb_")
    
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Clone the repository
    try:
        subprocess.run([
            "git", "clone", "--depth=1", 
            repo_url, target_dir
        ], check=True, capture_output=True, text=True)
        print(f"✅ Successfully cloned {repo_url} to {target_dir}")
        return target_dir
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone repository: {e.stderr}")
        raise

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clone_repo.py <github_repo_url> [target_directory]")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    cloned_path = clone_github_repo(repo_url, target_dir)
    print(f"Repository cloned to: {cloned_path}")