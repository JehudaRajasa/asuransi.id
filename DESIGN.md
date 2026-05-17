---
name: asuransi.id
mood: embracing, reassuring, protective, editorial calm
inspiration:
  - continue.dev (primary — restrained editorial, generous whitespace, ink-and-paper)
  - babylonlabs.io (typographic discipline only — monospace micro-labels, oversized headline scale, sharp corners)
tokens:
  color:
    bg:
      page: "#FAF8F4"
      surface: "#FFFFFF"
      sunken: "#F3EFE8"
      ink_inverse: "#0E0E0E"
    ink:
      primary: "#0E0E0E"
      secondary: "#4A4A45"
      tertiary: "#8A8A82"
      inverse: "#FAF8F4"
    accent:
      brand: "#1E4A6E"
      brand_soft: "#E6ECF2"
      brand_ink: "#0B2A3D"
    semantic:
      info: "#3C5A7A"
      success: "#1E5F4A"
      warning: "#9A6B1A"
      warning_soft: "#FAEFD8"
      danger: "#8A2A2A"
    line:
      hairline: "#E2DED5"
      strong: "#0E0E0E"
  radius:
    none: 0
    sm: 2
    md: 4
    pill: 999
  spacing_base: 4
  font:
    serif: "Source Serif Pro, Charter, Georgia, serif"
    sans: "Inter, system-ui, sans-serif"
    mono: "JetBrains Mono, ui-monospace, monospace"
  type_scale:
    micro: 11
    small: 13
    body: 15
    lead: 18
    h3: 22
    h2: 32
    h1: 56
    display: 88
  weight:
    regular: 400
    medium: 500
    semibold: 600
  shadow:
    none: none
    sm: "0 1px 0 rgba(14,14,14,0.04)"
    card: "0 1px 2px rgba(14,14,14,0.06), 0 0 0 1px rgba(14,14,14,0.04)"
  motion:
    fast_ms: 120
    base_ms: 200
    slow_ms: 360
    easing: "cubic-bezier(0.2, 0.7, 0.2, 1)"
---

## Visual Theme & Atmosphere

asuransi.id is a public-service tool for people reading dense Indonesian insurance documents. The atmosphere is **editorial, not commercial**. The page should feel like the inside of a well-printed booklet: warm paper background, dark ink, careful typography, lots of breathing room. Nothing flashes, nothing pulses, nothing competes for attention.

The mood is **protective** — a calm guide standing beside the user as they decipher their options. No urgency, no upsell, no aspirational lifestyle imagery. The brand colour is a deep, slightly desaturated editorial blue — present in small doses (CTAs, key data, accent rules), never dominant. Success states keep a separate, canonical green so brand and success never read as the same signal.

Reference: Continue.dev's quiet whitespace and serif headlines. Borrow Babylon's typographic discipline (monospaced micro-labels, oversized headlines, sharp corners) but reject its saturated full-bleed colour blocks.

## Color Palette & Roles

| Role | Token | Hex | Notes |
|---|---|---|---|
| Page background | `bg.page` | `#FAF8F4` | warm off-white, never pure white |
| Surface (cards) | `bg.surface` | `#FFFFFF` | only where content needs to rise off the page |
| Sunken (skeleton, code) | `bg.sunken` | `#F3EFE8` | one step darker than page |
| Inverse surface (footer, disclaimer) | `ink.primary` | `#0E0E0E` | near-black |
| Primary ink | `ink.primary` | `#0E0E0E` | body & headlines |
| Secondary ink | `ink.secondary` | `#4A4A45` | metadata, captions |
| Tertiary ink | `ink.tertiary` | `#8A8A82` | placeholders, disabled |
| Brand accent | `accent.brand` | `#1E4A6E` | CTAs, key amounts, links |
| Brand soft | `accent.brand_soft` | `#E6ECF2` | active chip background |
| Warning soft | `semantic.warning_soft` | `#FAEFD8` | parse-failure banner background |
| Hairline | `line.hairline` | `#E2DED5` | table borders, dividers |

Rules:
- Brand blue is used **sparingly**. Default surface is warm paper. If more than ~10% of any viewport is brand-coloured, scale it back.
- No gradients. No drop shadows beyond `shadow.sm` / `shadow.card`.
- Failure banner uses warm yellow, **not red**. Parse failures are an honesty signal, not an error.

## Typography Rules

- Headlines: **serif** (Source Serif Pro). Sets editorial tone.
- Body & UI: **sans** (Inter). Inter for chips, buttons, table cells.
- Micro-labels, citations, numeric amounts in tables: **mono** (JetBrains Mono).

Scale (px): `micro 11 · small 13 · body 15 · lead 18 · h3 22 · h2 32 · h1 56 · display 88`.

Line heights: 1.5 for body and lead, 1.15 for h1/h2/display, 1.3 for h3.

Numeric amounts (Rp figures) always rendered in mono with tabular-nums variant — column alignment in comparison tables depends on this.

All-caps reserved for **micro-labels** only (e.g. `SOURCE · RIPLAY p.4`). Never for headlines.

## Component Stylings

### `nav`
- Height 64. Background `bg.page`. Bottom hairline.
- Logo wordmark left in serif weight 600. Locale toggle right in mono micro.
- No drop shadow on scroll.

### `hero-search`
- Full-width input, height 72, font lead, sans regular.
- Background `bg.surface`. Bottom border 2px solid `ink.primary` (no full box border).
- Placeholder ink `tertiary`. On focus, bottom border thickens to 3px brand.
- Submit hint: small mono label "⏎ tanya" inside input on right.

