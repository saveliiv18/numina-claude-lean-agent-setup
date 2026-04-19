#!/bin/bash

# Lean + Claude Code Setup Script
# Usage: ./setup.sh [project_name]

set -e

PROJECT_NAME="${1:-leanproblems}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")/projects"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo "========================================"
echo "Lean + Claude Code Quick Setup"
echo "Project name: $PROJECT_NAME"
echo "========================================"

# 1. Install elan (Lean version manager)
echo ""
echo "[1/5] Installing elan (Lean version manager)..."
if command -v elan &> /dev/null; then
    echo "elan is already installed, skipping..."
else
    curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y
    source "$HOME/.elan/env"
fi

# 2. Create Lean project
echo ""
echo "[2/5] Creating Lean project: $PROJECT_NAME..."
if [ -d "$PROJECT_NAME" ]; then
    echo "Directory $PROJECT_NAME already exists, skipping project creation..."
else
    lake new "$PROJECT_NAME" math
fi
cd "$PROJECT_NAME"
echo "Updating dependencies and building (this may take a while)..."
lake update
lake exe cache get
lake build

# 3. Install Claude Code
echo ""
echo "[3/5] Installing Claude Code..."
if command -v claude &> /dev/null; then
    echo "Claude Code is already installed, skipping..."
else
    curl -fsSL https://claude.ai/install.sh | bash
fi

# 4. Install uv
echo ""
echo "[4/5] Installing uv..."
if command -v uv &> /dev/null; then
    echo "uv is already installed, skipping..."
else
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source "$HOME/.local/bin/env" 2>/dev/null || true
fi

# 5. Install local CLI skills
echo ""
echo "[5/5] Installing local CLI skills..."
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_SRC="$REPO_ROOT/skills"
PROJECT_PATH="$PROJECT_DIR/$PROJECT_NAME"
SKILLS_DST="$PROJECT_PATH/.claude/skills"

if [ ! -d "$SKILLS_SRC" ]; then
    echo "Error: skills source not found at $SKILLS_SRC"
    exit 1
fi

mkdir -p "$SKILLS_DST"
for skill in code-transform llm search sorrifier verification; do
    if [ -d "$SKILLS_SRC/$skill" ]; then
        echo "  installing $skill..."
        rm -rf "$SKILLS_DST/$skill"
        cp -r "$SKILLS_SRC/$skill" "$SKILLS_DST/"
    else
        echo "  warning: $skill not found in $SKILLS_SRC, skipping..."
    fi
done

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To verify installation:"
echo "  cd $PROJECT_PATH"
echo "  claude"
echo "  # then type /skills inside Claude Code"
echo ""
echo "To start working:"
echo "  cd $PROJECT_PATH"
echo "  claude"
echo ""
echo "For more details, see: tutorial/setup.md"
echo "========================================"
