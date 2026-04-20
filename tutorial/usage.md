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
> If you skip this, the first invocation of the CLI skills (e.g. `lean_check.py`) will be noticeably slower because Lean still needs to compile/index dependencies on first use.

> **Skills Setup (required):** Skills are loaded from the `.claude/skills/` directory in the **repo root** (not inside your Lean project). `tutorial/setup.sh` creates symlinks there automatically; if you set up manually, see `tutorial/setup.md` section 5. Because they are symlinks, skills stay up-to-date after every `git pull` with no reinstallation needed.
>
> Verify by running `claude` from the repo root and typing `/skills`; you should see all five skills listed.

> **Target must live inside a Lean project (required):** The target `.lean` file or folder you pass to `run` / `batch` / `from-folder` must be located **inside a Lean project** — i.e. some ancestor directory contains `lean-toolchain` and `lakefile.{lean,toml}`. The CLI skills (e.g. `lean_check.py`) walk up from the target to find the project root and invoke `lake env lean` there. A standalone `.lean` file outside any project will fail to compile.

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
| `--prompt` | str | - | Direct prompt content (**exactly one of `--prompt` / `--prompt-file` is required**) |
| `--prompt-file` | str | - | Read prompt from file (**exactly one of `--prompt` / `--prompt-file` is required**) |
| `--cwd` | str | `.` | Claude working directory (defaults to current directory) |
| `--max-rounds` | int | `20` | Maximum rounds (continue count limit) |
| `--check` | bool | `True` | Whether to check lean files after completion |
| `--sleep` | float | `1.0` | Sleep between rounds (seconds) |
| `--result-dir` | str | - | Result output directory (per-task JSON + isolated `cli.log` + `cli_stats.json`) |
| `--permission-mode` | str | `bypassPermissions` | Permission mode |
| `--json-output` | bool | `False` | Whether to use JSON output format |

> **Note:** For `--cwd` + skills setup, see **Skills Setup** in the Command Overview section above.

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
| `--prompt` | str | - | Direct prompt content (**exactly one of `--prompt` / `--prompt-file` is required**) |
| `--prompt-file` | str | - | Read prompt from file (**exactly one of `--prompt` / `--prompt-file` is required**) |
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
| `result_dir` | str | - | Result output directory (per-task JSON + isolated `cli.log` + `cli_stats.json`) |
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
  max_rounds: 2

tasks:
  - target_path: leanproblems/Minif2f/algebra_sqineq_2atp2bpge2ab.lean
  - target_path: leanproblems/Minif2f/amc12a_2021_p7.lean
  - target_path: leanproblems/Minif2f/mathd_algebra_478.lean
  - target_path: leanproblems/Minif2f/mathd_numbertheory_284.lean
  - target_path: leanproblems/Minif2f/imo_1964_p1.lean
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

If `result_dir` is set, each task writes under `<result_dir>/<task_id>/`:
- `result.json` — task ID, success, end reason, rounds used, duration, token/cost usage, line counts per round
- `round_<N>.json` / `claude_raw/round_<N>.jsonl` — per-round diagnostics and the raw Claude NDJSON stream
- `cli.log` — this task's own CLI skill log (see below)
- `cli_stats.json` — per-tool call counts (`called` / `ok` / `fail`) derived from `cli.log`

### CLI Skill Log (`$CLI_LOG_PATH`)

Each script under `skills/cli/` (`lean_check.py`, `leanexplore.py`, `loogle.py`, `discussion_partner.py`, `informal_prover.py`, …) logs every invocation via Python `logging.FileHandler`. The log path is driven by the `CLI_LOG_PATH` environment variable:

- **When the runner is used with `--result-dir`**: the runner sets `CLI_LOG_PATH=<result_dir>/<task_id>/cli.log` in the Claude subprocess env, so each task gets an **isolated log file** — safe for parallel runs.
- **When `CLI_LOG_PATH` is unset** (e.g. you call a skill script directly from the shell): scripts fall back to the shared default `<repo_root>/cli.log`.

```bash
# Follow the current task's log (replace with your task_id)
tail -f results/<run_id>/<task_id>/cli.log

# Standalone use — shared default log at repo root
tail -f cli.log
grep leanexplore cli.log
```

To override the log path manually (e.g., in a script or test):

```bash
export CLI_LOG_PATH=/tmp/my_cli.log
python skills/cli/leanexplore.py "..."
```

### Console Output

After execution, the console displays:
- Status for each task (SUCCESS / FAILED)
- End reason (COMPLETE / LIMIT / ERROR)
- Code line changes
- Batch summary statistics
