# Lean + Claude Code Environment Setup Guide

This guide helps you quickly set up a Lean + Claude Code development environment.

---

## Quick Start

```bash
# Install elan
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh
# Refresh your shell environment
source ~/.elan/env

# Create Lean project
lake new myproject math && cd myproject
lake update && lake exe cache get && lake build

# Install Claude Code
curl -fsSL https://claude.ai/install.sh | bash

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart your terminal (or `source ~/.bashrc` / `source ~/.zshrc`, depending on your shell)

# Setup lean-lsp-mcp
git clone https://github.com/project-numina/lean-lsp-mcp ~/lean-lsp-mcp
chmod +x ~/lean-lsp-mcp/numina-lean-mcp.sh

# Add MCP (run from your project directory!)
cd myproject
claude mcp add lean-lsp -- ~/lean-lsp-mcp/numina-lean-mcp.sh

# Verify
claude mcp list
```

---

## Detailed Setup Guide

### 1. Prerequisites

Ensure `git` and `curl` are installed:

```bash
git --version
curl --version
```

If not installed, use your system's package manager to install them first.

### 2. Install Lean (elan)

You can find the official installation guide [here](https://lean-lang.org/lean4/doc/setup.html), or follow the steps below.

Run the following command to install elan, the Lean version manager:

```bash
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh
```

After installation, refresh your environment:

```bash
source ~/.elan/env  # loads Lean into your PATH
```

Or restart your terminal.

> **Verify:** Run `lean --version` to confirm installation.

### 3. Create a Lean Project

```bash
lake new myproject math
cd myproject
lake update
lake exe cache get
lake build
```

> **Note:** The `math` template automatically configures Mathlib dependencies. `lake exe cache get` downloads pre-compiled caches to speed up the first build.

### 4. Install Claude Code

**Option 1: Using npm**

```bash
npm install -g @anthropic-ai/claude-code
```

**Option 2: Using install script (no npm required)**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

> **More info:** [Claude Code Official Documentation](https://docs.claude.com/en/docs/claude-code/setup)

### 5. Install lean-lsp-mcp

#### 5.1 Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal or run `source ~/.bashrc` after installation.
If you're using zsh, run `source ~/.zshrc` instead.

#### 5.2 Clone and Configure lean-lsp-mcp

```bash
# Clone the repository
git clone https://github.com/project-numina/lean-lsp-mcp
cd lean-lsp-mcp

# Add execute permission
chmod +x numina-lean-mcp.sh
```

#### 5.3 Add to Claude Code

> **IMPORTANT: MCP configuration is directory-specific.** The MCP server is registered for the directory where you run the `claude mcp add` command. You must run this command from your Lean project directory (or a parent directory) for the MCP to be available when working on that project.

**Replace the path with your actual absolute path:**

```bash
# Navigate to your Lean project first
cd /path/to/myproject

# Then add the MCP server
claude mcp add lean-lsp -- /absolute/path/to/lean-lsp-mcp/numina-lean-mcp.sh
```

Example:
```bash
cd ~/myproject
claude mcp add lean-lsp -- /home/username/lean-lsp-mcp/numina-lean-mcp.sh
```

> **Tip:** To make the MCP available globally (for all projects), run the command from your home directory (`~`) or use the `--scope user` flag.

#### 5.4 Verify MCP Connection

```bash
claude mcp list
```

Expected output:
```text
Checking MCP server health...
lean-lsp: /home/username/lean-lsp-mcp/numina-lean-mcp.sh  - ✓ Connected
```

#### Troubleshooting

**Issue: Shows `uvx lean-lsp-mcp` instead of custom path**

This means the official version was installed instead of the project version. Remove and re-add:

```bash
claude mcp remove lean-lsp
claude mcp add lean-lsp -- /absolute/path/to/lean-lsp-mcp/numina-lean-mcp.sh
```

**Issue: `lake` command not found or fails**

This usually means `~/.elan/env` is not sourced in your PATH. Add the following to your shell configuration file (`~/.bashrc` or `~/.zshrc`):

```bash
source ~/.elan/env
```

Then restart your terminal or run:
```bash
source ~/.elan/env
```

**Issue: Connection failed (Failed to connect)**

1. Verify the path is correct
2. Ensure the file has execute permission: `chmod +x numina-lean-mcp.sh`
3. Check the log file: `cat /path/to/lean-lsp-mcp/mcp_lean_lsp.log`
4. Confirm uv is properly installed: `uv --version`

**Issue: MCP not showing when running Claude Code**

The MCP configuration is tied to the directory where it was added. Make sure you:
- Added the MCP from your project directory (or a parent directory)
- Are running `claude` from the same project directory

To check where your MCP is configured:
```bash
claude mcp list
```


### 6. Install lean4-skills

Run the following commands inside Claude Code:

```bash
/plugin marketplace add cameronfreer/lean4-skills
/plugin install lean4-theorem-proving    # Core skill
/plugin install lean4-memories           # Optional: memory feature
```

> **More info:** [lean4-skills GitHub](https://github.com/cameronfreer/lean4-skills)

### 7. Verify Installation

Navigate to your Lean project directory and start Claude Code:

```bash
cd myproject
claude
```

Test inside Claude Code:

1. Type `/mcp` to check MCP connection status
2. Try asking Claude to analyze or write Lean code

---

## Related Links

- [Lean Official Installation Guide](https://lean-lang.org/install/manual/)
- [elan GitHub](https://github.com/leanprover/elan)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/setup)
- [lean-lsp-mcp GitHub](https://github.com/project-numina/lean-lsp-mcp)
- [lean4-skills GitHub](https://github.com/cameronfreer/lean4-skills)
