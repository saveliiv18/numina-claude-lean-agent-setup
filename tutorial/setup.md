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

#### Troubleshooting

**Issue: `lake` command not found or fails**

This usually means `~/.elan/env` is not sourced in your PATH. Add the following to your shell configuration file (`~/.bashrc` or `~/.zshrc`):

```bash
source ~/.elan/env
```

Then restart your terminal or run:
```bash
source ~/.elan/env
```

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


### 5. Install CLI skills

Copy the following folders under `numina-lean-agent/skills` into your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills #(If this folder not exist)
cp -r /path/to/numina-lean-agent/skills/code-transform .claude/skills/
cp -r /path/to/numina-lean-agent/skills/llm           .claude/skills/
cp -r /path/to/numina-lean-agent/skills/search        .claude/skills/
cp -r /path/to/numina-lean-agent/skills/sorrifier     .claude/skills/
cp -r /path/to/numina-lean-agent/skills/verification  .claude/skills/
```

After copying, your layout should look like:

```
.claude/skills/
    |- code-transform/
    |- llm/
    |- search/
    |- sorrifier/
    |- verification/
```

To verify, open Claude Code in your project directory by running `claude`, then type `/skills`. If you see the following, the installation is successful:

```
Skills
5 skills · t to sort, Esc to close

❯ ✔ on   code-transform · project · ~24 tok
  ✔ on   llm            · project · ~24 tok
  ✔ on   search         · project · ~20 tok
  ✔ on   sorrifier      · project · ~41 tok
  ✔ on   verification   · project · ~22 tok
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

1. Type `/skills` to check slills installation.
2. Try asking Claude to analyze or write Lean code.

---

## Related Links

- [Lean Official Installation Guide](https://lean-lang.org/install/manual/)
- [elan GitHub](https://github.com/leanprover/elan)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/setup)
- [lean4-skills GitHub](https://github.com/cameronfreer/lean4-skills)
