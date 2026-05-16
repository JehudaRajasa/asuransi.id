import argparse
import re
from pathlib import Path

import pymupdf4llm
from curl_cffi import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "data" / "raw" / "brosur"

BROSURS = {
    "allianz_preferred_medical": "https://www.allianz.co.id/content/dam/onemarketing/azli/wwwallianzcoid/produk/asuransi-individu/asuransi-kesehatan/allianz-preferred-medical/brosur-v-2-6/brosur-allianz-preferred-medical.pdf",
    "allianz_preferred_medical_riplay": "https://www.allianz.co.id/content/dam/onemarketing/azli/wwwallianzcoid/produk/asuransi-individu/asuransi-kesehatan/allianz-preferred-medical/riplay-v-2-1/riplay-umum-allianz-preferred-medical.pdf",
    "prudential_prusehat_brochure": "https://www.prudential.co.id/content/dam/prudential-aem-lbu/plai/pdf/Brochure-PRUSehat.pdf",
    "prudential_prusehat_summary": "https://www.prudential.co.id/content/dam/prudential-aem-lbu/plai/pdf/Product-Summary-PRUSehat.pdf",
    "manulife_miuhc_brosur": "https://www.manulife.co.id/content/dam/insurance/id/id/documents/produk/brosur/Brosur%20MiUltimate%20Health%20Care%20(MiUHC).pdf",
    "manulife_miuhc_ringkasan": "https://www.manulife.co.id/content/dam/insurance/id/id/documents/produk/ringkasan-informasi-produk/MiUltimate%20HealthCare%20(MiUHC)%20-%20Ringkasan%20Informasi%20Produk%20dan%20Layanan%20Umum.pdf",
}

PRICE_KEYWORDS = [
    "premi",
    "iuran",
    "biaya",
    "contoh premi",
    "ilustrasi premi",
    "tarif",
    "rate",
    "rp ",
    "rp.",
]

RP_AMOUNT_RE = re.compile(r"rp[.\s]*\d[\d.,]*", re.IGNORECASE)


def download(url: str, dest: Path) -> None:
    if dest.exists():
        return
    r = requests.get(url, impersonate="chrome", timeout=60)
    r.raise_for_status()
    dest.write_bytes(r.content)


def scan(slug: str, url: str) -> None:
    dest = CACHE_DIR / f"{slug}.pdf"
    download(url, dest)
    md = pymupdf4llm.to_markdown(str(dest))
    md_path = CACHE_DIR / f"{slug}.md"
    md_path.write_text(md)

    text = md.lower()
    print(f"\n=== {slug} ===")
    print(f"  pdf bytes:    {dest.stat().st_size}")
    print(f"  md chars:     {len(md)}")
    print(f"  md tables:    {md.count('|---')}  (approx, by `|---` separator rows)")
    print(f"  keyword hits:")
    for kw in PRICE_KEYWORDS:
        count = text.count(kw)
        if count:
            print(f"    {kw!r:24s} x {count}")
    rp_matches = RP_AMOUNT_RE.findall(md)
    print(f"  Rp amounts:   {len(rp_matches)} matches")
    for m in rp_matches[:10]:
        print(f"    {m}")
    if len(rp_matches) > 10:
        print(f"    ... +{len(rp_matches) - 10} more")

    page_hits = []
    for i, page in enumerate(md.split("\n-----\n"), start=1):
        if any(kw in page.lower() for kw in ("premi", "iuran", "contoh premi")):
            page_hits.append(i)
    print(f"  premi-mentioning page blocks: {page_hits[:20]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe brosur/RIPLAY PDFs for pricing signals.")
    parser.add_argument("--only", nargs="*", default=list(BROSURS.keys()))
    args = parser.parse_args()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    for slug in args.only:
        scan(slug, BROSURS[slug])


if __name__ == "__main__":
    main()
