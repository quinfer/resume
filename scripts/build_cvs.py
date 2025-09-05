#!/usr/bin/env python3
"""
Build script for Prof. Barry Quinn's CV versions
Generates all HTML and PDF versions using Quarto
"""

import subprocess
import sys
from pathlib import Path
import time

def run_command(command, description):
    """Run a command and return success status"""
    print(f"  → {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ {description} completed")
            return True
        else:
            print(f"  ❌ Error in {description}: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ Exception in {description}: {e}")
        return False

def build_cv(filename):
    """Build both HTML and PDF versions of a CV file"""
    if not Path(filename).exists():
        print(f"❌ File not found: {filename}")
        return False
    
    print(f"📄 Building {filename}...")
    
    # Build HTML version (output to dist/)
    html_success = run_command(
        f"quarto render {filename} --to html --output-dir dist",
        f"HTML version of {filename}"
    )
    
    # Build PDF version (output to dist/)
    pdf_success = run_command(
        f"quarto render {filename} --to pdf --output-dir dist", 
        f"PDF version of {filename}"
    )
    
    return html_success and pdf_success

def list_generated_files():
    """List all generated HTML and PDF files"""
    print("\n📁 Generated files in dist/:")
    
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("No dist directory found")
        return
    
    html_files = list(dist_dir.glob("*.html"))
    if html_files:
        print("\nHTML files:")
        for file in sorted(html_files):
            print(f" - {file}")
    
    pdf_files = list(dist_dir.glob("*.pdf"))
    if pdf_files:
        print("\nPDF files:")
        for file in sorted(pdf_files):
            print(f" - {file}")

def copy_assets():
    """Copy assets to dist directory"""
    import shutil
    
    # Copy img directory to dist/
    src_img = Path("assets/img")
    dst_img = Path("dist/img")
    
    if src_img.exists():
        if dst_img.exists():
            shutil.rmtree(dst_img)
        shutil.copytree(src_img, dst_img)
        print(f"  ✅ Copied assets/img/ to dist/img/")

    # Copy custom CSS to dist/
    src_css = Path("assets/custom-styles.css")
    dst_css = Path("dist/custom-styles.css")
    if src_css.exists():
        shutil.copy2(src_css, dst_css)
        print(f"  ✅ Copied assets/custom-styles.css to dist/")

def main():
    """Main build process"""
    print("🚀 Building all CV versions...\n")
    
    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    import os
    os.chdir(project_root)
    
    # Ensure dist directory exists
    Path("dist").mkdir(exist_ok=True)
    
    # Copy assets first
    copy_assets()
    
    # CV files to build (in src directory)
    cv_files = [
        "src/index.qmd",        # Main website
        "src/cv_academic.qmd",  # Academic version
        "src/cv_industry.qmd",  # Industry version
        "src/cv_grants.qmd"     # Grant application version
    ]
    
    success_count = 0
    total_files = len(cv_files)
    
    # Build each CV version
    for cv_file in cv_files:
        if build_cv(cv_file):
            success_count += 1
        print()  # Add spacing between files
    
    # Summary
    print("🎉 Build process completed!")
    print(f"📊 Success rate: {success_count}/{total_files} files built successfully")
    
    if success_count == total_files:
        print("✨ All CV versions built successfully!")
        list_generated_files()
        print("\n🌐 Your resume website is ready! Open dist/index.html in a browser to view.")
    else:
        print("⚠️  Some files failed to build. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