### `intent-pill`
- Pill, radius `pill`, padding `8 16`. Border 1px `line.hairline`. Background transparent.
- Hover: background `accent.brand_soft`, border colour shifts to `accent.brand`.
- Mono small.

### `featured-card`
- Surface `bg.surface`. Padding 24. Shadow `card`. Radius `md`.
- Insurer badge top-left. Plan tier tag top-right (mono micro).
- Headline manfaat block: serif h3 amount, mono micro label.
- CTA "Bandingkan →" bottom, brand text on transparent, no button chrome.

### `filter-chip`
- Pill. Inactive: 1px hairline border, ink primary text, transparent fill.
- Active: 1px brand border, brand_soft fill, brand_ink text.
- Always mono small.

### `comparison-table`
- No outer border. Hairline row dividers. No vertical lines.
- Header row sticky on scroll. Header text mono micro all-caps, ink secondary.
- Manfaat label column sticky left.
- Cells: mono body, tabular numerals, right-aligned for amounts, left-aligned for prose.
- Empty cell renders mono `—` ink tertiary.

### `manfaat-row` (expanded state)
- Disclosure indent 24. Background `bg.sunken`. Mono small for raw_label and raw_cell.
- Inline `citation-chip` at end of expanded block.

### `citation-chip`
- Inline. Mono micro. Background transparent, ink secondary, underline on hover.
- Format: `RIPLAY · p.{n}` or `RIPLAY · §{section}`.
- Click target ≥ 24px.

### `failure-banner`
- Background `semantic.warning_soft`. Ink primary. 1px border `semantic.warning`.
- Padding 16. Radius `sm`. Icon optional, prefer text-only.

### `gemma-response-block`
- Surface `bg.surface`, padding 32, max-width 720.
- Summary in serif lead. Beneath: stacked structured cards (not paragraphs).
- Every figure carries inline citation-chip. No streamed text effect on first paint.

### `disclaimer-strip`
- Inverse surface (`ink.primary` background, `ink.inverse` text).
- Mono small. Padding 16. Always visible at viewport bottom on home, sticky-on-scroll-stop on other pages.

### `cta` (generic button)
- Primary: filled brand, ink inverse, mono small uppercase, padding `12 20`, radius `sm`. No shadow.
- Secondary: text-only brand, no background, no border.
- Disabled: ink tertiary text on `bg.sunken`.

## Layout Principles

- 12-column grid, 80px gutters at desktop, 16px at mobile.
- Max content width 1180. Reading max-width 720.
- Vertical rhythm in multiples of `spacing_base` (4): 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96.
- Page padding: 96 top, 64 bottom on desktop. 32 / 32 on mobile.
- Breakpoints: 480 / 768 / 1024 / 1280.
- `/compare` reserves 240px left rail for filter-chip stack; collapses to a horizontal bar < 1024.

## Depth & Elevation

Three layers only:

| Layer | Use | Token |
|---|---|---|
| Flat | text on `bg.page`, dividers | `shadow.none` |
| Hairline | tables, banners, inputs | bottom border or `shadow.sm` |
| Card | featured-card, gemma-response-block | `shadow.card` |

No layered modals beyond a single overlay. No floating action buttons. Z-index used only for: nav (10), filter-bar sticky (20), modal (50), disclaimer-strip (5).

## Do's and Don'ts

**Do:**
- Use mono for every Rupiah amount and every citation.
- Treat empty cells as `—` (em dash) in mono tertiary ink.
- Show citation-chip inline with every amount the Gemma response surfaces.
- Render parse-failure products in a yellow `failure-banner` with a link to the original RIPLAY.
- Let the page breathe — when in doubt, add whitespace not content.

**Don't:**
- Use saturated colour blocks larger than ~10% of any viewport.
- Use red for parse failures (failure is honesty, not error).
- Add drop shadows beyond `shadow.card`.
- Animate the gemma-response-block as a streamed token effect — render the structured block once retrieval is done.
- Use rounded corners larger than `md` (4px). No pill cards.
- Render any Rp amount without a citation-chip.
- Show a chatbot avatar, mascot, or "AI is thinking" spinner.
- Use lifestyle photography of families or happy patients. The product is text and tables, not aspiration.

## Agent Prompt Guide

For Stitch:
- Default to light mode (`bg.page` warm off-white). Skip dark mode for MVP.
- Prefer Continue.dev's restraint when in doubt between two design options.
- Indonesian copy first; English fallback strings provided.
- All amounts are read from `data/normalized/policies.json` at build time; do not invent placeholder figures — use real product names (Allianz Preferred Medical, MiUltimate Healthcare, PRUSehat, BPJS Kesehatan Kelas I/II/III).
- Comparison-table is the heaviest layout — get it right first.
- For accessibility: minimum contrast 4.5:1 on body text, 3:1 on micro labels. Mono numerals must be tabular for column alignment.

For Claude / Cursor / Gemini CLI generating code from this design:
- Tailwind preferred. Map tokens to CSS variables, expose as a Tailwind theme extension.
- React + Vite or Next.js (App Router) acceptable. No CSS-in-JS runtime libraries.
- Components live under `web/components/`. No barrel files.
- One component per file, named export, no default export.
- Never read PDFs or `data/raw/` from the web app — only `data/normalized/policies.json` and `data/normalized/parse_failures.json` are public inputs.
