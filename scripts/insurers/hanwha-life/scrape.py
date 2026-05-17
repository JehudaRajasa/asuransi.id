import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _common import (
    download_pdf,
    fetch_html,
    find_pdf_links,
    product_slug_from_url,
    render_markdown,
)
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "insurers" / "hanwha-life"

# Hanwha Life category page is JS-rendered; only `/category/kesehatan/` known
# from static HTML, with one individu health product. Hardcode the URL.
LANDING_CFG = {
    "insurer_slug": "hanwha-life",
    "insurer_name": "PT Hanwha Life Insurance Indonesia",
    "insurer_category": "asuransi_jiwa",
    "jenis": "konvensional",
}

PRODUCT_URLS = [
    "https://www.hanwhalife.co.id/produk-hanwha/hanwha-premier-health-care/",
]


def scrape_product(product_url: str, out_dir: Path) -> dict:
    slug = product_slug_from_url(product_url)
    print(f"\n-> [{LANDING_CFG['insurer_slug']}] {slug}  ({product_url})")
    product_dir = out_dir / LANDING_CFG["insurer_slug"] / slug
    product_dir.mkdir(parents=True, exist_ok=True)

    html = fetch_html(product_url)
    (product_dir / "page.html").write_text(html)

    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    product_name = h1.get_text(" ", strip=True) if h1 else (soup.title.string.strip() if soup.title and soup.title.string else slug)

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
        "product_id": f"{LANDING_CFG['insurer_slug']}-{slug}",
        "product_name": product_name,
        "insurer_slug": LANDING_CFG["insurer_slug"],
        "insurer_name": LANDING_CFG["insurer_name"],
        "insurer_category": LANDING_CFG["insurer_category"],
        "product_type": "kesehatan_individu",
        "jenis": LANDING_CFG["jenis"],
        "product_page_url": product_url,
        "source_pdfs": source_pdf_paths,
        "source_pdf_urls": source_pdf_urls,
        "scraped_at": datetime.now(UTC).isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Hanwha Life health insurance product pages and PDFs.")
    parser.add_argument("--out-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--only", nargs="*", help="Limit to specific product slugs.")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    all_records: list[dict] = []
    print(f"\n=== Scraping {len(PRODUCT_URLS)} Hanwha Life products (hardcoded list — JS-only category page) ===")
    for url in PRODUCT_URLS:
        slug = product_slug_from_url(url)
        if args.only and slug not in args.only:
            continue
        try:
            all_records.append(scrape_product(url, args.out_dir))
        except Exception as e:
            print(f"   ERROR scraping {slug}: {e!r}")

    out_json = args.out_dir / "products.json"
    out_json.write_text(json.dumps(all_records, ensure_ascii=False, indent=2))
    print(f"\nWrote {out_json} ({len(all_records)} products)")


if __name__ == "__main__":
    main()
