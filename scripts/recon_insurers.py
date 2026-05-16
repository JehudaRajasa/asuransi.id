import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from curl_cffi import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INSURERS_PATH = PROJECT_ROOT / "data" / "normalized" / "insurers.json"
OUT_PATH = PROJECT_ROOT / "data" / "raw" / "recon" / "insurer_links.json"

TARGET_SITES = [
    "www.allianz.co.id",
    "www.prudential.co.id",
    "www.axa-mandiri.co.id",
    "www.manulife.co.id",
    "www.bpjs-kesehatan.go.id",
]

KEYWORDS = ("kesehatan", "health", "medical", "medis")


def normalize_url(site: str) -> str:
    if site.startswith("http"):
        return site
    return f"https://{site}/"


def probe(site: str) -> dict:
    url = normalize_url(site)
    result: dict = {"site": site, "url": url, "status": None, "error": None, "links": []}
    try:
        r = requests.get(url, impersonate="chrome", timeout=30, allow_redirects=True)
        result["status"] = r.status_code
        result["final_url"] = str(r.url)
        soup = BeautifulSoup(r.text, "html.parser")
        seen: set[str] = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(" ", strip=True)
            haystack = (href + " " + text).lower()
            if any(k in haystack for k in KEYWORDS):
                full = urljoin(str(r.url), href)
                key = (full, text[:80])
                key_str = full + "||" + text[:80]
                if key_str in seen:
                    continue
                seen.add(key_str)
                result["links"].append({"url": full, "text": text[:120]})
    except Exception as e:
        result["error"] = repr(e)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe target insurer homepages for asuransi-kesehatan links.")
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    parser.add_argument("--sites", nargs="*", default=TARGET_SITES)
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=len(args.sites)) as pool:
        futures = {pool.submit(probe, s): s for s in args.sites}
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)
            tag = "OK " if res["status"] == 200 else "FAIL"
            print(f"[{tag}] {res['site']:30s} status={res['status']} links={len(res['links'])} err={res['error']}")

    results.sort(key=lambda r: args.sites.index(r["site"]) if r["site"] in args.sites else 999)
    args.out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nWrote {args.out}")

    for r in results:
        host = urlparse(r.get("final_url") or r["url"]).netloc
        print(f"\n=== {r['site']} ({host}) ===")
        if r["error"]:
            print(f"ERROR: {r['error']}")
            continue
        for link in r["links"][:15]:
            print(f"  {link['url']}\n    {link['text']}")
        if len(r["links"]) > 15:
            print(f"  ... +{len(r['links']) - 15} more")


if __name__ == "__main__":
    main()
