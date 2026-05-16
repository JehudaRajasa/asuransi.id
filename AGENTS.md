# AGENTS.md

Operational rules for AI coding agents working on this repo. Domain context lives in [CONTEXT.md](CONTEXT.md) — read it first.

## Stack

- Python 3.14
- `uv` for dependency management — install with `uv add <pkg>`, never pin versions by hand
- docling` parser.

## How to run

```bash
# 1. Scrape one insurer (downloads PDFs → data/raw/, parses → data/parsed/)
uv run python -u scripts/insurers/allianz/scrape.py

# 2. Normalize all parsed output into canonical policies.json
uv run python scripts/normalize_policies.py
```

The `-u` flag (unbuffered stdout) matters for scrapers — without it, long runs can lose final output if the process is interrupted.

## Data flow — three tiers, one direction

```
data/raw/        immutable, binary, gitignored
data/parsed/     docling output (md + tables.json), gitignored, regenerable
data/normalized/ canonical JSON, committed — this is the deliverable
```

Never edit `data/parsed/` by hand. Never edit `data/normalized/*.json` by hand — regenerate via `normalize_policies.py`.

## Hard rules

### Deterministic output only
The chatbot layer (Gemma 4) must ground on `data/normalized/policies.json`. **No raw-markdown fallback, no "best-effort" LLM extraction at runtime.** If a PDF cannot be parsed deterministically, the product goes into `data/normalized/parse_failures.json` for manual review — it does **not** ship.

### Amount convention: ×1000 multiplier
RIPLAY tables show values in '000 Rupiah ("ribuan rupiah") by Indonesian convention. `parse_amount()` in `normalize_policies.py` multiplies by 1000. Do not strip this without re-checking every source PDF.

### Cell that looks like prose is not an amount
`parse_amount()` rejects cells longer than 40 chars with 5+ spaces. This guards against descriptive text like "Mana yang lebih besar antara Kamar terendah dengan 1 tempat tidur…" being parsed as Rp 1.000. Keep the guard.

## Failure handling

Every parse failure (layer 1: docling cannot find tables; layer 2: tables exist but no canonical row maps) is recorded in `data/normalized/parse_failures.json` with `product_id`, `reason`, and source-PDF path. Failures are expected and do not block a release — they queue for manual review.
