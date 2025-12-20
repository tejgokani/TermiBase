#!/bin/bash
# Helper script to submit TermiBase to Homebrew Core

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         Submitting TermiBase to Homebrew Core              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if homebrew-core is cloned
if [ ! -d "homebrew-core" ]; then
    echo "📦 Cloning homebrew-core..."
    git clone https://github.com/Homebrew/homebrew-core.git
    cd homebrew-core
else
    echo "📦 Using existing homebrew-core directory..."
    cd homebrew-core
    git pull origin master
fi

# Create branch
echo ""
echo "🌿 Creating branch 'termibase'..."
git checkout -b termibase 2>/dev/null || git checkout termibase

# Copy formula
echo ""
echo "📋 Copying formula..."
cp ../Formula/termibase-core.rb Formula/termibase.rb

# Show what will be committed
echo ""
echo "📝 Formula ready. Here's what will be committed:"
echo "─────────────────────────────────────────────────"
git diff --stat Formula/termibase.rb || echo "New file: Formula/termibase.rb"
echo ""

# Ask for confirmation
read -p "Continue with commit? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled."
    exit 1
fi

# Commit
echo ""
echo "💾 Committing..."
git add Formula/termibase.rb
git commit -m "termibase: add formula"

# Push
echo ""
echo "🚀 Pushing to GitHub..."
git push origin termibase

echo ""
echo "✅ Done! Now create a PR at:"
echo "   https://github.com/Homebrew/homebrew-core/compare/master...$(git config user.name):termibase"
echo ""
echo "Or visit: https://github.com/Homebrew/homebrew-core/pulls"

