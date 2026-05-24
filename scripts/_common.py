import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from curl_cffi import requests
from docling.document_converter import DocumentConverter

_PT_PREFIX = re.compile(r"^pt\.?\s+", re.IGNORECASE)
_ASURANSI = re.compile(r"\basuransi\b", re.IGNORECASE)
_INDONESIA = re.compile(r"\bindonesia\b", re.IGNORECASE)
_PERSERO = re.compile(r"\(persero\)", re.IGNORECASE)
_TBK = re.compile(r"\btbk\.?\b", re.IGNORECASE)
_NONWORD = re.compile(r"[^a-z0-9]+")

DEFAULT_RIPLAY_MARKERS = ("riplay", "ringkasan", "ringkasan-informasi-produk", "product-summary", "product-information")
DEFAULT_BROSUR_MARKERS = ("brosur", "brochure")


# Map the raw slugify output of selected OJK official names to the
# shorter consumer-facing slug used in product scrapes and URLs.
# Without this override, e.g. "PT Asuransi Jiwa BCA" → "jiwa-bca" would
# never match the product-side "bca-life", and the insurer record would
# orphan from its policies.
_SLUG_OVERRIDES = {
    "jiwa-bca": "bca-life",
    "bni-life-insurance": "bni-life",
    "central-asia-financial": "car",
    "jiwa-generali": "generali",
    "jiwa-sequis-life": "sequis",
    "sun-life-financial": "sun-life",
    "zurich-topas-life": "zurich-topas",
}


def slugify_insurer(name: str) -> str:
    s = name.lower()
    s = _PT_PREFIX.sub("", s)
    s = _ASURANSI.sub("", s)
    s = _INDONESIA.sub("", s)
    s = _PERSERO.sub("", s)
    s = _TBK.sub("", s)
    s = _NONWORD.sub("-", s)
    raw = s.strip("-")
    return _SLUG_OVERRIDES.get(raw, raw)


def fetch_html(url: str, timeout: int = 30) -> str:
    r = requests.get(url, impersonate="chrome", timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    return r.text


def fetch_bytes(url: str, timeout: int = 120) -> bytes:
    r = requests.get(url, impersonate="chrome", timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    return r.content


def discover_product_urls(
    landing_html: str,
    landing_url: str,
    product_path_prefix: str,
    exclude_path_suffixes: tuple[str, ...] = (),
) -> list[dict]:
    soup = BeautifulSoup(landing_html, "html.parser")
    landing_path = urlparse(landing_url).path
    seen: set[str] = set()
    out: list[dict] = []
    for a in soup.find_all("a", href=True):
        full = urljoin(landing_url, a["href"])
        path = urlparse(full).path
        if not path.lower().startswith(product_path_prefix.lower()):
            continue
        if path == landing_path:
            continue
        if any(path.lower().endswith(suf) for suf in exclude_path_suffixes):
            continue
        if full in seen:
            continue
        seen.add(full)
        out.append({"url": full, "text": a.get_text(" ", strip=True)[:120]})
    return out


def find_pdf_links(
    html: str,
    base_url: str,
    riplay_markers: tuple[str, ...] = DEFAULT_RIPLAY_MARKERS,
    brosur_markers: tuple[str, ...] = DEFAULT_BROSUR_MARKERS,
) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    riplay: str | None = None
    brosur: str | None = None
    others: list[str] = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href.lower().split("?", 1)[0].endswith(".pdf"):
            continue
        full = urljoin(base_url, href)
        marker = (full + " " + a.get_text(" ", strip=True)).lower()
        if riplay is None and any(m in marker for m in riplay_markers):
            riplay = full
        elif brosur is None and any(m in marker for m in brosur_markers):
            brosur = full
        else:
            others.append(full)
    return {"riplay": riplay, "brosur": brosur, "others": others}


def product_slug_from_url(url: str) -> str:
    path = urlparse(url).path
    last = path.rstrip("/").rsplit("/", 1)[-1]
    if last.endswith(".html"):
        last = last[: -len(".html")]
    return last


def download_pdf(url: str, dest: Path) -> None:
    if dest.exists():
        return
    dest.write_bytes(fetch_bytes(url))


_RAW_SEG = "/data/raw/"
_PARSED_SEG = "/data/parsed/"

_converter: DocumentConverter | None = None


def _get_converter() -> DocumentConverter:
    # Lazy singleton — docling model init is heavy (~1-2 min cold).
    global _converter
    if _converter is None:
        _converter = DocumentConverter()
    return _converter


def parsed_path_for(raw_pdf_path: Path) -> Path:
    s = str(raw_pdf_path)
    if _RAW_SEG not in s:
        raise ValueError("pdf path must be under data/raw/: " + s)
    return Path(s.replace(_RAW_SEG, _PARSED_SEG, 1))


def render_markdown(pdf_path: Path) -> dict:
    parsed_pdf_path = parsed_path_for(pdf_path)
    md_path = parsed_pdf_path.with_suffix(".md")
    tables_path = parsed_pdf_path.with_suffix(".tables.json")
    if md_path.exists() and tables_path.exists():
        return {"md": md_path, "tables": tables_path}

    md_path.parent.mkdir(parents=True, exist_ok=True)
    result = _get_converter().convert(str(pdf_path))
    doc = result.document
    md_path.write_text(doc.export_to_markdown())

    table_records: list[dict] = []
    for i, tbl in enumerate(getattr(doc, "tables", []) or []):
        try:
            df = tbl.export_to_dataframe(doc=doc)
        except TypeError:
            df = tbl.export_to_dataframe()
        table_records.append({
            "index": i,
            "columns": [str(c) for c in df.columns],
            "rows": df.astype(str).values.tolist(),
        })
    tables_path.write_text(json.dumps({
        "source_pdf": str(pdf_path),
        "n_tables": len(table_records),
        "tables": table_records,
    }, ensure_ascii=False, indent=2))
    return {"md": md_path, "tables": tables_path}
