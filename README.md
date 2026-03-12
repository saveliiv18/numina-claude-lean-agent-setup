# Numina-Lean-Agent

<div align="center">
  <a href="https://arxiv.org/abs/2601.14027"><b>Paper</b></a> |
  <a href="https://leandex.projectnumina.ai"><b>Leandex</b></a> |
  <a href="https://demo.projectnumina.ai/"><b>Demo</b></a> |
  <a href="https://github.com/project-numina/Numina-Putnam2025"><b>Putnam 2025</b></a>
</div>

<br>

An agent built on Claude Code for formal theorem proving tasks. We used this system to prove all 12 problems from Putnam 2025, and completed a paper-level formalization of [Effective Brascamp-Lieb inequalities](https://arxiv.org/abs/2511.11091).

## System Overview

<p align="center">
  <a href="assets/Numina-LeanAgent-v3.png">
    <img src="assets/Numina-LeanAgent-v3.png" alt="Numina-Lean-Agent system overview" width="900" />
  </a>
</p>


## Quick Start

### 1. Environment Setup

Run the following command to set up Lean, Claude Code, and numina-lean-lsp-mcp:

```bash
git clone https://github.com/project-numina/numina-lean-agent
cd numina-lean-agent/tutorial
./setup.sh YOUR_PROJECT_NAME
```


If you prefer a manual installation or encounter any issues with the automatic script, please refer to the **[Tutorial: Setup Guide](tutorial/setup.md)** for detailed step-by-step instructions.

Next, set up the Python environment:
```bash
cd ..
uv python install
uv sync
```


Before running any scripts, activate the Python environment:
```bash
source .venv/bin/activate
```

### 2. Run Our Agent

After following the setup instructions, your project will be located at `projects/YOUR_PROJECT_NAME`. Place your Lean code here and start experimenting! 

#### Quick Examples

Before running the examples, you need to configure Claude Code. Choose one of the following options:

- **Option 1: Claude Account Login**  
  Run `Claude` in the terminal and follow the interactive login instructions.

- **Option 2: API Key Configuration**  
  Set the following environment variables with your API credentials:

```bash
export ANTHROPIC_BASE_URL=xxx      # Optional: custom API endpoint
export ANTHROPIC_AUTH_TOKEN=xxx    # Your API key
export ANTHROPIC_MODEL=xxx         # Model name (e.g., anthropic/claude-opus-4.5)
```


Once configured, you can use the following commands to get started:

```bash
# Run on a single file
python -m scripts.run_claude run leanproblems/Minif2f/mathd_algebra_478.lean \
  --prompt-file prompts/prompt_complete_file.txt \
  --max-rounds 5

# Run batch tasks from config
python -m scripts.run_claude batch config/config_minif2f.yaml

# Run all .lean files in a folder
python -m scripts.run_claude from-folder leanproblems/Minif2f \
  --prompt-file prompts/prompt_complete_file.txt \
  --max-rounds 5
```

#### Detailed Docs
For comprehensive instructions on using our agent, check out:

**[Tutorial: Usage Guide](tutorial/usage.md)**

## Related Projects

- [numina-lean-lsp-mcp](https://github.com/project-numina/lean-lsp-mcp) - MCP server for Lean LSP integration (based on [lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp))
- [lean4-skills](https://github.com/cameronfreer/lean4-skills) - Claude Code skills for Lean 4
- [Leandex](https://leandex.projectnumina.ai) - Semantic search for Lean codebases

## Citation
If you find the content of this project helpful, please cite our paper as follows:

```
@article{liu2026numina,
  title={Numina-Lean-Agent: An Open and General Agentic Reasoning System for Formal Mathematics},
  author={Junqi Liu and Zihao Zhou and Zekai Zhu and Marco Dos Santos and Weikun He and Jiawei Liu and Ran Wang and Yunzhou Xie and Junqiao Zhao and Qiufeng Wang and Lihong Zhi and Jia Li and Wenda Li},
  journal={arXiv preprint arXiv:2601.14027},
  year={2026}
}
```

## License

MIT License
