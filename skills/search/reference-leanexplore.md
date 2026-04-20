# leanexplore — Semantic Search

Searches Lean theorems/definitions using natural language, Lean terms, concept names, or identifiers. This is the recommended first-choice search tool.

> **Limit**: Do NOT run more than 5 leanexplore queries in parallel. Issue them one at a time or in small batches (≤5).

## CLI Invocation

```bash
python skills/cli/leanexplore.py QUERY [-n NUM_RESULTS]
```

Uses the `lean-explore` binary (`lean-explore search QUERY --limit N`) when `LEANEXPLORE_API_KEY` is set. If the binary is missing, the key is unset, or lean-explore returns an error, it automatically falls back to the Leandex HTTP API. Every invocation is logged to `cli.log`.

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `QUERY` | yes | — | Search query: natural language, Lean terms, concept names, identifiers |
| `-n, --num-results` | no | 5 | Maximum number of results to return |

## Examples

```bash
python skills/cli/leanexplore.py "continuous function"
python skills/cli/leanexplore.py "Cauchy Schwarz inequality"
python skills/cli/leanexplore.py "List.sum" -n 10
python skills/cli/leanexplore.py "{f : A → B} (hf : Injective f) : ∃ h, Bijective h"
```

## Notes

- Requires `LEANEXPLORE_API_KEY` env var for the `lean-explore` backend; automatically falls back to Leandex if unset or on error.
- Works best when you phrase the query as a mathematical concept, a Lean identifier, or a partial type signature.
- For proof-state-style queries, prefer `state-search` or `hammer-premise` instead.
- **Limit**: Do NOT run more than 5 leanexplore queries in parallel.
