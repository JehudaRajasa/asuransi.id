import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import (
    discover_product_urls,
    download_pdf,
    fetch_html,
    find_pdf_links,
    product_slug_from_url,
    render_markdown,
)
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "insurers" / "manulife"

LANDING_URL = "https://www.manulife.co.id/id/produk/kesehatan/asuransi-kesehatan.html"
PRODUCT_PATH_PREFIX = "/id/produk/kesehatan/asuransi-kesehatan/"


def resolve_insurer(product_slug: str, product_name: str) -> dict:
    is_syariah = "syariah" in product_slug.lower() or "syariah" in product_name.lower()
    if is_syariah:
        return {
            "insurer_slug": "jiwa-manulife-syariah",
            "insurer_name": "PT Asuransi Jiwa Manulife Indonesia Syariah",
            "insurer_category": "asuransi_jiwa",
            "jenis": "syariah",
        }
    return {
        "insurer_slug": "jiwa-manulife",
        "insurer_name": "PT Asuransi Jiwa Manulife Indonesia",
        "insurer_category": "asuransi_jiwa",
        "jenis": "konvensional",
    }


def scrape_product(product_url: str, out_dir: Path) -> dict:
    slug = product_slug_from_url(product_url)
    html = fetch_html(product_url)
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    product_name = h1.get_text(" ", strip=True) if h1 else (soup.title.string.strip() if soup.title and soup.title.string else slug)

    insurer = resolve_insurer(slug, product_name)
    print(f"\n-> [{insurer['insurer_slug']}] {slug}  ({product_url})")

    product_dir = out_dir / insurer["insurer_slug"] / slug
    product_dir.mkdir(parents=True, exist_ok=True)
    (product_dir / "page.html").write_text(html)

    pdfs = find_pdf_links(html, product_url)
    print(f"   pdfs: riplay={'Y' if pdfs['riplay'] else 'N'} brosur={'Y' if pdfs['brosur'] else 'N'} others={len(pdfs['others'])}")

    source_pdf_paths: dict[str, str] = {}
    source_pdf_urls: dict[str, str] = {}
    for kind in ("riplay", "brosur"):
        url = pdfs[kind]
        if not url:
            continue
        filename = unquote(url.rsplit("/", 1)[-1].split("?", 1)[0])
        pdf_dest = product_dir / filename
        download_pdf(url, pdf_dest)
        print(f"   downloaded {kind}: {filename} ({pdf_dest.stat().st_size} bytes)")
        rendered = render_markdown(pdf_dest)
        print(f"   parsed: {rendered['md'].name} ({rendered['md'].stat().st_size}B md, tables.json)")
        source_pdf_paths[kind] = str(pdf_dest.relative_to(PROJECT_ROOT))
        source_pdf_urls[kind] = url

    return {
        "product_id": f"{insurer['insurer_slug']}-{slug}",
        "product_name": product_name,
        "insurer_slug": insurer["insurer_slug"],
        "insurer_name": insurer["insurer_name"],
        "insurer_category": insurer["insurer_category"],
        "product_type": "kesehatan_individu",
        "jenis": insurer["jenis"],
        "product_page_url": product_url,
        "source_pdfs": source_pdf_paths,
        "source_pdf_urls": source_pdf_urls,
        "scraped_at": datetime.now(UTC).isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Manulife health insurance product pages and PDFs (conv + syariah on same domain).")
    parser.add_argument("--out-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--only", nargs="*", help="Limit to specific product slugs.")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== Landing: Manulife ({LANDING_URL}) ===")
    landing_html = fetch_html(LANDING_URL)
    products = discover_product_urls(landing_html, LANDING_URL, PRODUCT_PATH_PREFIX)
    print(f"Discovered {len(products)} products")
    for p in products:
        slug = product_slug_from_url(p["url"])
        print(f"  - {slug}: {p['text']}")

    all_records: list[dict] = []
    for p in products:
        slug = product_slug_from_url(p["url"])
        if args.only and slug not in args.only:
            continue
        try:
            all_records.append(scrape_product(p["url"], args.out_dir))
        except Exception as e:
            print(f"   ERROR scraping {slug}: {e!r}")

    out_json = args.out_dir / "products.json"
    out_json.write_text(json.dumps(all_records, ensure_ascii=False, indent=2))
    by_slug: dict[str, int] = {}
    for r in all_records:
        by_slug[r["insurer_slug"]] = by_slug.get(r["insurer_slug"], 0) + 1
    print(f"\nWrote {out_json} ({len(all_records)} products)")
    for slug, n in sorted(by_slug.items()):
        print(f"  {slug}: {n}")


if __name__ == "__main__":
    main()
