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

def pdf_output_format(filename):
    """Use Typst for the complete CV; LaTeX PDF for optional variant extracts."""
    if filename == "src/index.qmd":
        return "typst"
    return "pdf"


def build_cv(filename):
    """Build HTML and PDF versions of a CV file"""
    if not Path(filename).exists():
        print(f"❌ File not found: {filename}")
        return False
    
    print(f"📄 Building {filename}...")
    
    # Build HTML version (output to project-root dist/)
    # NOTE: Quarto resolves --output-dir relative to the input file location.
    # Since our .qmd files live in src/, use an absolute dist/ path.
    project_root = Path(__file__).parent.parent
    dist_dir = (project_root / "dist").resolve()
    pdf_format = pdf_output_format(filename)

    html_success = run_command(
        f"quarto render {filename} --to html --output-dir \"{dist_dir}\"",
        f"HTML version of {filename}"
    )
    
    pdf_success = run_command(
        f"quarto render {filename} --to {pdf_format} --output-dir \"{dist_dir}\"",
        f"PDF version of {filename} ({pdf_format})"
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

def remove_stale_variants():
    """Remove demoted variant CV outputs from dist/ when not building --all."""
    import shutil

    stale = [
        "cv_academic.html", "cv_academic.pdf", "cv_academic_files",
        "cv_industry.html", "cv_industry.pdf", "cv_industry_files",
        "cv_grants.html", "cv_grants.pdf", "cv_grants_files",
    ]
    dist_dir = Path("dist")
    for name in stale:
        path = dist_dir / name
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"  🗑️  Removed dist/{name}")

def main():
    """Main build process"""
    print("🚀 Building CV website...\n")
    
    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    import os
    os.chdir(project_root)
    
    # Ensure dist directory exists
    Path("dist").mkdir(exist_ok=True)
    
    # Copy assets first
    copy_assets()
    
    # Primary published CV (website + PDF)
    cv_files = [
        "src/index.qmd",
    ]

    # Optional tailored extracts — build with: python3 scripts/build_cvs.py --all
    if "--all" in sys.argv:
        cv_files.extend([
            "src/cv_academic.qmd",
            "src/cv_industry.qmd",
            "src/cv_grants.qmd",
        ])
    
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
        if "--all" not in sys.argv:
            print("\n🧹 Cleaning demoted variant outputs from dist/...")
            remove_stale_variants()
        print("✨ CV website built successfully!")
        list_generated_files()
        print("\n🌐 Open dist/index.html in a browser to view.")
        if "--all" not in sys.argv:
            print("ℹ️  Tailored extracts are skipped by default. Use --all to build cv_academic, cv_industry, and cv_grants.")
    else:
        print("⚠️  Some files failed to build. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
