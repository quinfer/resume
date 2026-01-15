#!/usr/bin/env python3
"""
Development build script for quick CV testing
Only builds HTML versions for faster iteration
"""

import subprocess
import sys
from pathlib import Path

def build_html(filename):
    """Build HTML version only for quick preview"""
    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    import os
    os.chdir(project_root)
    
    if not Path(filename).exists():
        print(f"❌ File not found: {filename}")
        return False
    
    print(f"🔄 Building HTML for {filename}...")
    try:
        # NOTE: Quarto resolves --output-dir relative to the input file location.
        # Our .qmd files live in src/, so use an absolute project-root dist/ path.
        dist_dir = (project_root / "dist").resolve()

        result = subprocess.run(
            f"quarto render {filename} --to html --output-dir \"{dist_dir}\"", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {filename} → HTML completed")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Main development build process"""
    if len(sys.argv) > 1:
        # Build specific file if provided
        filename = sys.argv[1]
        if not filename.endswith('.qmd'):
            filename = f"src/{filename}.qmd"
        
        print(f"🚀 Development build for {filename}...")
        success = build_html(filename)
        
        if success:
            base_name = Path(filename).stem
            print(f"🌐 Preview ready: open dist/{base_name}.html")
        
        return 0 if success else 1
    
    else:
        # Build all files (HTML only)
        print("🚀 Development build (HTML only) for all CVs...")
        
        cv_files = ["src/index.qmd", "src/cv_academic.qmd", "src/cv_industry.qmd", "src/cv_grants.qmd"]
        success_count = 0
        
        for cv_file in cv_files:
            if build_html(cv_file):
                success_count += 1
        
        print(f"\n📊 Built {success_count}/{len(cv_files)} files successfully")
        
        if success_count > 0:
            print("🌐 Preview ready: open dist/index.html")
        
        return 0 if success_count == len(cv_files) else 1

if __name__ == "__main__":
    sys.exit(main())
