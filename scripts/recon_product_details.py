import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from curl_cffi import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = PROJECT_ROOT / "data" / "raw" / "recon" / "product_details.json"

PRODUCT_URLS = {
    "allianz": "https://www.allianz.co.id/produk/asuransi-individu/asuransi-kesehatan/allianz-preferred-medical.html",
    "prudential": "https://www.prudential.co.id/id/products/asuransi-kesehatan/prusehat/",
    "axa_mandiri": "https://www.axa-mandiri.co.id/asuransi-mandiri-solusi-kesehatan",
    "manulife": "https://www.manulife.co.id/id/produk/kesehatan/asuransi-kesehatan/miultimate-healthcare.html",
}


def probe(insurer: str, url: str) -> dict:
    result: dict = {
        "insurer": insurer,
        "url": url,
        "status": None,
        "final_url": None,
        "error": None,
        "html_bytes": 0,
        "visible_text_chars": 0,
        "table_count": 0,
        "form_count": 0,
        "email_input_count": 0,
        "pdf_links": [],
        "iframe_srcs": [],
        "title": None,
        "h1": [],
        "h2": [],
    }
    try:
        r = requests.get(url, impersonate="chrome", timeout=30, allow_redirects=True)
        result["status"] = r.status_code
        result["final_url"] = str(r.url)
        result["html_bytes"] = len(r.content)
        soup = BeautifulSoup(r.text, "html.parser")

        if soup.title and soup.title.string:
            result["title"] = soup.title.string.strip()
        result["h1"] = [h.get_text(" ", strip=True)[:120] for h in soup.find_all("h1")][:5]
        result["h2"] = [h.get_text(" ", strip=True)[:120] for h in soup.find_all("h2")][:10]

        visible = soup.get_text(" ", strip=True)
        result["visible_text_chars"] = len(visible)
        result["table_count"] = len(soup.find_all("table"))
        result["form_count"] = len(soup.find_all("form"))
        result["email_input_count"] = len(soup.find_all("input", attrs={"type": "email"}))

        base = str(r.url)
        seen_pdf: set[str] = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full = urljoin(base, href)
            if full.lower().split("?", 1)[0].endswith(".pdf") and full not in seen_pdf:
                seen_pdf.add(full)
                text = a.get_text(" ", strip=True)
                result["pdf_links"].append({"url": full, "text": text[:120]})

        for iframe in soup.find_all("iframe", src=True):
            src = urljoin(base, iframe["src"])
            result["iframe_srcs"].append(src)
    except Exception as e:
        result["error"] = repr(e)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Third-pass recon: probe sample product detail pages.")
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=len(PRODUCT_URLS)) as pool:
        futures = {pool.submit(probe, ins, url): ins for ins, url in PRODUCT_URLS.items()}
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)
            tag = "OK " if res["status"] == 200 else "FAIL"
            print(f"[{tag}] {res['insurer']:12s} status={res['status']} bytes={res['html_bytes']} text={res['visible_text_chars']} tables={res['table_count']} forms={res['form_count']} pdfs={len(res['pdf_links'])}")

    results.sort(key=lambda r: list(PRODUCT_URLS.keys()).index(r["insurer"]))
    args.out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nWrote {args.out}\n")

    for r in results:
        print(f"=== {r['insurer']} ===")
        print(f"  URL:    {r['final_url']}")
        print(f"  title:  {r['title']}")
        if r["h1"]:
            print(f"  h1:     {r['h1']}")
        if r["h2"]:
            print(f"  h2:     {r['h2'][:5]}{'...' if len(r['h2']) > 5 else ''}")
        print(f"  signal: html_bytes={r['html_bytes']} text_chars={r['visible_text_chars']} tables={r['table_count']} forms={r['form_count']} email_inputs={r['email_input_count']}")
        if r["pdf_links"]:
            print(f"  PDFs ({len(r['pdf_links'])}):")
            for pdf in r["pdf_links"][:10]:
                print(f"    {pdf['url']}\n      {pdf['text']}")
            if len(r["pdf_links"]) > 10:
                print(f"    ... +{len(r['pdf_links']) - 10} more")
        else:
            print("  PDFs: none")
        if r["iframe_srcs"]:
            print(f"  iframes ({len(r['iframe_srcs'])}):")
            for s in r["iframe_srcs"][:5]:
                print(f"    {s}")
        print()


if __name__ == "__main__":
    main()
