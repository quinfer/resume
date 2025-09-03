# Prof. Barry Quinn - Resume Website

This repository contains multiple versions of Prof. Barry Quinn's CV, optimized for different purposes and audiences.

## 🌐 Website
The main resume website is generated from `index.qmd` and provides access to all CV versions.

**Live Website**: Open `index.html` in a browser after building.

## 📄 CV Versions

| File | Purpose | Target Audience | Length |
|------|---------|----------------|---------|
| `index.qmd` | **Resume Website** | General public, website visitors | Full |
| `cv_academic.qmd` | **Academic CV** | University positions, tenure applications | 4 pages |
| `cv_industry.qmd` | **Executive Summary** | Corporate roles, board positions | 2 pages |
| `cv_grants.qmd` | **Research Portfolio** | Grant applications, fellowships | 5 pages |

## 🔧 Building the CVs

### Quick Build (Choose your preferred method)

**Python (Recommended)**
```bash
python3 scripts/build_cvs.py
```

**Bash**
```bash
./scripts/build_all_cvs.sh
```

### Manual Build
```bash
# Build individual versions (from project root)
quarto render src/index.qmd --output-dir dist
quarto render src/cv_academic.qmd --output-dir dist
quarto render src/cv_industry.qmd --output-dir dist
quarto render src/cv_grants.qmd --output-dir dist
```

### Development Builds (Fast HTML-only for testing)

**Quick build all HTML versions**
```bash
python3 scripts/dev_build.py
```

**Build specific file for testing**
```bash
python3 scripts/dev_build.py index           # Builds src/index.qmd → dist/index.html
python3 scripts/dev_build.py cv_academic     # Builds src/cv_academic.qmd → dist/cv_academic.html
```

**Manual development builds**
```bash
# Build just HTML for quick preview
quarto render src/index.qmd --to html --output-dir dist

# Build specific version to PDF
quarto render src/cv_academic.qmd --to pdf --output-dir dist
```

## 📁 File Structure

```
resume/
├── src/                   # Source files
│   ├── index.qmd          # Main resume website
│   ├── cv_academic.qmd    # Academic version (4 pages)
│   ├── cv_industry.qmd    # Industry version (2 pages)
│   └── cv_grants.qmd      # Grant application version (5 pages)
├── scripts/               # Build automation
│   ├── build_cvs.py       # Main build script (Python)
│   ├── build_all_cvs.sh   # Build script (Bash)
│   ├── dev_build.py       # Development build script (HTML only)
│   └── deploy_local.py    # GitHub Pages local deployment
├── assets/                # Templates and styling
│   ├── custom-template.html
│   ├── custom-styles.css
│   └── img/
│       └── head_shot.png
├── data/                  # Data files
│   ├── bqpubs.bib         # Bibliography
│   └── Grant_income.csv   # Grant data
├── dist/                  # Generated outputs (HTML, PDF, assets)
│   ├── index.html         # Built website
│   ├── *.pdf              # All PDF versions
│   └── *_files/           # Quarto generated assets
├── .github/workflows/     # GitHub Actions
│   └── publish.yml        # Auto-deploy to GitHub Pages
├── archive/               # Old/unused files
├── index.html             # GitHub Pages file (copied by deploy script)
├── index_files/           # GitHub Pages assets (copied by deploy script)
├── README.md              # This file
└── .gitignore            # Git ignore patterns
```

## 🎯 Usage Guidelines

### For Academic Applications
Use `cv_academic.pdf` - emphasizes research excellence, publications, and academic leadership.

### For Industry Opportunities  
Use `cv_industry.pdf` - focuses on business impact, technology leadership, and practical applications.

### For Grant Applications
Use `cv_grants.pdf` - detailed research track record, funding history, and future directions.

### For General Reference
Share the website link or `index.pdf` for comprehensive overview.

## 🔄 Development Workflow

### For Quick Edits and Testing
1. Edit the relevant `.qmd` file(s) in `src/`
2. Run `python3 scripts/dev_build.py` for fast HTML preview
3. Open `dist/index.html` in browser to review changes
4. Iterate until satisfied

### For Final Production Build
1. Run `python3 scripts/build_cvs.py` to generate all HTML and PDF versions
2. Test all download links in the website
3. Commit and push changes

### Typical Development Session
```bash
# Edit files in your editor (src/*.qmd)
# Quick test build
python3 scripts/dev_build.py index

# Preview in browser
open dist/index.html

# Final build when ready
python3 scripts/build_cvs.py
```

## 🌐 GitHub Pages Deployment

### Automatic Deployment (Recommended)
The repository includes GitHub Actions that automatically build and deploy to GitHub Pages on every push to main branch. The workflow:
1. Builds all CV versions using our Python build system
2. Deploys the `dist/` folder contents to GitHub Pages
3. Your website is automatically updated

### Manual Local Deployment
For local GitHub Pages testing or manual deployment:

```bash
# Build and copy files to root directory for GitHub Pages
python3 scripts/deploy_local.py
```

This script:
- Builds all CV versions
- Copies `index.html` and `index_files/` to root directory
- Maintains clean `dist/` folder structure

## 📋 Dependencies

- **Quarto** (includes R runtime for executing R code blocks)
- **Python 3** (for build scripts)
- **LaTeX distribution** (for PDF generation)

**R Packages** (automatically managed by Quarto):
- `tidyverse`, `knitr`, `kableExtra` (loaded in .qmd files as needed)

## 📞 Contact

Prof. Barry Quinn  
Email: b.quinn1@ulster.ac.uk  
GitHub: [quinfer](https://github.com/quinfer)
