#!/bin/bash

# setup_env.sh - macOS Environment Setup for LLManim_Agent
# Based on dependencies identified in Manimator's Dockerfile

echo "🚀 Starting Manim Environment Setup for macOS..."

# 1. Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Please install Homebrew first: https://brew.sh/"
    exit 1
fi

echo "✅ Homebrew found."

# 2. Update Homebrew
echo "📦 Updating Homebrew..."
brew update

# 3. Install System Dependencies (FFmpeg, Cairo, Pango)
echo "📦 Installing core dependencies (ffmpeg, cairo, pango)..."
brew install ffmpeg cairo pango pkg-config scipy

# 4. LaTeX Setup
if ! command -v pdflatex &> /dev/null; then
    echo "⚠️  pdflatex not found."
    echo "📦 We recommend installing BasicTeX (lighter) or MacTeX (full)."
    echo "Proto-typing: 'brew install --cask basictex'"
    
    read -p "Do you want to install BasicTeX via Homebrew Cask? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        brew install --cask basictex
        
        # Add texbin to PATH (common issue after install)
        export PATH="/Library/TeX/texbin:$PATH"
        
        # Update tlmgr and install common packages needed for Manim
        echo "📦 Installing common LaTeX packages..."
        sudo tlmgr update --self
        sudo tlmgr install standalone preview dvisvgm doubling
        sudo tlmgr install amsmath babel-english cm-super
    else
        echo "⚠️  Skipping LaTeX installation. Manim need LaTeX for math rendering."
    fi
else
    echo "✅ pdflatex found."
fi

# 5. Python Environment (Optional hint)
echo "python3 -m pip install -r requirements.txt"

echo "🎉 Environment setup check complete!"
echo "If you installed BasicTeX, you might need to restart your terminal or run: export PATH=\"/Library/TeX/texbin:\$PATH\""
