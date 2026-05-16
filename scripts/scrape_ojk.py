import argparse
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urljoin

import pandas as pd
from _common import slugify_insurer
from bs4 import BeautifulSoup
from curl_cffi import requests

OJK_BASE = "https://ojk.go.id"
DIREKTORI_INDEX = f"{OJK_BASE}/id/kanal/iknb/data-dan-statistik/direktori/asuransi/default.aspx"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "ojk"
NORMALIZED_PATH = PROJECT_ROOT / "data" / "normalized" / "insurers.json"
QUARTER_LINK_RE = re.compile(r"Direktori-Asuransi-Triwulan-([IV]+)-(\d{4})", re.IGNORECASE)

SHEET_CATEGORY_MAP = {
    "Asuransi Jiwa": "asuransi_jiwa",
    "Asuransi Umum": "asuransi_umum",
    "Reasuransi": "reasuransi",
    "Asuransi Wajib": "asuransi_wajib",
    "Asuransi Sosial": "asuransi_sosial",
}

FIELD_MAP = {
    "Nama Perusahaan": "name",
    "Jenis Perusahaan": "jenis_perusahaan",
    "Jenis Kantor": "jenis_kantor",
    "No Izin": "license_no",
    "Tanggal Izin": "license_date",
    "Alamat": "address",
    "Kota": "city",
    "Kode Pos": "postal_code",
    "No Telp": "phone",
    "Email": "email",
    "Website": "website",
}


def fetch(url: str) -> str:
    r = requests.get(url, impersonate="chrome", timeout=30)
    r.raise_for_status()
    return r.text


def find_latest_quarter_url(index_html: str) -> tuple[str, str]:
    soup = BeautifulSoup(index_html, "html.parser")
    for a in soup.find_all("a", href=True):
        m = QUARTER_LINK_RE.search(a["href"])
        if m:
            quarter_label = f"Triwulan {m.group(1).upper()} {m.group(2)}"
            return urljoin(OJK_BASE, a["href"]), quarter_label
    sys.exit("No quarterly direktori link found on OJK index page.")


def find_xlsx_url(quarter_html: str) -> str:
    soup = BeautifulSoup(quarter_html, "html.parser")
    for a in soup.find_all("a", href=True):
        if a["href"].lower().endswith(".xlsx"):
            return urljoin(OJK_BASE, a["href"])
    sys.exit("No .xlsx link found on quarterly direktori sub-page.")


def download_binary(url: str, dest: Path) -> None:
    r = requests.get(url, impersonate="chrome", timeout=60)
    r.raise_for_status()
    dest.write_bytes(r.content)


def clean(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.date().isoformat()
    if isinstance(value, str):
        v = value.strip()
        return v or None
    return value


def normalize_sheet(df: pd.DataFrame, category: str, source_quarter: str) -> list[dict]:
    records = []
    for _, row in df.iterrows():
        record: dict[str, object] = {"category": category, "source_quarter": source_quarter}
        for src_col, dst_field in FIELD_MAP.items():
            if src_col in df.columns:
                record[dst_field] = clean(row[src_col])
            else:
                record[dst_field] = None
        if record["name"]:
            record["slug"] = slugify_insurer(str(record["name"]))
            records.append(record)
    return records


def normalize_xlsx(xlsx_path: Path, source_quarter: str) -> list[dict]:
    xl = pd.ExcelFile(xlsx_path)
    all_records: list[dict] = []
    for sheet_name in xl.sheet_names:
        key = sheet_name.strip()
        category = SHEET_CATEGORY_MAP.get(key)
        if not category:
            continue
        df = xl.parse(sheet_name)
        all_records.extend(normalize_sheet(df, category, source_quarter))
    return all_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape OJK insurer direktori (latest quarter).")
    parser.add_argument("--raw-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--normalized-path", type=Path, default=NORMALIZED_PATH)
    parser.add_argument("--inspect", action="store_true", help="Print sheet names, columns, head of each sheet.")
    args = parser.parse_args()

    args.raw_dir.mkdir(parents=True, exist_ok=True)
    args.normalized_path.parent.mkdir(parents=True, exist_ok=True)

    print("Fetching OJK direktori index...")
    index_html = fetch(DIREKTORI_INDEX)
    quarter_url, quarter_label = find_latest_quarter_url(index_html)
    print(f"Latest quarter: {quarter_label} -> {quarter_url}")

    quarter_html = fetch(quarter_url)
    xlsx_url = find_xlsx_url(quarter_html)
    print("xlsx URL: " + xlsx_url)

    filename = unquote(xlsx_url.rsplit("/", 1)[-1]).replace(" ", "_")
    dest = args.raw_dir / filename
    print(f"Downloading -> {dest}")
    download_binary(xlsx_url, dest)
    print(f"Saved {dest.stat().st_size} bytes")

    if args.inspect:
        xl = pd.ExcelFile(dest)
        print("\nSheets: " + ", ".join(xl.sheet_names))
        for name in xl.sheet_names:
            df = xl.parse(name)
            print(f"\n=== Sheet: {name} ({len(df)} rows, {len(df.columns)} cols) ===")
            print("Columns: " + ", ".join(str(c) for c in df.columns))
            print(df.head(3).to_string(max_cols=8))

    records = normalize_xlsx(dest, quarter_label)
    args.normalized_path.write_text(json.dumps(records, ensure_ascii=False, indent=2))
    print(f"\nNormalized {len(records)} insurers -> {args.normalized_path}")
    by_cat: dict[str, int] = {}
    for r in records:
        by_cat[r["category"]] = by_cat.get(r["category"], 0) + 1
    for cat, n in sorted(by_cat.items()):
        print(f"  {cat}: {n}")


if __name__ == "__main__":
    main()
