# DESIGN_AGENT_BRIEF — asuransi.id

> **What this is.** A self-contained brief you can paste into an external design agent (Stitch, Claude Design at claude.ai, Figma AI, v0, Lovable, etc.) to generate screens for the asuransi.id MVP. It restates everything the agent needs without requiring access to this repo.
>
> **Source of truth.** This brief derives from `docs/PRD.md`, `PRODUCT.md` (register + principles), and `DESIGN.md` (visual system). If they disagree, the PRD wins; fix this brief.

---

## 1. Product in one paragraph

asuransi.id is a free, public-service Indonesian website that makes individual health-insurance products (asuransi kesehatan individu) comparable. Each Indonesian insurer publishes an OJK-mandated RIPLAY — a 30–100 page regulatory PDF — for every consumer product. Buyers cannot read those PDFs in practice. asuransi.id parses RIPLAYs into a single normalized dataset and presents them in three ways: (a) plain-Indonesian natural-language search powered by Gemma 4, (b) browse-by-insurer and browse-by-benefit grids, and (c) a side-by-side comparison table for 2–4 products. Every figure rendered in the UI is distilled from a specific cell in a specific source PDF, and every product detail page links to its source RIPLAY in one click. Built for the Kaggle Gemma 4 Good hackathon, Digital Equity & Inclusivity track, submission deadline 2026-05-18.

## 2. Target user

Indonesian adult on a low-end Android phone over metered mobile data, comparing 2–4 private health policies against the BPJS Kesehatan public baseline before talking to an agent. Does not speak regulatory Indonesian ("uang pertanggungan", "wilayah pertanggungan", "risiko sendiri"). Has never read a RIPLAY end-to-end. Low insurance literacy, high stakes.

## 3. Tone and personality

**Three words:** protective · grounded · plainspoken.

**Voice:** a knowledgeable friend reading the document with the user, not a salesperson. Calm guide standing beside the buyer.

**Emotional goal:** the user feels less alone in front of a 60-page PDF. Confidence comes from sources being open, not from hype.

**No:** urgency, upsell, aspirational lifestyle framing, mascots, "AI is thinking" spinners, hero metrics, gradients, dark-mode trust signals.

## 4. Visual system (summary — full tokens in `DESIGN.md`)

- **Atmosphere:** editorial, not commercial. Like the inside of a well-printed booklet — warm paper background, dark ink, careful typography, generous whitespace.
- **Page bg:** `#FAF8F4` (warm off-white). Never pure white.
- **Ink primary:** `#0E0E0E`.
- **Brand accent:** `#1E4A6E` (deep, slightly desaturated editorial blue). Used **sparingly** — ≤10% of any viewport. Never as full-bleed.
- **Success / warning / danger:** semantic green / warm yellow / muted red — kept separate from brand. Parse failures use **warm yellow**, not red — failure is an honesty signal.
- **Fonts:** Source Serif Pro (headlines) · Inter (UI/body) · JetBrains Mono (micro-labels, Rupiah numerals).
- **Numerals:** every Rupiah amount in mono with tabular-nums variant — comparison-table column alignment depends on this.
- **Radius:** `0 / 2 / 4 / pill`. No rounded cards beyond 4px.
- **Shadows:** only `sm` and `card`. No drop-shadow stacks, no glow, no gradients.
- **Motion:** 120 / 200 / 360 ms with `cubic-bezier(0.2, 0.7, 0.2, 1)`. Reduced-motion respected.

## 5. References (and anti-references)

**Borrow from:**
- **continue.dev** — quiet whitespace, serif headlines, ink-and-paper restraint. Primary reference.
- **babylonlabs.io** — typographic discipline only: mono micro-labels, oversized headline scale, sharp corners. **Reject** their saturated full-bleed colour blocks.

**Reject:**
- **pasal.id** (Indonesian aggregator) — saturated brand color, generic "Jelajahi Berdasarkan Jenis" icon+count grid. asuransi.id browse-grid card is center-aligned, no icon+count split, serif lead name, mono micro qualifier.
- **Generic insurance-marketing sites** (Allianz, Prudential, AXA brand sites) — lifestyle photography of smiling families, glossy CTAs, sales-funnel framing.
- **Crypto / fintech dark mode** — navy + gold, neon-on-black, "trust through severity".

## 6. Screens to design (MVP)

Ordered by priority. Get the comparison table right first — it's the heaviest layout and the product's reason to exist.

