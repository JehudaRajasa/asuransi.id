import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from curl_cffi import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = PROJECT_ROOT / "data" / "raw" / "recon" / "product_landings.json"

LANDINGS = {
    "allianz": "https://www.allianz.co.id/produk/asuransi-individu/asuransi-kesehatan.html",
    "prudential": "https://www.prudential.co.id/id/products/asuransi-kesehatan/",
    "axa_mandiri": "https://www.axa-mandiri.co.id/asuransi-kesehatan-individu",
    "manulife": "https://www.manulife.co.id/id/produk/kesehatan/asuransi-kesehatan.html",
}

PRODUCT_PATH_PREFIX = {
    "allianz": "/produk/asuransi-individu/asuransi-kesehatan/",
    "prudential": "/id/products/asuransi-kesehatan/",
    "axa_mandiri": "/asuransi-",
    "manulife": "/id/produk/kesehatan/",
}


def probe(insurer: str, url: str) -> dict:
    result: dict = {
        "insurer": insurer,
        "url": url,
        "status": None,
        "final_url": None,
        "error": None,
        "product_links": [],
        "pdf_links": [],
    }
    try:
        r = requests.get(url, impersonate="chrome", timeout=30, allow_redirects=True)
        result["status"] = r.status_code
        result["final_url"] = str(r.url)
        soup = BeautifulSoup(r.text, "html.parser")
        base = str(r.url)
        host = urlparse(base).netloc
        prefix = PRODUCT_PATH_PREFIX[insurer]

        seen_product: set[str] = set()
        seen_pdf: set[str] = set()

        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(" ", strip=True)
            full = urljoin(base, href)
            path = urlparse(full).path
            netloc = urlparse(full).netloc

            if netloc != host:
                continue

            if path.lower().endswith(".pdf") and full not in seen_pdf:
                seen_pdf.add(full)
                result["pdf_links"].append({"url": full, "text": text[:120]})
                continue

            if path.lower().startswith(prefix.lower()) and full != base and full not in seen_product:
                if path.rstrip("/").rstrip(".html") == urlparse(base).path.rstrip("/").rstrip(".html"):
                    continue
                seen_product.add(full)
                result["product_links"].append({"url": full, "text": text[:120]})
    except Exception as e:
        result["error"] = repr(e)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Second-pass recon: probe per-insurer product landing pages.")
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    parser.add_argument("--insurers", nargs="*", default=list(LANDINGS.keys()))
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=len(args.insurers)) as pool:
        futures = {pool.submit(probe, ins, LANDINGS[ins]): ins for ins in args.insurers}
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)
            tag = "OK " if res["status"] == 200 else "FAIL"
            print(f"[{tag}] {res['insurer']:12s} status={res['status']} products={len(res['product_links'])} pdfs={len(res['pdf_links'])} err={res['error']}")

    results.sort(key=lambda r: args.insurers.index(r["insurer"]))
    args.out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nWrote {args.out}\n")

    for r in results:
        print(f"=== {r['insurer']} ===  {r['final_url']}")
        if r["error"]:
            print(f"  ERROR: {r['error']}")
            print()
            continue
        print(f"  -- product pages ({len(r['product_links'])}) --")
        for link in r["product_links"][:20]:
            print(f"  {link['url']}\n    {link['text']}")
        if len(r["product_links"]) > 20:
            print(f"  ... +{len(r['product_links']) - 20} more")
        print(f"  -- PDFs ({len(r['pdf_links'])}) --")
        for link in r["pdf_links"][:10]:
            print(f"  {link['url']}\n    {link['text']}")
        if len(r["pdf_links"]) > 10:
            print(f"  ... +{len(r['pdf_links']) - 10} more")
        print()


if __name__ == "__main__":
    main()
