# PRD — asuransi.id MVP comparison app

## Problem Statement

Indonesians shopping for individual health insurance (asuransi kesehatan individu) have no practical way to compare what private policies actually cover.

Each insurer publishes an OJK-mandated Ringkasan Informasi Produk dan Layanan (RIPLAY) for every consumer product. These documents are the canonical source of truth — they spell out room rates, surgery limits, critical-illness coverage, exclusions, waiting periods. But each RIPLAY is a 30–100 page PDF written in regulatory Indonesian, and the manfaat (benefit) tables are buried inside. To compare two products, a prospective buyer has to download two PDFs, scroll to the right pages, decode jargon they do not speak ("uang pertanggungan", "wilayah pertanggungan", "risiko sendiri"), and manually line up the numbers.

In practice, no one does this. Buyers rely on agents, marketing brochures, or word of mouth — none of which are accountable to the regulator-grade detail in the RIPLAY. The result is a market where the people most exposed to medical-cost shocks have the least visibility into what they're being sold. BPJS Kesehatan, the public option, suffers from the same opacity — most BPJS holders cannot articulate the difference between Kelas I, II, and III beyond the premium.

The gap is one of access, not of data. The data exists. It is just unreadable.

## Solution

A free, public-service website where ordinary Indonesians can:

- Ask a plain-Indonesian question about insurance and get a grounded answer drawn directly from the normalized RIPLAY tables.
- Browse private insurers (Allianz, Prudential, Manulife) and the BPJS Kesehatan baseline.
- Pick 2–4 products and see their manfaat side by side in a single table.
- Open the original RIPLAY (and brosur) from any product detail page — the source document is one click away.

The site never invents numbers. Every Rupiah figure rendered in the UI is distilled from a specific cell in a specific source PDF, and that source PDF is linked from the product's detail page. When a product's RIPLAY could not be parsed, the site says so plainly and points the user to the original document instead of guessing.

The natural-language layer is powered by Gemma 4. Gemma's role is interpretation and explanation, not arithmetic or coverage assertion. Gemma translates the user's question into a structured filter, and Gemma writes the prose summary that wraps the deterministically-rendered comparison cards. Gemma never produces a figure of its own.

## User Stories

### Discovery and browsing

1. As a first-time visitor, I want to see at a glance what kinds of insurance the site covers, so that I can quickly judge whether it is useful to me.
2. As a visitor who recognizes the major insurers, I want to browse by insurer (Allianz, Prudential, Manulife, BPJS Kesehatan), so that I can see which products each one offers.
3. As a visitor who knows what kind of coverage they need but not which insurer offers it, I want to browse by benefit category (rawat inap, rawat jalan, kanker, penyakit kritis, maternity, dental & optical), so that I can find relevant products without insurer-by-insurer hunting.
4. As a Muslim consumer, I want to filter products by jenis (konvensional vs syariah), so that I can shortlist products that match my financial preferences.
5. As a BPJS holder considering supplemental private coverage, I want to see BPJS Kesehatan presented alongside private policies, so that I can compare what I already have against what I am being offered.

### Natural-language search

6. As a user who does not know insurance terminology, I want to type a question in everyday Indonesian ("apakah ada asuransi yang menanggung kanker untuk anak saya?"), so that I can find relevant products without learning jargon.
7. As an English-comfortable user, I want to optionally view the interface in English, so that I can use the site even if Indonesian is not my strongest language.
8. As an inexperienced user, I want suggested example questions to click, so that I can see what kinds of queries the site can answer.

### Comparison

9. As a serious shortlist-maker, I want to add 2–4 products to a comparison set, so that I can see their manfaat side by side without flipping between tabs.
10. As a comparison-table user, I want manfaat grouped by category (rawat inap, rawat jalan, kritis, dental/optical, lainnya), so that I can navigate the table by what I care about.
11. As a comparison-table user, I want the manfaat label column to stay visible while I scroll horizontally through plans, so that I never lose track of which row I am reading.
12. As a comparison-table user, I want the column headers to stay visible while I scroll vertically through rows, so that I always know which plan a number belongs to.
13. As a comparison-table user, I want empty cells to render as "—" (em dash), not "0", so that I can distinguish "not covered" from "covered but unknown amount" without being misled.

