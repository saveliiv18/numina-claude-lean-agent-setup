---
name: verification
description: "Verification tools for compiling, validating, and disproving Lean theorems"
---

# Verification Tools

Tools for verifying Lean code correctness.

- **diagnostic** uses `python skills/cli/diagnostic.py`
- **axle** tools use `python skills/cli/axle.py <subcommand>`

## Available Tools

| Tool | CLI | Purpose | When to use |
|------|-----|---------|-------------|
| **diagnostic** | `python skills/cli/diagnostic.py` | Get diagnostic messages (errors, warnings, infos) from a Lean 4 server | First step to validate any proof attempt |
| **axle verify-proof** | `python skills/cli/axle.py verify-proof` | Validate a proof matches a formal statement | When you need to confirm a proof proves exactly the right theorem |
| **axle disprove** | `python skills/cli/axle.py disprove` | Attempt to disprove theorems by proving negation | Before investing effort in a proof, check if the conjecture is false |

For full parameters and examples, read the corresponding `reference-*.md` file in this directory.
