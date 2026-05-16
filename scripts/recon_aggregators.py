import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from curl_cffi import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = PROJECT_ROOT / "data" / "raw" / "recon" / "aggregators.json"

CANDIDATES = {
    "lifepal_kesehatan": "https://lifepal.co.id/asuransi-kesehatan/",
    "lifepal_kesehatan_alt": "https://lifepal.co.id/produk/asuransi-kesehatan/",
    "cermati_kesehatan": "https://www.cermati.com/asuransi-kesehatan",
    "cekaja_kesehatan": "https://www.cekaja.com/asuransi-kesehatan",
    "qoala_kesehatan": "https://www.qoala.app/id/asuransi-kesehatan/",
    "duitpintar_kesehatan": "https://duitpintar.com/asuransi-kesehatan/",
}

RP_AMOUNT_RE = re.compile(r"rp[.\s]*[\d][\d.,]*", re.IGNORECASE)
INSURER_TARGETS = ["allianz", "prudential", "axa mandiri", "axa", "manulife", "bpjs"]


def probe(slug: str, url: str) -> dict:
    result: dict = {
        "slug": slug,
        "url": url,
        "status": None,
        "final_url": None,
        "error": None,
        "html_bytes": 0,
        "visible_text_chars": 0,
        "rp_amount_count": 0,
        "rp_amount_sample": [],
        "insurer_mentions": {},
        "title": None,
        "card_signals": {},
    }
    try:
        r = requests.get(url, impersonate="chrome", timeout=30, allow_redirects=True)
        result["status"] = r.status_code
        result["final_url"] = str(r.url)
        result["html_bytes"] = len(r.content)
        soup = BeautifulSoup(r.text, "html.parser")

        if soup.title and soup.title.string:
            result["title"] = soup.title.string.strip()

        visible = soup.get_text(" ", strip=True)
        result["visible_text_chars"] = len(visible)
        rp_matches = RP_AMOUNT_RE.findall(visible)
        result["rp_amount_count"] = len(rp_matches)
        result["rp_amount_sample"] = rp_matches[:15]

        low = visible.lower()
        for target in INSURER_TARGETS:
            result["insurer_mentions"][target] = low.count(target)

        result["card_signals"] = {
            "article_count": len(soup.find_all("article")),
            "card_class_hits": len(soup.select("[class*=card]")),
            "product_class_hits": len(soup.select("[class*=product]")),
            "premium_class_hits": len(soup.select("[class*=premium], [class*=premi], [class*=price]")),
        }
    except Exception as e:
        result["error"] = repr(e)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe aggregator sites for asuransi-kesehatan pricing data.")
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    parser.add_argument("--candidates", nargs="*", default=list(CANDIDATES.keys()))
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=len(args.candidates)) as pool:
        futures = {pool.submit(probe, slug, CANDIDATES[slug]): slug for slug in args.candidates}
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)
            tag = "OK " if res["status"] == 200 else "FAIL"
            print(f"[{tag}] {res['slug']:30s} status={res['status']} bytes={res['html_bytes']} text={res['visible_text_chars']} rp={res['rp_amount_count']} err={res['error']}")

    results.sort(key=lambda r: args.candidates.index(r["slug"]) if r["slug"] in args.candidates else 999)
    args.out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nWrote {args.out}\n")

    for r in results:
        print(f"=== {r['slug']} ===  {r['final_url']}")
        if r["error"]:
            print(f"  ERROR: {r['error']}")
            print()
            continue
        print(f"  title:   {r['title']}")
        print(f"  signal:  text={r['visible_text_chars']} rp_count={r['rp_amount_count']} cards={r['card_signals']}")
        print(f"  insurer_mentions: {r['insurer_mentions']}")
        print(f"  rp samples: {r['rp_amount_sample']}")
        print()


if __name__ == "__main__":
    main()