| # | Screen | Path | Why it matters |
|---|---|---|---|
| 1 | **Comparison table** | `/compare?products=...` | Side-by-side 2–4 products × N manfaat rows. Sticky left manfaat-label column, sticky header row, hairline dividers only, mono tabular numerals. Group rows by category (rawat inap, rawat jalan, kritis, dental/optical, lainnya). Empty cells render as `—` mono tertiary. |
| 2 | **Home (hero-search + browse)** | `/` | Editorial hero with full-width search input (lead font, bottom-border-only, no full box). Below: browse-by-insurer and browse-by-benefit grids. Non-dismissable disclaimer strip at viewport bottom. |
| 3 | **Single-product detail** | `/produk/[slug]` | Full manfaat table for one product, exclusions, waiting periods, claim procedure. Top of page: insurer badge + product name + plan-tier tag. Prominent `source-link` to RIPLAY and brosur PDFs ("Buka RIPLAY ↗" mono small). |
| 4 | **Gemma response block** | injected into `/` | Renders after natural-language query. Surface card max-width 720, padding 32. Serif-lead summary on top, stacked structured product cards below. **No streamed-token effect** — block appears once after retrieval. Each product card carries a `source-link` to its RIPLAY. |
| 5 | **Parse-failure state** | inline in detail / compare | Yellow `failure-banner` (bg `#FAEFD8`, ink primary, hairline warning border). Plain-Indonesian copy: "Tabel manfaat produk ini belum dapat kami baca otomatis. Buka dokumen sumber:" + `source-link`. **Yellow, not red.** |
| 6 | **Empty / no-match state** | inline in `/` and `/compare` | Calm copy ("Tidak ada produk cocok dengan kriteria. Coba kurangi filter…"), suggestion chips to broaden filters. No stack traces, no developer-speak. |

## 7. Layout grid

- Desktop: 12-column, 80px gutters, max content width 1180, reading max-width 720.
- Mobile: 16px gutters, 32px page padding.
- Breakpoints: 480 / 768 / 1024 / 1280.
- Comparison page: reserve 240px left rail for filter-chip stack on ≥ 1024; collapse to horizontal bar below.

## 8. Real data — use these names, not placeholders

The dataset is small and finite. Do not invent insurer or product names. Use these:

**Insurers:** Allianz · Prudential · Manulife · BPJS Kesehatan (public baseline).

**Sample product names:** Allianz Preferred Medical · MiUltimate Healthcare · PRUSehat · BPJS Kesehatan Kelas I / Kelas II / Kelas III.

**Sample benefit categories:** Rawat inap (kamar & menginap) · Rawat jalan · Penyakit kritis · Kanker · Dental & optical · Maternity · Lainnya.

**Sample numeric formats:** `Rp 500.000 / hari` · `Rp 1.500.000 / kunjungan` · `Rp 100.000.000 / tahun` · `Tak terbatas` · `—` (em dash for unknown/empty).

## 9. Hard rules (do not break)

- **Indonesian copy first.** Empty states, error messages, CTAs, disclaimers all written in plain Indonesian first. English is a fallback string for the locale toggle, not a co-equal.
- **No fabricated figures.** Use only the sample formats above. The product never invents numbers.
- **Every product detail page surfaces a `source-link` to RIPLAY (+ brosur if available).** Source PDF reachable in one click from the detail page.
- **No "AI is thinking" spinner, no streamed-token text effect.** The Gemma response renders as one structured block after retrieval.
- **Parse failures use warm yellow, not red.** They are an honesty signal, not a malfunction.
- **No lifestyle photography.** No happy families, no smiling patients, no aspirational imagery. The product is text and tables.
- **No mascot, no chatbot avatar.**
- **Default to light mode** for MVP. No dark mode.
- **Contrast ≥ 4.5:1** on body text, ≥ 3:1 on micro-labels.
- **Tabular-nums on every Rupiah amount.** Column alignment depends on it.
- **Non-dismissable disclaimer strip** at viewport bottom on home, sticky-on-scroll-stop on other pages: "Ini adalah alat bantu baca, bukan nasihat keuangan. Dokumen RIPLAY tetap mengikat."

## 10. Output format expected from the design agent

- Static high-fidelity mockups of the six screens above at desktop (1280) and mobile (375) widths.
- A component inventory matching the names in `DESIGN.md` § Component Stylings (`nav`, `hero-search`, `intent-pill`, `featured-card`, `filter-chip`, `comparison-table`, `source-link`, `failure-banner`, `gemma-response-block`, `disclaimer-strip`, `cta`).
- Export-friendly artefact (Figma file, PNG, or HTML/CSS) — implementer will translate into React + Tailwind under `web/components/`, one component per file, named exports only, no barrel files.
- **Do not** ship animations, micro-interactions, or onboarding tours. The product is a reading tool, not an experience.

## 11. Accessibility & inclusion (working standard for MVP)

- Contrast ≥ 4.5:1 body, ≥ 3:1 micro.
- Semantic table structure (`<table>`, `<th scope>`, row/column headers) so screen-reader users can navigate manfaat by row and column.
- Low-end Android usable — no horizontal scroll on home, modest JS payload, works on metered mobile data.
- Reduced motion respected.
- Indonesian primary. Empty states and errors in plain Indonesian first.
- **Formal WCAG audit is out of scope for MVP.** Targets above are the working standard.
