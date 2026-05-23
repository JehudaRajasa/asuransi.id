# Product

## Register

product

## Users

Indonesian adults shopping for individual health insurance (asuransi kesehatan individu) — typically before talking to an agent or finalizing a purchase. Most have never read a RIPLAY end-to-end and do not speak the regulatory vocabulary ("uang pertanggungan", "wilayah pertanggungan", "risiko sendiri"). Many are on low-end Android phones over metered mobile data. Some hold BPJS Kesehatan and are weighing whether to add private coverage on top.

Their job: understand what private products actually cover so they are not sold the wrong policy. They are comparing 2–4 products at a time across major insurers (Allianz, Prudential, Manulife) against the BPJS Kesehatan public baseline.

## Product Purpose

asuransi.id makes Indonesian individual health insurance products comparable. It collapses the OJK-mandated RIPLAY PDFs — scattered across each insurer's site, in inconsistent layouts and inconsistent benefit naming — into a single canonical dataset. Users can:

- Ask a plain-Indonesian question and get a grounded answer drawn from the normalized RIPLAY tables.
- Browse by insurer or by benefit category (rawat inap, kanker, dental, etc.).
- Pick 2–4 products and read their manfaat side by side in one table.
- Open the original RIPLAY from any product detail page to verify the source.

Success looks like: a buyer arrives without insurance vocabulary, identifies 2–3 candidate products in under five minutes, and leaves the site with enough understanding to ask the right questions of an agent (or to confidently choose to stay with BPJS only). The site is an aid for the buyer side of a market currently dominated by the seller side.

Built for the Kaggle Gemma 4 Good hackathon (Digital Equity & Inclusivity track, submission deadline 2026-05-18).

## Brand Personality

Embracing, reassuring, protective, editorial calm. Voice is a knowledgeable friend reading the document with the user, not a salesperson. Three-word personality: **protective · grounded · plainspoken**. Indonesian copy is plain and low-jargon by default; technical terms are introduced only where the source document requires them, and always with quiet context.

Emotional goal: the user should feel less alone in front of a 60-page PDF. No urgency, no upsell, no aspirational lifestyle framing. Confidence comes from sources being open, not from hype.

## Anti-references

- **pasal.id** — Indonesian aggregator pattern with saturated brand color and the "Jelajahi Berdasarkan Jenis" category grid. asuransi.id deliberately differentiates the browse-grid card design (center-aligned, no icon+count split, serif lead name, mono micro qualifier) and rejects the saturated brand-block treatment.
- **Generic insurance-marketing sites** (Allianz / Prudential / AXA brand sites) — aspirational lifestyle photography of smiling families and happy patients, glossy CTAs, sales-funnel framing. asuransi.id shows tables and citations, not aspiration.
- **Crypto / fintech dark-mode tropes** — navy + gold, neon-on-black, "trust through severity". Category reflex for finance. Light, warm, editorial paper is the answer instead.

## Design Principles

1. **Honest about failures.** Products whose RIPLAY could not be auto-parsed render with a yellow informational banner and a direct link to the source PDF — never a red error, never silent omission. Failure is an honesty signal, not a malfunction.

2. **Interpretation, not authority.** The site is an aid, not an advisor. The RIPLAY is the binding document; asuransi.id is a reading tool over it. Gemma 4 frames and summarizes; it never asserts coverage or invents a Rupiah figure. A non-dismissable disclaimer makes this role unambiguous.

3. **Editorial restraint over commercial polish.** Warm off-white paper, serif headlines, mono numerals. Brand color present in small doses (≤10% of any viewport), never as a full-bleed block. Reject SaaS chrome (gradients, hero-metric template, drop shadows, streamed-token effects) and reject insurance-marketing aspiration (lifestyle photos, mascots, urgency).

4. **Sources are accessible, not invisible.** Every policy detail page links to its original RIPLAY and brosur PDFs. The normalized numbers in the app are distilled from those documents; a user who wants to verify can open the source in one click. Verifiability is the differentiator versus generic AI chatbots that hallucinate insurance numbers.

## Accessibility & Inclusion

- Contrast: ≥ 4.5:1 on body text, ≥ 3:1 on micro-labels. Mono numerals tabular for column alignment in comparison tables.
- Semantic table structure (`<table>`, `<th scope>`, row/column headers) so screen-reader users can navigate manfaat by row and column.
- Low-end Android usable: no horizontal scroll on the home page, modest JS payload, works on metered mobile data.
- Reduced motion respected. No streamed-token effect on the Gemma response — render the structured block once retrieval completes.
- Indonesian primary, English fallback via locale toggle. Empty states and error messages written in plain Indonesian first ("Tidak ada produk cocok dengan kriteria. Coba kurangi filter…"), not technical or developer-speak.
- Formal WCAG audit is out of scope for the MVP; the targets above are the working standard.
