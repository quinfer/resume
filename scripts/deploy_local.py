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
    
    # First, build the primary CV website
    print("📦 Building CV website...")
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
        "custom-styles.css",
        "index_files",   # Directory with assets for index
        "img",           # Image directory
    ]

    # Only publish the complete CV PDF
    cv_pdf_files = ["index.pdf"]
    
    pdf_files = []
    for pdf_name in cv_pdf_files:
        pdf_path = dist_dir / pdf_name
        if pdf_path.exists():
            files_to_copy.append(pdf_name)
            pdf_files.append(pdf_path)
    
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

    # Remove demoted variant CVs from previous deployments
    stale_items = [
        "cv_academic.html",
        "cv_academic_files",
        "cv_academic.pdf",
        "cv_industry.html",
        "cv_industry_files",
        "cv_industry.pdf",
        "cv_grants.html",
        "cv_grants_files",
        "cv_grants.pdf",
    ]
    print("\n🧹 Removing demoted variant CV files from root...")
    for item in stale_items:
        path = root_dir / item
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"  🗑️  Removed: {item}")

    print("\n🌐 Local GitHub Pages setup complete!")
    print("📋 Files in root directory:")
    print("   - index.html (main website)")
    print("   - index_files/ (website assets)")
    print("   - img/ (profile picture and images)")
    print(f"   - {len(pdf_files)} CV PDF file(s) (index.pdf)")
    print("\n💡 Tailored extracts remain in src/; build with: python3 scripts/build_cvs.py --all")
    print("🔗 GitHub Pages will now work from root directory")
    
    return 0

if __name__ == "__main__":
    exit(main())
