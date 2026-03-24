---
name: numina-lean-agent
description: "Lean 4 theorem proving toolkit: search lemmas, verify proofs, repair/simplify code, and get LLM-assisted informal proofs"
---

# Numina Lean Agent — Tool Reference

All CLI scripts are in `skills/cli/` relative to project root. AXLE tools use the `axle` CLI directly.

---

## Search Tools

### leandex.py — Semantic search (recommended first choice)

Searches Lean theorems/definitions using natural language, Lean terms, concept names, or identifiers.

```bash
python skills/cli/leandex.py QUERY [-n NUM_RESULTS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `QUERY` | yes | — | Search query: natural language, Lean terms, concept names, identifiers |
| `-n, --num-results` | no | 5 | Maximum number of results to return |

Examples:
```bash
python skills/cli/leandex.py "Cauchy Schwarz inequality"
python skills/cli/leandex.py "List.sum" -n 10
python skills/cli/leandex.py "{f : A → B} (hf : Injective f) : ∃ h, Bijective h"
```

---

### loogle.py — Pattern matching search

Searches by constant name, name substring, subexpression pattern, type shape, or conclusion.

```bash
python skills/cli/loogle.py QUERY [-n NUM_RESULTS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `QUERY` | yes | — | Loogle query pattern |
| `-n, --num-results` | no | 8 | Maximum number of results |

Query patterns:
- By constant: `Real.sin`
- By name substring: `"differ"`
- By subexpression: `_ * (_ ^ _)`
- Non-linear: `Real.sqrt ?a * Real.sqrt ?a`
- By type shape: `(?a -> ?b) -> List ?a -> List ?b`
- By conclusion: `|- tsum _ = _ * tsum _`
- By conclusion with hypotheses: `|- _ < _ → tsum _ < tsum _`

---

### leanfinder.py — Mathlib semantic search

Searches Mathlib theorems/definitions semantically by mathematical concept or proof state.

```bash
python skills/cli/leanfinder.py QUERY [-n NUM_RESULTS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `QUERY` | yes | — | Mathematical concept, proof state, or statement definition |
| `-n, --num-results` | no | 5 | Maximum number of results |

Best for: natural language math statements, proof states, statement fragments. Multiple targeted queries beat one complex query.

---

### leansearch.py — Natural language + Lean term search

```bash
python skills/cli/leansearch.py QUERY [-n NUM_RESULTS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `QUERY` | yes | — | Natural language description or Lean terms |
| `-n, --num-results` | no | 5 | Maximum number of results |

---

### state_search.py — Search by proof goal

Searches theorems relevant to a given proof state/goal using premise-search.com.

```bash
python skills/cli/state_search.py GOAL [-n NUM_RESULTS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOAL` | yes | — | Proof state / goal text (paste the goal as-is) |
| `-n, --num-results` | no | 5 | Maximum number of results |

Environment variable: `LEAN_STATE_SEARCH_URL` overrides the default endpoint (https://premise-search.com).

---

### hammer_premise.py — Premise search by proof goal

Searches for relevant premises using the Lean Hammer premise retrieval service.

```bash
python skills/cli/hammer_premise.py GOAL [-n NUM_RESULTS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOAL` | yes | — | Proof state / goal text |
| `-n, --num-results` | no | 32 | Maximum number of premises to return |

Environment variable: `LEAN_HAMMER_URL` overrides the default endpoint (http://leanpremise.net).

---

## Verification Tools (AXLE)

All AXLE commands require `--environment` to specify the Lean version.

### axle check — Compile check

Check if Lean code compiles without errors.

```bash
axle check CONTENT --environment ENV [OPTIONS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONTENT` | yes | — | Lean file path or code string |
| `--environment` | yes | — | Lean environment, e.g. `lean-4.28.0` |
| `--mathlib-linter` | no | off | Enable Mathlib linter checks |
| `--ignore-imports` | no | off | Ignore imports, use environment defaults |
| `--timeout-seconds` | no | 120 | Max execution time (max 300) |

Returns: `okay` (bool), `lean_messages` (errors/warnings/infos), `failed_declarations`.

---

### axle verify-proof — Verify proof matches statement

Validates a candidate proof against a formal statement specification.

```bash
axle verify-proof FORMAL_STATEMENT CONTENT --environment ENV [OPTIONS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `FORMAL_STATEMENT` | yes | — | Sorried theorem to verify against |
| `CONTENT` | yes | — | Candidate proof code |
| `--environment` | yes | — | Lean environment, e.g. `lean-4.28.0` |
| `--permitted-sorries` | no | none | Comma-separated theorem names allowed to contain sorry |
| `--mathlib-linter` | no | off | Enable Mathlib linters |
| `--use-def-eq` | no | on | Use definitional equality for type comparison |
| `--ignore-imports` | no | off | Ignore import mismatches |
| `--timeout-seconds` | no | 120 | Max execution time (max 300) |

Returns: `okay` (bool), `failed_declarations`, `tool_messages` with verification details.

---

### axle disprove — Try to disprove a theorem

Attempts to prove the negation of theorems.

```bash
axle disprove CONTENT --environment ENV [OPTIONS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONTENT` | yes | — | Lean file path or code string |
| `--environment` | yes | — | Lean environment |
| `--names` | no | all | Comma-separated theorem names to try |
| `--indices` | no | all | Comma-separated theorem indices (0-based, supports negative) |
| `--terminal-tactics` | no | `grind` | Tactics to try for proving negation, comma-separated |
| `--ignore-imports` | no | off | Ignore imports |
| `--timeout-seconds` | no | 120 | Max execution time (max 300) |

Returns: `disproved_theorems` list, per-theorem `results`.

---

## Repair & Simplify Tools (AXLE)

### axle repair-proofs — Auto-fix broken proofs

```bash
axle repair-proofs CONTENT --environment ENV [OPTIONS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONTENT` | yes | — | Lean file path or code string |
| `--environment` | yes | — | Lean environment |
| `--names` | no | all | Comma-separated theorem names to repair |
| `--indices` | no | all | Comma-separated theorem indices (0-based, supports negative) |
| `--repairs` | no | all | Which repairs to apply: `remove_extraneous_tactics`, `apply_terminal_tactics`, `replace_unsafe_tactics` |
| `--terminal-tactics` | no | `grind` | Tactics for closing goals, comma-separated (e.g. `grind,aesop,simp,rfl`) |
| `--ignore-imports` | no | off | Ignore imports |
| `--timeout-seconds` | no | 120 | Max execution time (max 300) |

Available repairs:
- `remove_extraneous_tactics` — strips unreachable tactics after proof completion
- `apply_terminal_tactics` — replaces sorry with terminal tactics
- `replace_unsafe_tactics` — converts unsafe tactics (e.g. native_decide) to safer alternatives

---

### axle simplify-theorems — Simplify proofs

```bash
axle simplify-theorems CONTENT --environment ENV [OPTIONS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONTENT` | yes | — | Lean file path or code string |
| `--environment` | yes | — | Lean environment |
| `--names` | no | all | Comma-separated theorem names |
| `--indices` | no | all | Comma-separated theorem indices |
| `--simplifications` | no | all | Which simplifications: `remove_unused_tactics`, `remove_unused_haves`, `rename_unused_vars` |
| `--ignore-imports` | no | off | Ignore imports |
| `--timeout-seconds` | no | 120 | Max execution time (max 300) |

---

## Code Transform Tools (AXLE)

### axle sorry2lemma — Extract sorry into standalone lemmas

```bash
axle sorry2lemma CONTENT --environment ENV [OPTIONS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONTENT` | yes | — | Lean file path or code string |
| `--environment` | yes | — | Lean environment |
| `--names` | no | all | Comma-separated theorem names |
| `--indices` | no | all | Comma-separated theorem indices |
| `--no-extract-sorries` | no | on | Disable lifting sorries into standalone lemmas |
| `--no-extract-errors` | no | on | Disable lifting errors into standalone lemmas |
| `--no-include-whole-context` | no | on | Don't include all context variables when extracting |
| `--reconstruct-callsite` | no | off | Replace sorry with extracted lemma call |
| `--verbosity` | no | 0 | Pretty-printer verbosity (0=default, 1=robust, 2=extra robust) |
| `--ignore-imports` | no | off | Ignore imports |
| `--timeout-seconds` | no | 120 | Max execution time (max 300) |

---

### axle extract-theorems — Split file into individual theorems

```bash
axle extract-theorems CONTENT --environment ENV [OPTIONS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONTENT` | yes | — | Lean file path or code string |
| `--environment` | yes | — | Lean environment |
| `--ignore-imports` | no | off | Ignore imports |
| `--timeout-seconds` | no | 120 | Max execution time (max 300) |

Returns per-theorem: declaration, signature, type, type_hash, is_sorry, dependencies, tactic_counts, proof_length.

---

## LLM Tools

### informal_prover.py — Solve math problems with LLM + verification

Generates a step-by-step solution, then auto-verifies and refines it in a loop.

```bash
python skills/cli/informal_prover.py PROBLEM [OPTIONS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PROBLEM` | yes | — | Math problem text. Use `-` to read from stdin |
| `--backend` | no | `gemini` | LLM backend: `gemini` or `gpt` |
| `--model` | no | auto | Model name. Default: `gemini-3-pro-preview` (gemini) or `gpt-5.2-pro` (gpt) |
| `--temperature` | no | 0.7 | Generation temperature |
| `--max-attempts` | no | 10 | Max generate+verify+refine cycles |
| `--log-dir` | no | none | Directory to save results as JSONL |

Output: JSON with `solution`, `verification` ("correct" or feedback), `attempts`.

Examples:
```bash
python skills/cli/informal_prover.py "Prove that sqrt(2) is irrational" --backend gemini
python skills/cli/informal_prover.py "Prove the AM-GM inequality" --backend gpt --max-attempts 5
echo "Prove Fermat's little theorem" | python skills/cli/informal_prover.py - --backend gemini --model gemini-2.5-pro
```

---

### code_golf.py — Simplify Lean proof via Gemini

```bash
python skills/cli/code_golf.py LEAN_CODE [OPTIONS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `LEAN_CODE` | yes | — | Lean code to simplify. Use `-` to read from stdin |
| `--model` | no | `gemini-3-pro-preview` | Gemini model name |
| `--temperature` | no | 0.7 | Generation temperature |

Examples:
```bash
python skills/cli/code_golf.py "theorem foo : 1 + 1 = 2 := by norm_num"
cat proof.lean | python skills/cli/code_golf.py -
python skills/cli/code_golf.py - --model gemini-2.5-pro < proof.lean
```

---

### discussion_partner.py — Discuss with Gemini/GPT

Free-form discussion about proof strategies, Lean code, math problems, or anything else.

```bash
python skills/cli/discussion_partner.py QUESTION [OPTIONS]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `QUESTION` | yes | — | Question or context to discuss. Use `-` to read from stdin |
| `--backend` | no | `gemini` | LLM backend: `gemini` or `gpt` |
| `--model` | no | auto | Model name. Default: `gemini-3-pro-preview` (gemini) or `gpt-5.2-pro` (gpt) |

Examples:
```bash
python skills/cli/discussion_partner.py "How should I approach this induction proof?" --backend gemini
python skills/cli/discussion_partner.py "What tactic should I use for this goal: ⊢ n + 0 = n" --backend gpt
cat stuck_proof.lean | python skills/cli/discussion_partner.py - --backend gemini
```

---

## Workflow Guide

### Typical proving cycle:
1. **Understand the goal** — Read the .lean file, understand what needs to be proved
2. **Search** — Use leandex/loogle/leanfinder to find relevant lemmas
3. **Get informal proof** — Use informal_prover if the math is non-trivial
4. **Write/edit code** — Edit the .lean file with your proof attempt
5. **Check** — Run `axle check` to see if it compiles
6. **Repair** — If close but broken, try `axle repair-proofs`
7. **Simplify** — Once it works, run `axle simplify-theorems` to clean up
8. **Verify** — Run `axle verify-proof` to confirm the proof matches the statement


### Environment variables:
- `GEMINI_API_KEY` — required for: informal_prover (gemini backend), code_golf, discussion_partner (gemini backend)
- `OPENAI_API_KEY` — required for: informal_prover (gpt backend), discussion_partner (gpt backend)
- `AXLE_API_KEY` — required for: all axle commands
