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

# 5. Setup lean-lsp-mcp
echo ""
echo "[5/5] Setting up lean-lsp-mcp..."
MCP_DIR="$HOME/lean-lsp-mcp"
if [ -d "$MCP_DIR" ]; then
    echo "lean-lsp-mcp already exists at $MCP_DIR, updating..."
    cd "$MCP_DIR"
    git pull
else
    git clone https://github.com/project-numina/lean-lsp-mcp "$MCP_DIR"
fi
chmod +x "$MCP_DIR/numina-lean-mcp.sh"

# Add MCP to Claude Code (from project directory)
cd "$PROJECT_DIR/$PROJECT_NAME" 2>/dev/null || cd "$PROJECT_NAME"
echo "Adding MCP server to Claude Code..."
claude mcp remove lean-lsp 2>/dev/null || true
claude mcp add lean-lsp -- "$MCP_DIR/numina-lean-mcp.sh"

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To verify installation:"
echo "  claude mcp list"
echo ""
echo "To start working:"
echo "  cd $PROJECT_DIR/$PROJECT_NAME"
echo "  claude"
echo ""
echo "For more details, see: tutorial/setup.md"
echo "========================================"
