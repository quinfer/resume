#!/usr/bin/env python3
"""
Local deployment script for GitHub Pages compatibility
Copies main website files from dist/ to root directory
"""

import shutil
import subprocess
from pathlib import Path

def main():
    """Copy website files to root for GitHub Pages"""
    print("🚀 Preparing local GitHub Pages deployment...")
    
    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    import os
    os.chdir(project_root)
    
    # First, build everything
    print("📦 Building all CV versions...")
    result = subprocess.run(["python3", "scripts/build_cvs.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Build failed!")
        print(result.stderr)
        return 1
    
    # Copy main website files to root
    dist_dir = Path("dist")
    root_dir = Path(".")
    
    files_to_copy = [
        "index.html",
        "index_files"  # Directory with assets
    ]
    
    print("📁 Copying website files to root directory...")
    
    for item in files_to_copy:
        src = dist_dir / item
        dst = root_dir / item
        
        if src.exists():
            # Remove existing file/directory
            if dst.exists():
                if dst.is_dir():
                    shutil.rmtree(dst)
                else:
                    dst.unlink()
            
            # Copy new file/directory
            if src.is_dir():
                shutil.copytree(src, dst)
                print(f"  ✅ Copied directory: {item}")
            else:
                shutil.copy2(src, dst)
                print(f"  ✅ Copied file: {item}")
        else:
            print(f"  ⚠️  File not found: {item}")
    
    print("\n🌐 Local GitHub Pages setup complete!")
    print("📋 Files in root directory:")
    print("   - index.html (main website)")
    print("   - index_files/ (website assets)")
    print("\n💡 Note: dist/ folder still contains all CV versions")
    print("🔗 GitHub Pages will now work from root directory")
    
    return 0

if __name__ == "__main__":
    exit(main())
