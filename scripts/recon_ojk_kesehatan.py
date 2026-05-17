import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

import pandas as pd
from bs4 import BeautifulSoup
from curl_cffi import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OJK_XLSX = PROJECT_ROOT / "data" / "raw" / "ojk" / "Direktori_Asuransi_Triwulan_III_2025.xlsx"
OUT_PATH = PROJECT_ROOT / "data" / "raw" / "recon" / "ojk_kesehatan_candidates.json"

SHEETS = ["Asuransi Jiwa", "Asuransi Umum"]
HEADER_ROW = 0

KEYWORDS = ("kesehatan", "health", "medical", "medis")
HIGH_VALUE_TOKENS = ("asuransi-kesehatan", "asuransi kesehatan", "individu", "kesehatan-individu")


def clean_website(raw: str | None) -> str | None:
    if not raw or not isinstance(raw, str):
        return None
    s = raw.strip().rstrip("/")
    if not s or s.lower() in ("-", "n/a", "tidak ada"):
        return None
    if not s.startswith("http"):
        s = "https://" + s
    return s


def load_ojk_insurers() -> list[dict]:
    out: list[dict] = []
    for sheet in SHEETS:
        df = pd.read_excel(OJK_XLSX, sheet_name=sheet, header=HEADER_ROW)
        df.columns = [str(c).strip() for c in df.columns]
        name_col = next((c for c in df.columns if "Nama Perusahaan" in c), None)
        web_col = next((c for c in df.columns if c.lower().startswith("website")), None)
        jenis_col = next((c for c in df.columns if "Jenis Perusahaan" in c), None)
        if not name_col or not web_col:
            continue
        for _, row in df.iterrows():
            name = row.get(name_col)
            if not isinstance(name, str) or not name.strip():
                continue
            web = clean_website(row.get(web_col))
            if not web:
                continue
            out.append({
                "name": name.strip(),
                "sheet": sheet,
                "jenis": str(row.get(jenis_col, "")).strip() if jenis_col else "",
                "website": web,
            })
    seen: dict[str, dict] = {}
    for item in out:
        key = urlparse(item["website"]).netloc.lower()
        if key not in seen:
            seen[key] = item
    return list(seen.values())


def score_link(href: str, text: str) -> int:
    hay = (href + " " + text).lower()
    score = 0
    for tok in HIGH_VALUE_TOKENS:
        if tok in hay:
            score += 3
    for tok in KEYWORDS:
        if tok in hay:
            score += 1
    return score


def probe(insurer: dict) -> dict:
    url = insurer["website"]
    result: dict = {
        **insurer,
        "status": None,
        "error": None,
        "final_url": None,
        "links": [],
        "score": 0,
    }
    try:
        r = requests.get(url, impersonate="chrome", timeout=30, allow_redirects=True)
        result["status"] = r.status_code
        result["final_url"] = str(r.url)
        soup = BeautifulSoup(r.text, "html.parser")
        seen: set[str] = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(" ", strip=True)
            s = score_link(href, text)
            if s == 0:
                continue
            full = urljoin(str(r.url), href)
            key = full + "||" + text[:80]
            if key in seen:
                continue
            seen.add(key)
            result["links"].append({"url": full, "text": text[:160], "score": s})
        result["score"] = sum(l["score"] for l in result["links"])
    except Exception as e:
        result["error"] = repr(e)
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="Probe every OJK-listed insurer for kesehatan product links.")
    ap.add_argument("--out", type=Path, default=OUT_PATH)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--limit", type=int, help="Process only first N insurers (debug).")
    args = ap.parse_args()

    if not OJK_XLSX.exists():
        print("OJK xlsx not found: " + str(OJK_XLSX), file=sys.stderr)
        sys.exit(1)

    insurers = load_ojk_insurers()
    if args.limit:
        insurers = insurers[: args.limit]
    print("loaded " + str(len(insurers)) + " unique insurers from OJK directory")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(probe, ins): ins for ins in insurers}
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)
            tag = "OK  " if res["status"] == 200 else "FAIL"
            host = urlparse(res.get("final_url") or res["website"]).netloc
            err = res["error"] or ""
            print(f"[{tag}] score={res['score']:3d} links={len(res['links']):2d} {host:40s} {res['name'][:50]} {err[:40]}")

    results.sort(key=lambda r: (-r["score"], -len(r["links"]), r["name"]))
    args.out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print("\nwrote " + str(args.out))

    print("\n=== top 25 candidates by kesehatan-link score ===")
    for r in results[:25]:
        host = urlparse(r.get("final_url") or r["website"]).netloc
        print(f"  score={r['score']:3d} links={len(r['links']):2d}  {r['name'][:55]:55s} {host}")


if __name__ == "__main__":
    main()
