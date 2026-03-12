# run_claude Usage Guide

`run_claude` is a CLI tool for running Claude on Lean theorem proving tasks.

## Command Overview

```bash
python -m scripts.run_claude <command> [options]
```

> **Performance tip (recommended):** Before running on a Lean project, run a one-time build in that project directory:
>
> ```bash
> lake update
> lake exe cache get
> lake build
> ```
>
> If you skip this, the first MCP/LSP startup may be noticeably slower because it needs to compile/index dependencies.

> **MCP Setup (lean-lsp-mcp, required):** MCP configuration is **directory-scoped**. If you plan to run `run_claude` with `--cwd /path/to/project`, you must add the MCP **from that same directory** (or a parent directory):
>
> If you do **not** pass `--cwd`, the effective working directory is the **current directory** where you run `python -m scripts.run_claude ...` (i.e. `.`). In that case, you must run `claude mcp add ...` from the current directory (or a parent directory).
>
> ```bash
> cd /path/to/project
> claude mcp add lean-lsp -- /absolute/path/to/numina-lean-mcp.sh
> ```
>
> Verify:
>
> ```bash
> claude mcp list
> ```

Three commands are supported:
- `run` - Run a single task
- `batch` - Run batch tasks from a config file
- `from-folder` - Scan a folder for .lean files and run tasks

---

## Commands

### 1. `run` - Single Task

```bash
python -m scripts.run_claude run <target> [options]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `target` | str | (required) | Target path (file or folder) |
| `--task-type` | str | `auto` | Task type: `file` / `folder` / `auto` |
| `--prompt` | str | - | Direct prompt content |
| `--prompt-file` | str | - | Read prompt from file (mutually exclusive with `--prompt`) |
| `--cwd` | str | `.` | Claude working directory (defaults to current directory) |
| `--max-rounds` | int | `20` | Maximum rounds (continue count limit) |
| `--check` | bool | `True` | Whether to check lean files after completion |
| `--sleep` | float | `1.0` | Sleep between rounds (seconds) |
| `--result-dir` | str | - | Result output directory (JSON files) |
| `--mcp-log-name` | str | - | MCP log name |
| `--permission-mode` | str | `bypassPermissions` | Permission mode |
| `--json-output` | bool | `False` | Whether to use JSON output format |

> **Note:** For `--cwd` + lean-lsp-mcp setup, see **MCP Setup** in the Command Overview section above.

**Examples:**

```bash
# Single file
python -m scripts.run_claude run /path/to/file.lean --prompt-file prompt.txt

# Folder
python -m scripts.run_claude run /path/to/folder --task-type folder --prompt "..."
```

---

### 2. `batch` - Batch Tasks

```bash
python -m scripts.run_claude batch <config_file> [options]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config_file` | str | (required) | Config file path (YAML or JSON) |
| `--parallel` | bool | `False` | Whether to run in parallel |
| `--max-workers` | int | `1` | Maximum parallel workers |

**Examples:**

```bash
# Sequential execution
python -m scripts.run_claude batch config/config_minif2f.yaml

# Parallel execution
python -m scripts.run_claude batch config/config_minif2f.yaml --parallel --max-workers 4
```

---

### 3. `from-folder` - Generate Tasks from Folder

Scans all `.lean` files in a folder and generates one task per file.

```bash
python -m scripts.run_claude from-folder <folder> [options]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `folder` | str | (required) | Folder containing .lean files |
| `--prompt` | str | - | Direct prompt content |
| `--prompt-file` | str | - | Read prompt from file |
| `--cwd` | str | `.` | Claude working directory (defaults to current directory) |
| `--max-rounds` | int | `20` | Maximum rounds |
| `--check` | bool | `True` | Whether to check after completion |
| `--sleep` | float | `1.0` | Sleep between rounds |
| `--result-dir` | str | - | Result output directory |
| `--permission-mode` | str | `bypassPermissions` | Permission mode |
| `--parallel` | bool | `False` | Whether to run in parallel |
| `--max-workers` | int | `1` | Maximum parallel workers |

**Examples:**

```bash
# Sequential execution
python -m scripts.run_claude from-folder leanproblems/Minif2f --prompt-file prompts/prompt_complete_file.txt

# Parallel execution
python -m scripts.run_claude from-folder leanproblems/Minif2f --prompt-file prompts/prompt_complete_file.txt --parallel --max-workers 4
```

---

## Config File Format (config.yaml)

Config files support YAML and JSON formats, containing two main sections: `defaults` and `tasks`.

### Full Parameter List

