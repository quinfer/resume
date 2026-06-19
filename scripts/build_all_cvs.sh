#!/bin/bash
# Build script for Prof. Barry Quinn's CV versions
# Generates all HTML and PDF versions using Quarto

set -e  # Exit on error

# Change to project root directory (parent of scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "🚀 Building CV website..."
echo

# CV files to build (in src directory)
cv_files=("src/index.qmd")
if [[ "${1:-}" == "--all" ]]; then
    cv_files+=("src/cv_academic.qmd" "src/cv_industry.qmd" "src/cv_grants.qmd")
fi

# IMPORTANT: Quarto resolves --output-dir relative to the input file location.
# Since our .qmd files live in src/, use an absolute dist/ path at the project root.
DIST_DIR="$PROJECT_ROOT/dist"

# Ensure custom CSS is available in dist/ so HTML can reference `custom-styles.css`
mkdir -p "$DIST_DIR"
cp -f "$PROJECT_ROOT/assets/custom-styles.css" "$DIST_DIR/custom-styles.css"

success_count=0
total_files=${#cv_files[@]}

# Build each CV version
for file in "${cv_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "📄 Building $file..."
        
        # Build HTML version
        echo "  → HTML version..."
        if quarto render "$file" --to html --output-dir "$DIST_DIR" --quiet; then
            echo "  ✅ HTML version completed"
            html_success=true
        else
            echo "  ❌ Error rendering HTML"
            html_success=false
        fi
        
        # Build PDF version (Typst for complete CV, LaTeX for variant extracts)
        pdf_format="pdf"
        if [[ "$file" == "src/index.qmd" ]]; then
            pdf_format="typst"
        fi
        echo "  → PDF version ($pdf_format)..."
        if quarto render "$file" --to "$pdf_format" --output-dir "$DIST_DIR" --quiet; then
            echo "  ✅ PDF version completed"
            pdf_success=true
        else
            echo "  ❌ Error rendering PDF"
            pdf_success=false
        fi
        
        # Count successful builds
        if [[ "$html_success" == true && "$pdf_success" == true ]]; then
            ((success_count++))
        fi
        
    else
        echo "❌ File not found: $file"
    fi
    echo
done

echo "🎉 Build process completed!"
echo "📊 Success rate: $success_count/$total_files files built successfully"
echo

if [[ $success_count -eq $total_files ]]; then
    echo "✨ CV website built successfully!"
    
    echo "📁 Generated files in dist/:"
    echo
    echo "HTML files:"
    for file in dist/*.html; do
        [[ -f "$file" ]] && echo " - $(basename "$file")"
    done
    
    echo
    echo "PDF files:"
    for file in dist/*.pdf; do
        [[ -f "$file" ]] && echo " - $(basename "$file")"
    done
    
    echo
    echo "🌐 Open dist/index.html in a browser to view."
    if [[ "${1:-}" != "--all" ]]; then
        echo "ℹ️  Tailored extracts skipped. Use --all to build cv_academic, cv_industry, and cv_grants."
    fi
else
    echo "⚠️  Some files failed to build. Check the errors above."
    exit 1
fi