### Verification and trust

14. As a user encountering a benefit cell that contains descriptive prose (e.g. "mana yang lebih besar antara…"), I want to see the prose verbatim instead of a fabricated number, so that I am not misled by a misparse.
15. As a user looking at a product whose RIPLAY could not be auto-parsed, I want a clear notice that the manfaat data is unverified, with a link to the original PDF, so that I know to consult the source directly.
16. As a regulator-aware user, I want to see OJK attribution and the date the data was last scraped, so that I know how current the information is.

### Single-product detail

17. As a user who clicked through from a comparison or search result, I want a single-product view that shows the full manfaat table, exclusions, waiting periods, and claim procedure for that one product, so that I can read everything about it in one place.
18. As a single-product viewer, I want a direct link to the original RIPLAY and brosur PDFs, so that I can read the source documents without leaving the site.
19. As a viewer of a parse-failed product, I want a yellow banner — not a red error — explaining that the table data is pending manual review, so that I understand the limitation without feeling that the site is broken.

### Accessibility and inclusion

20. As a user with limited insurance literacy, I want supportive empty states and reassuring copy ("Tidak ada produk cocok dengan kriteria. Coba kurangi filter…") instead of stack traces or developer-speak, so that errors do not chase me away.
21. As a screen-reader user, I want comparison tables to be semantically structured, so that I can navigate them by row and column with assistive technology.

### Honest framing

22. As a regulator or consumer-advocate observer, I want to see a non-dismissable disclaimer that this is not financial advice and the RIPLAY is the binding document, so that the project's role as an aid (not an authority) is unambiguous.
23. As an open-source observer, I want a footer link to the project's GitHub repository, so that I can verify how the data is produced.

### Edge cases

24. As a user whose query returns no matches, I want a calm empty state suggesting how to broaden filters, so that I am not left at a dead end.
25. As a user whose query fails due to a transient backend error, I want a quiet apology and a retry button, so that I can try again without losing my place.

## Implementation Decisions

### Architecture: deterministic core + LLM seam, behind a service boundary

The application splits cleanly into two layers, with the LLM strictly on the explanatory side of the boundary:

- **Deterministic core** — pure transforms over normalized policy data. No LLM involvement. Given the same inputs, always returns the same outputs.
- **LLM seam** — Gemma 4 maps natural-language queries to structured intent, and writes natural-language summaries of already-filtered results.

These layers run inside a **Python FastAPI service** (separate from the web frontend) so that the LLM and the deterministic transforms can be unit-tested with the existing Python tooling (uv, pytest) and so that the web layer can be rebuilt or replaced without touching the data pipeline.

### Modules

**Pure deterministic modules** (Python, no external dependencies beyond stdlib + pydantic):

- `policy_filter` — given a structured intent (insurer, manfaat categories, plan tier, jenis) and the full policies dataset, returns the subset of products matching the intent.
- `comparison_builder` — given a list of products, produces a comparison table shaped as (rows × columns) where rows are manfaat categories and columns are individual plans. Handles empty cells, multi-plan products, and category grouping.
- `figure_renderer` — given an amount, unit, and optional note, returns the display string for the UI ("Rp 500.000 / hari", "—", "Tak terbatas", an italic prose note for descriptive cells).

**LLM-mediated modules** (Python, Gemma 4 via constrained output):

- `intent_extractor` — given a natural-language query in Indonesian or English, returns a typed intent object. Output is constrained to a schema; the model cannot return free text.
- `response_composer` — given an intent and a list of already-filtered products, returns a short prose summary that wraps the comparison cards. The composer is forbidden from emitting any figure not present in its input — its job is interpretation and framing, not number generation.

**Service layer:**

- A FastAPI app exposes one endpoint, `POST /api/query`, that orchestrates `intent_extractor` → `policy_filter` → `comparison_builder` → `response_composer` and returns a single structured response containing the prose summary, the comparison table, and the source-PDF links per product.
- All other site content (home page browse grids, single-product pages, the full comparison page when accessed by direct URL with filters in the query string) is served statically from `data/normalized/*.json` with no LLM involvement.

**Web frontend** (separate codebase under `web/`, framework choice deferred to implementation):