#### Parameters for defaults / tasks

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `task_type` | str | - | Task type: `file` / `folder` |
| `target_path` | str | - | Target path (file or folder) |
| `prompt` | str | - | Direct prompt content |
| `prompt_file` | str | - | Read prompt from file |
| `cwd` | str | - | Claude working directory |
| `max_rounds` | int | `20` | Maximum rounds |
| `check_after_complete` | bool | `True` | Whether to check lean files after completion |
| `allow_sorry` | bool | `False` | Whether to allow sorry (default: not allowed) |
| `sleep_between_rounds` | float | `1.0` | Sleep between rounds (seconds) |
| `result_dir` | str | - | Result output directory |
| `mcp_log_dir` | str | - | MCP log directory |
| `mcp_log_name` | str | - | MCP log name |
| `permission_mode` | str | `bypassPermissions` | Permission mode |
| `output_format` | str | - | Output format (`json` / `None`) |
| `track_statements` | bool | `True` | Whether to track statement changes |
| `on_statement_change` | str | `warn` | Action on statement change: `error` / `warn` |
| `git_commit` | bool | `False` | Whether to create git commits after each round |

---

## defaults Inheritance

The `defaults` section in the config file defines default values for all tasks. Each task inherits from defaults and can override any parameter.

**Inheritance Rule:**

```
Final config = defaults + task (task takes priority)
```

**Example:**

```yaml
defaults:
  task_type: file
  prompt_file: prompts/prompt_complete_file.txt
  max_rounds: 2              # Default 2 rounds

tasks:
  - target_path: file1.lean
    # Inherits from defaults: task_type=file, prompt_file=..., max_rounds=2

  - target_path: file2.lean
    max_rounds: 5             # Override: max_rounds=5, others inherited from defaults
```

In this example:
- `file1.lean` has `max_rounds` of `2` (inherited from defaults)
- `file2.lean` has `max_rounds` of `5` (overrides defaults)

---

## MiniF2F Example

### Config File (`config/config_minif2f.yaml`)

```yaml
defaults:
  task_type: file
  prompt_file: prompts/prompt_complete_file.txt
  cwd: .
  check_after_complete: true
  permission_mode: bypassPermissions
  result_dir: results/minif2f
  mcp_log_dir: mcp_logs/minif2f
  max_rounds: 2

tasks:
  - target_path: leanproblems/Minif2f/algebra_sqineq_2atp2bpge2ab.lean
    mcp_log_name: algebra_sqineq_2atp2bpge2ab
  - target_path: leanproblems/Minif2f/amc12a_2021_p7.lean
    mcp_log_name: amc12a_2021_p7
  - target_path: leanproblems/Minif2f/mathd_algebra_478.lean
    mcp_log_name: mathd_algebra_478
  - target_path: leanproblems/Minif2f/mathd_numbertheory_284.lean
    mcp_log_name: mathd_numbertheory_284
  - target_path: leanproblems/Minif2f/imo_1964_p1.lean
    mcp_log_name: imo_1964_p1
    max_rounds: 5            # This task is harder, allow more rounds
```

### Running Commands

**Option 1: Using batch command (recommended for fine-grained control)**

```bash
python -m scripts.run_claude batch config/config_minif2f.yaml
```

**Option 2: Using from-folder command (simple batch run)**

```bash
python -m scripts.run_claude from-folder leanproblems/Minif2f \
  --prompt-file config/prompt_complete_file.txt \
  --max-rounds 5 \
  --result-dir results/minif2f
```

**Parallel execution:**

```bash
# batch parallel
python -m scripts.run_claude batch config/config_minif2f.yaml --parallel --max-workers 4

# from-folder parallel
python -m scripts.run_claude from-folder leanproblems/Minif2f \
  --prompt-file config/prompt_complete_file.txt \
  --parallel --max-workers 4
```

---

## Git Auto-Commit Feature

When `git_commit: true` is set in the config, the runner automatically creates a git commit after each round. This is useful for:
- Tracking progress and changes made by Claude
- Easy rollback if something goes wrong
- Debugging and reviewing what Claude did in each round

**How it works:**
- After each round, changes are committed to the git repository
- The commit is made in the target directory (for folder tasks) or the parent directory (for file tasks)
- Commit messages indicate the round number

**Example config with git_commit:**

```yaml
defaults:
  task_type: file
  prompt_file: config/prompt_complete_file.txt
  git_commit: true           # Enable auto-commit after each round
  max_rounds: 5

tasks:
  - target_path: leanproblems/Minif2f/imo_1964_p1.lean
```

**Note:** This feature is only available via config file (`batch` command), not via CLI flags for `run` or `from-folder` commands.

---

## Output

### Result Directory

If `result_dir` is set, a JSON file is generated for each task containing:
- Task ID, success status, end reason
- Rounds used, duration
- Line count changes per round
- MCP tool call statistics

### MCP Logs

If `mcp_log_dir` and `mcp_log_name` are set, MCP server logs are saved to the specified directory.

### Console Output

After execution, the console displays:
- Status for each task (SUCCESS / FAILED)
- End reason (COMPLETE / LIMIT / ERROR)
- Code line changes
- Batch summary statistics
