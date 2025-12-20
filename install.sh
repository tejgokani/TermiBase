#!/bin/bash

# TermiBase Installation Script
# This script installs TermiBase on your system

set -e

echo "🚀 Installing TermiBase..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 3.8 or higher is required. Found: Python $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION found"

# Try to install using pip
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "❌ pip is not found. Trying python3 -m pip..."
    PIP_CMD="python3 -m pip"
fi

echo "📦 Installing TermiBase using $PIP_CMD..."
echo ""

# Install TermiBase
if $PIP_CMD install termibase 2>/dev/null; then
    echo ""
    echo "✅ TermiBase installed successfully!"
    echo ""
    echo "🎉 You can now use TermiBase:"
    echo "   termibase          # Launch interactive REPL"
    echo "   termibase init     # Initialize database"
    echo "   termibase --help   # Show all commands"
    echo ""
else
    echo ""
    echo "⚠️  Direct installation failed. Trying with --user flag..."
    if $PIP_CMD install --user termibase; then
        echo ""
        echo "✅ TermiBase installed successfully (user installation)!"
        echo ""
        echo "📝 Note: Make sure ~/.local/bin is in your PATH"
        echo ""
        echo "🎉 You can now use TermiBase:"
        echo "   termibase          # Launch interactive REPL"
        echo "   termibase init     # Initialize database"
        echo "   termibase --help   # Show all commands"
        echo ""
    else
        echo ""
        echo "❌ Installation failed. Please try manually:"
        echo "   $PIP_CMD install termibase"
        echo ""
        echo "Or use a virtual environment:"
        echo "   python3 -m venv venv"
        echo "   source venv/bin/activate"
        echo "   pip install termibase"
        exit 1
    fi
fi

