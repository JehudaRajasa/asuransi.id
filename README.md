# asuransi.id

Indonesian health insurance policy info aggregator. Normalizes RIPLAY (OJK-mandated product summaries) from major insurers into a single canonical schema so consumers can compare benefits, limits, and exclusions side-by-side — with BPJS Kesehatan as the public baseline.

## The problem

Indonesia has 100+ OJK-licensed insurers selling private health policies. Every product is required by POJK 23/2023 to publish a RIPLAY (Ringkasan Informasi Produk dan Layanan), but the documents are scattered across each insurer's own website, follow no shared layout, and use inconsistent benefit names and plan-tier naming. A consumer who wants to compare "kamar rawat inap" or annual limits across three insurers has to download three PDFs, decode three different tabel manfaat formats, and reconcile terminology by hand. The result is an information asymmetry that protects sellers, not buyers — and it disproportionately harms households who lack the time or literacy to do that legwork.

## The solution

asuransi.id collapses that work into a single canonical dataset. Each insurer has a deterministic scraper that downloads RIPLAY and brosur PDFs into `data/raw/`. A single ML-based parser (`docling`) extracts markdown and structured tables into `data/parsed/`. A normalizer (`scripts/normalize_policies.py`) maps every tabel manfaat row to a canonical manfaat category (~30 categories covering rawat inap, ICU, bedah, dental, kanker, dialisis, telehealth, and more), producing `data/normalized/policies.json`. BPJS Kesehatan is included as a hardcoded baseline so private policies can be compared against the public mandatory option. The pipeline is fully deterministic — no LLM extraction at the data layer — so every value in the canonical output is traceable back to a specific cell in a specific source PDF.

See [CONTEXT.md](CONTEXT.md) for the domain glossary, data sourcing scope, and the canonical schema.
