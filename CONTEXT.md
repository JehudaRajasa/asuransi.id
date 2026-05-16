# asuransi.id — Domain Context

## Glossary

### Asuransi Kesehatan
Private individual health insurance products (asuransi kesehatan individu) sold by OJK-licensed private insurers (Allianz, Prudential, AXA, Manulife, Sequis, etc.), plus BPJS Kesehatan as a public/government baseline comparator.

### BPJS Kesehatan
Government mandatory health insurance, single product with 3 tiers (Class I/II/III), fixed premium per class. Public baseline against which private policies are compared.

### OJK (Otoritas Jasa Keuangan)
Indonesian Financial Services Authority. Source of truth for the list of legally registered insurers. Every insurer in the directory must appear on OJK's licensed list. Insurers not yet scraped for product data are shown with status `data pending`.

**Source:** OJK publishes a quarterly Excel file `Direktori Asuransi Triwulan <Q> <Year>.xlsx` at `ojk.go.id/id/kanal/iknb/data-dan-statistik/direktori/asuransi/Documents/`. Read with `pandas.read_excel`.

### RIPLAY (Ringkasan Informasi Produk dan Layanan)
OJK-mandated standardized product summary (POJK 23/2023). Every Indonesian insurer must publish one per consumer product. Uniform structure across insurers: product identity, manfaat (benefits), tabel manfaat, exclusions, waiting periods, claim procedure, T&C. **Primary data source.** Linked from each product detail page on insurer site.

### Brosur (marketing brochure)
Marketing PDF per product on insurer site. Contains product summary and sample claim/payout illustrations. Secondary data source for claim illustrations and supplementary benefit details.

## Data sourcing scope (MVP)

| Data class | Source |
|---|---|
| Insurer directory | OJK quarterly direktori xlsx |
| Manfaat (benefits) & tabel manfaat | RIPLAY (primary), Brosur (supplement) |
| Uang pertanggungan / coverage limits | RIPLAY tabel manfaat |
| Exclusions (pengecualian) | RIPLAY |
| Waiting periods (masa tunggu) | RIPLAY |
| Claim procedure (cashless/reimbursement) | RIPLAY |
| Hospital network info | RIPLAY or insurer product page |
| Claim payout illustrations | Brosur |
| Age entry, coverage duration | RIPLAY |
| Payment modes (annual/semi/quarterly/monthly) | RIPLAY |

## Priority insurers (5)
- Allianz (`PT Asuransi Allianz Life Indonesia` / `PT Asuransi Allianz Utama Indonesia`)
- Prudential (`PT Prudential Life Assurance`)
- AXA Mandiri (`PT Axa Mandiri Financial Services`)
- Manulife (`PT Asuransi Jiwa Manulife Indonesia`)
- BPJS Kesehatan (hardcoded — fixed regulatory tiers)

## Scraping stack
- `curl-cffi` — HTML/PDF fetch with TLS fingerprint mimicry
- `beautifulsoup4` — HTML parse, find brochure links
- `docling` — PDF → Markdown + structured tables (ML-based, single parser for all layouts)
- Deterministic regex + table parsing — map docling tables to canonical schema
- Gemma 4 — chatbot layer only

## Pipeline layout
```
scripts/
├── _common.py
├── scrape_ojk.py
├── recon_*.py
└── insurers/
    ├── allianz/scrape.py
    ├── prudential/scrape.py
    ├── manulife/scrape.py
    └── bpjs-kesehatan/scrape.py

data/
├── raw/                          # immutable downloads (HTML + PDF)
│   ├── ojk/
│   └── insurers/<insurer>/<product>/
│       ├── page.html
│       ├── riplay-*.pdf
│       └── brosur-*.pdf
├── parsed/                       # docling output, re-runnable
│   └── insurers/<insurer>/<product>/
│       ├── riplay-*.md
│       ├── riplay-*.tables.json
│       ├── brosur-*.md
│       └── brosur-*.tables.json
└── normalized/                   # canonical schema (deliverable)
    ├── insurers.json
    ├── policies.json
    └── parse_failures.json
```

## Output: policies.json schema (draft)
```jsonc
{
  "product_id": "allianz-preferred-medical",
  "product_name": "Allianz Preferred Medical",
  "insurer_name": "PT Asuransi Allianz Life Indonesia",
  "insurer_slug": "allianz",
  "insurer_category": "asuransi_jiwa",
  "product_type": "kesehatan_individu",
  "jenis": "konvensional",         // | "syariah"
  "product_page_url": "https://www.allianz.co.id/...",
  "source_pdfs": {
    "riplay": "https://...riplay-umum-allianz-preferred-medical.pdf",
    "brosur": "https://...brosur-allianz-preferred-medical.pdf"
  },
  "scraped_at": "2026-05-15T...",
  "age_entry": {"min_months": 1, "max_years": 75},
  "coverage_until_age": 100,
  "payment_modes": ["tahunan", "semesteran", "kuartalan", "bulanan"],
  "currency": "IDR",
  "coverage_regions": ["Indonesia", "Asia", "Worldwide"],
  "plans": [
    {
      "plan_name": "Plan Standar",
      "annual_limit_rp": null,
      "manfaat": [
        {"category": "kamar_rs", "amount_rp": 500000, "unit": "per_day"},
        {"category": "icu", "amount_rp": 1000000, "unit": "per_day"},
        {"category": "tindakan_bedah", "amount_rp": null, "note": "sesuai tagihan"}
      ]
    }
  ],
  "waiting_periods": {
    "general_days": 30,
    "cancer_months": 3,
    "specific_diseases_months": 6,
    "hiv_aids_months": 6
  },
  "exclusions": ["..."],
  "claim_procedure": ["cashless", "reimbursement"],
  "hospital_network": {"name": "Preferred Network / Other Network", "url_or_note": "..."},
  "claim_illustrations": [
    {"profile": "Bapak Lutfi, age 30, Plan Premier", "scenario": "Gagal Ginjal tahun ke-2", "payout_rp": null}
  ]
}
```
