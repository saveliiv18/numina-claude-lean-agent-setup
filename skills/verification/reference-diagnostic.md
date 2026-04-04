# diagnostic — Get Diagnostic Messages from Lean 4 Server

Query a remote Lean 4 verification server for diagnostic messages (errors, warnings, infos). Replaces `axle check` for compilation checking.

## CLI Invocation

```bash
python skills/cli/diagnostic.py CONTENT [OPTIONS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONTENT` | yes | — | Lean code string or path to a `.lean` file |
| `-u`, `--url` | no | `$LEAN4_SERVER_URL` or `http://localhost:6666` | Server URL (host:port) |
| `-t`, `--timeout` | no | 300 | Timeout in seconds |

## Output

Returns JSON with:
- `has_error` (bool) — whether any message has severity `"error"`
- `diagnostics` — formatted list of messages with position and severity
- `raw_messages` — raw message objects from the server

## Examples

```bash
# Check a .lean file
python skills/cli/diagnostic.py proof.lean

# Check inline code
python skills/cli/diagnostic.py "import Mathlib\n#check Nat.add_comm"

# Use a different server
python skills/cli/diagnostic.py proof.lean -u http://myserver:8080

# Custom timeout
python skills/cli/diagnostic.py proof.lean -t 600
```

## Notes

- Set `LEAN4_SERVER_URL` environment variable to configure the server address. Falls back to `http://localhost:6666`.
- The server must be running and accessible at the specified URL.
- Uses the `one_pass_verify_batch` endpoint with automatic retries (exponential backoff).
- Severity `"error"` in diagnostics means the code does not compile.