- Reads `data/normalized/policies.json`, `data/normalized/insurers.json`, and `data/normalized/parse_failures.json` as static build inputs.
- Calls `POST /api/query` only when the user submits a natural-language query.
- Every product detail page links to its source RIPLAY and brosur PDFs.

### Hard rules carried over from AGENTS.md

These are product-level invariants, not implementation choices:

- **No LLM-generated figures.** The composer is given a list of filtered products and writes prose around them; it must not introduce a Rupiah amount that does not appear in the input.
- **Source PDFs reachable from the product detail page.** Every product detail page surfaces a direct link to its RIPLAY (and brosur where available). Users do not chase citations per cell — they open the source from one place.
- **Parse failures stay visible, not hidden.** Products in `parse_failures.json` get a yellow informational banner on their detail page, not a red error and not silent omission.
- **No streamed-token effect on the AI response.** The response renders as a single structured block after retrieval completes — the application is not a chatbot, it is an aid.

### Indonesian-first copy

All user-facing strings are Indonesian by default. English strings exist as fallbacks for the locale toggle, not as co-equals. Empty states, error messages, disclaimers, and CTA labels are written in Indonesian first and translated, not the other way around.

### Data freshness

The site shows the date `data/normalized/` was last regenerated, sourced from a single timestamp written by `normalize_policies.py`. There is no in-app refresh — the pipeline is offline and the site is a static-plus-API view over a snapshot.

## Testing Decisions

### What makes a good test

Tests verify external behavior, not implementation. For the four pure modules this means: given fixtures of input data, assert the shape and content of the output. No mocking the function under test; no asserting on intermediate state. If the implementation changes but the contract holds, the test should still pass.

### Modules to test

All three deterministic modules are covered by pytest:

- `policy_filter` — fixture intents (insurer-only, manfaat-only, multi-criteria, no-match) against fixture subsets of the real `policies.json`.
- `comparison_builder` — fixture product lists (single-plan, multi-plan, mixed insurer, with empty cells) → expected table shape.
- `figure_renderer` — table-driven tests covering every combination of `(amount_rp ∈ {None, value}, unit ∈ enum, note ∈ {None, prose})`.

The LLM-mediated modules (`intent_extractor`, `response_composer`) are not unit-tested in the MVP. Their behavior is non-deterministic; their correctness is constrained by the schema for intent extraction and by the "no figure not in input" rule for composition. Manual smoke testing covers them before submission.

### Prior art

No existing tests in the repo. Fixtures live alongside tests in a `tests/fixtures/` directory and are derived from real entries in `data/normalized/policies.json`.

## Out of Scope

- **User accounts** — no login, no saved comparisons, no personalization.
- **Premium calculator** — premium pricing is not normalized in the current dataset; no quote engine.
- **Hospital network search** — networks vary by product and are not yet structured data.
- **Transactional flows** — no quote requests, no claim filing, no agent contact.
- **Other insurance lines** — asuransi jiwa, travel insurance, kendaraan, properti are out. The scope is asuransi kesehatan individu plus BPJS Kesehatan as comparator.
- **Real-time data** — the site shows a snapshot; there is no continuous re-scrape.
- **Dark mode** — light mode only for MVP.
- **Native mobile app** — responsive web only.
- **A11y certification** — semantic structure and contrast targets are met; formal audit is out.
- **Authentication for the API** — `/api/query` is public, rate-limited at the edge but not user-keyed.

## Further Notes

- **Hackathon deadline:** 2026-05-18 (Kaggle Gemma 4 Good, Digital Equity & Inclusivity track). The MVP must be live and demonstrable in a recorded video by that date.
- **Dataset size:** 11 normalized policies across 3 priority insurers + 3 BPJS Kesehatan tiers, plus 4 known parse failures. Small enough that the entire dataset can ship in the static bundle. This might increase later.
- **Determinism is the differentiator.** Most consumer-facing "AI chatbots" for finance and insurance are demos that hallucinate numbers. Holding the line on "every figure traces to a source PDF, and the source PDF is one click away" is what makes this a public-service tool instead of a liability.
- **The downstream design artifacts (`DESIGN.md`, `DESIGN_AGENT_BRIEF.md`) must be regenerated to align with this PRD if there is drift.** The PRD is the source of truth; the design artifacts derive from it.
