import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_INSURERS = PROJECT_ROOT / "data" / "raw" / "insurers"
PARSED_INSURERS = PROJECT_ROOT / "data" / "parsed" / "insurers"
NORMALIZED = PROJECT_ROOT / "data" / "normalized"

# Canonical manfaat categories. Order matters — more specific patterns first.
CATEGORY_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("icu", re.compile(r"\b(icu|intensive\s+care|unit\s+perawatan\s+intensif|santunan\s+perawatan\s+intensif)\b", re.IGNORECASE)),
    ("kamar_rs", re.compile(r"\b(biaya\s+)?kamar(\s+dan\s+akomodasi)?(\s+harian)?(\s+(rumah\s+sakit|rawat\s+inap))?\b", re.IGNORECASE)),
    ("dialisis", re.compile(r"\b(dialisis|cuci\s+darah|hemodialisa)\b", re.IGNORECASE)),
    ("rehabilitasi", re.compile(r"\b(rehabilitasi|terapi\s+okupasi|terapi\s+wicara|fisioterapi)\b", re.IGNORECASE)),
    ("perawatan_di_rumah", re.compile(r"\b(perawatan\s+di\s+rumah|perawat\s+pribadi\s+di\s+rumah|juru\s+rawat)\b", re.IGNORECASE)),
    ("pengobatan_tradisional", re.compile(r"\bpengobatan\s+tradisional\b|\bakupuntur\b|\btiongkok\b", re.IGNORECASE)),
    ("telehealth", re.compile(r"\b(telehealth|telekonsultasi|telemedicine)\b", re.IGNORECASE)),
    ("infeksi_tropis", re.compile(r"\b(demam\s+berdarah|tifus|paratifus|malaria)\b", re.IGNORECASE)),
    ("dokter_umum", re.compile(r"\bdokter\s+umum\b", re.IGNORECASE)),
    ("dokter_spesialis", re.compile(r"\bdokter\s+spesialis\b", re.IGNORECASE)),
    ("dokter_inpatient", re.compile(r"\b(kunjungan\s+dokter|biaya\s+konsultasi)\b", re.IGNORECASE)),
    ("obat_inpatient", re.compile(r"\b(obat(\s+resep)?|bahan\s+habis\s+pakai|aneka\s+perawatan\s+rumah\s+sakit|lain[-\s]?lain\s+rawat\s+inap)\b", re.IGNORECASE)),
    ("diagnostik_inpatient", re.compile(r"\b(laboratorium|diagnostik|pemeriksaan|tes\s+diagnostik)\b", re.IGNORECASE)),
    ("tindakan_bedah", re.compile(r"\b(pembedahan|tindakan\s+bedah|bedah\s+sehari|bedah\s+rekonstruktif)\b(?!.*rawat\s+jalan)", re.IGNORECASE)),
    ("pre_hospitalization", re.compile(r"\b(perawatan\s+)?sebelum\s+rawat\s+inap\b", re.IGNORECASE)),
    ("post_hospitalization", re.compile(r"\b(perawatan\s+)?(setelah|sesudah)\s+rawat\s+inap\b", re.IGNORECASE)),
    ("gawat_darurat", re.compile(r"\b(gawat\s+darurat|rawat\s+jalan\s+darurat|emergency)\b", re.IGNORECASE)),
    ("rawat_jalan", re.compile(r"\brawat\s+jalan\b", re.IGNORECASE)),
    ("ambulans", re.compile(r"\bambulan(s|ce)?\b", re.IGNORECASE)),
    ("kanker", re.compile(r"\b(kanker|cancer|kemoterapi|chemotherapy|radioterapi|radiotherapy)\b", re.IGNORECASE)),
    ("penyakit_kritis", re.compile(r"\b(penyakit\s+kritis|critical\s+illness)\b", re.IGNORECASE)),
    ("hiv_aids", re.compile(r"\b(hiv|aids)\b", re.IGNORECASE)),
    ("kesehatan_mental", re.compile(r"\b(psikiater|kesehatan\s+mental|mental\s+health)\b", re.IGNORECASE)),
    ("maternity", re.compile(r"\b(kehamilan|melahirkan|persalinan|maternity)\b", re.IGNORECASE)),
    ("dental", re.compile(r"\b(gigi|dental)\b", re.IGNORECASE)),
    ("optical", re.compile(r"\b(optik|optical|kacamata|perawatan\s+mata)\b", re.IGNORECASE)),
    ("second_opinion", re.compile(r"\b(second\s+opinion|expert\s+medical\s+opinion|medical\s+assistance)\b", re.IGNORECASE)),
    ("prostesis_implan", re.compile(r"\b(prostesis|prothesis|prosthesis|implan|implants?|anggota\s+tubuh\s+artifisial|crown)\b", re.IGNORECASE)),
    ("preventive", re.compile(r"\b(pencegahan|preventive)\b", re.IGNORECASE)),
    ("alat_medis", re.compile(r"\bperalatan\s+medis\b|\balat\s+medis\b", re.IGNORECASE)),
    ("pengobatan_luar_negeri", re.compile(r"\b(pengobatan|perawatan)\s+(di\s+)?luar\s+negeri\b", re.IGNORECASE)),
    ("santunan_harian", re.compile(r"\bsantunan(\s+tunai)?\s+harian\b", re.IGNORECASE)),
    ("pemakaman", re.compile(r"\b(pemakaman|funeral|santunan\s+(meninggal|kematian)|meninggal\s+dunia)\b", re.IGNORECASE)),
    ("deductible", re.compile(r"\b(risiko\s+sendiri|deductible|tanggungan\s+sendiri|co[-\s]?pay)\b", re.IGNORECASE)),
    ("akomodasi_pendamping", re.compile(r"\bakomodasi\s+pendamping\b|\bpendamping\s+(tertanggung|inap)\b", re.IGNORECASE)),
    ("annual_limit", re.compile(r"\b(annual\s+limit|batas\s+(manfaat\s+)?tahunan|maksimum\s+manfaat\s+tahunan|manfaat\s+tahunan)\b", re.IGNORECASE)),
    ("limit_booster", re.compile(r"\b(limit\s+booster|booster)\b", re.IGNORECASE)),
]

# Labels that should never be mapped — section headers / regions / disambiguators.
SKIP_LABEL_PATTERNS = [
    re.compile(r"^\s*wilayah\s+(pertanggungan|asuransi|perlindungan)\b", re.IGNORECASE),
    re.compile(r"^\s*di\s+luar\s+wilayah\b", re.IGNORECASE),
    re.compile(r"^\s*(besar|kecil|sedang|kompleks)\s*$", re.IGNORECASE),
    re.compile(r"^\s*\d+\s*$"),
    re.compile(r"^\s*manfaat\s+lainnya\s+yang\s+berkaitan\b", re.IGNORECASE),
    re.compile(r"^\s*manfaat\s+tambahan\s+untuk\s+semua\b", re.IGNORECASE),
]

UNIT_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("per_day", re.compile(r"\bper\s+hari\b|/hari", re.IGNORECASE)),
    ("per_visit", re.compile(r"\bper\s+kunjungan\b|/kunjungan", re.IGNORECASE)),
    ("per_event", re.compile(r"\bper\s+(rawat\s+inap|perawatan|klaim|kejadian|kali)\b", re.IGNORECASE)),
    ("per_year", re.compile(r"\bper\s+tahun(\s+polis)?\b|/tahun", re.IGNORECASE)),
    ("per_lifetime", re.compile(r"\bseumur\s+hidup\b|\bper\s+(masa\s+)?polis\b", re.IGNORECASE)),
    ("percent_of_bill", re.compile(r"%\s*(dari|of)\s+tagihan|persen\s+tagihan", re.IGNORECASE)),
    ("no_cap", re.compile(r"\b(sesuai\s+tagihan|as\s+charged|ditanggung|tanpa\s+batas)\b", re.IGNORECASE)),
]

# Header keywords used to detect canonical Tabel Manfaat.
TABEL_MANFAAT_HEADER_TOKENS = ("manfaat", "jenis manfaat", "no.")
PLAN_COLUMN_REGEX = re.compile(
    r"\b("
    r"plan\s*\d+"
    r"|plan\s+[ivx]+\b"
    r"|plan\s+(a|b|c|d|e|f|g|h|i|standar|standard|extra|premier|premium)\b"
    r"|sehat\s+[a-z]\b"
    r"|(diamond|ruby|emerald|topaz|jade|sapphire|bronze|silver|gold|platinum)\b"
    r"|maxi\s+\w+"
    r"|as\s+charged"
    r"|plan\s+(?!(diamond|ruby|emerald|topaz|jade|sapphire|bronze|silver|gold|platinum|rp\d|rp\b|manfaat|biaya|kamar|plan)\b)[a-z][a-z0-9-]*\b"
    r"|santunan\s+\w+\d*"
    r"|ip[-\s]\d+"
    r")",
    re.IGNORECASE,
)

NUMERIC_TOKEN_RE = re.compile(r"\d[\d.,]*")
RANGE_OR_DECIMAL_RE = re.compile(r"(\d+(?:[.,]\d+)?)")


def is_manfaat_header(col: str) -> bool:
    c = col.strip().lower()
    return any(t in c for t in TABEL_MANFAAT_HEADER_TOKENS)


_PLAN_QUALIFIER_RE = re.compile(
    r"^(?P<core>(plan\s*[a-z0-9ivx]+|sehat\s+[a-z]|bronze\s+[ab]|silver\s+[ab]|diamond|ruby|emerald|topaz|jade|sapphire|gold|platinum|bronze|silver|maxi\s+\w+|as\s+charged|santunan\s+\w+\d*(\s+\d+)?|ip[-\s]\d+)"
    r"(?:\s+(?:indonesia|smart|premier|extra|standard))*)",
    re.IGNORECASE,
)


_PLAN_PARENT_RE = re.compile(r"^plan(\s*\([^)]*\))?$", re.IGNORECASE)
_PLAN_TIER_VALUE_RE = re.compile(r"^([a-z]|\d+|[ivx]+|\d+[a-z]|[a-z]\d+)$", re.IGNORECASE)


def _synth_parent_child_plan(col: str) -> str | None:
    # Docling renders cluster headers like "Plan (Rp).I" as parent.child.
    # Only fire when a segment is literally "Plan" (optionally with a currency
    # tag) and the last segment is a bare tier value (letter / digits / roman).
    # Refuses noisy parent.child headers where last segment is a benefit label.
    parts = [p.strip() for p in col.split(".") if p.strip()]
    if len(parts) < 2:
        return None
    if not any(_PLAN_PARENT_RE.match(p) for p in parts):
        return None
    if not _PLAN_TIER_VALUE_RE.match(parts[-1]):
        return None
    return "Plan " + parts[-1]


_BODY_PROSE_WORDS_RE = re.compile(
    r"\b(atau|yang|dari|untuk|dengan|sesuai|pilih|salah|tertanggung|kalender|tagihan)\b",
    re.IGNORECASE,
)
_PAREN_PHRASE_RE = re.compile(r"\(\s*\w+\s+\w+")


def _is_plausible_plan_header_part(p: str) -> bool:
    # Reject docling header parts that read like penjelasan / body text.
    # Real plan-tier headers are short tokens: "Plan A", "Diamond",
    # "Topaz Indonesia / Topaz Indonesia Smart". Body text leaks contain
    # commas, sentence connectives, or parenthesized phrases.
    if len(p) > 60:
        return False
    if "," in p:
        return False
    if _PAREN_PHRASE_RE.search(p):
        return False
    if _BODY_PROSE_WORDS_RE.search(p):
        return False
    return True


def plan_name_from_col(col: str) -> str:
    # Docling concatenates multi-line table headers with '.'. Pick the segment that contains a plan match, then keep only the canonical plan token + standard qualifiers (Smart / Indonesia).
    parts = [p.strip() for p in col.split(".") if p.strip()]
    if not parts:
        return col.strip()
    for p in parts:
        if not _is_plausible_plan_header_part(p):
            continue
        if "manfaat" in p.lower():
            continue
        m = PLAN_COLUMN_REGEX.search(p)
        if not m:
            continue
        tail = p[m.start():]
        qm = _PLAN_QUALIFIER_RE.match(tail)
        if qm:
            return re.sub(r"\s+", " ", qm.group("core")).strip().title()
        return m.group(0).title()
    synth = _synth_parent_child_plan(col)
    if synth and PLAN_COLUMN_REGEX.search(synth):
        tier = synth.split(" ", 1)[1]
        if re.fullmatch(r"[ivx]+", tier, re.IGNORECASE):
            return "Plan " + tier.upper()
        return synth.title()
    return parts[0]


def is_plan_header(col: str) -> bool:
    for p in col.split("."):
        ps = p.strip()
        if not _is_plausible_plan_header_part(ps):
            continue
        # Parts that contain "manfaat" are benefit-label columns, not plan tiers.
        if "manfaat" in ps.lower():
            continue
        if PLAN_COLUMN_REGEX.search(p):
            return True
    synth = _synth_parent_child_plan(col)
    if synth and PLAN_COLUMN_REGEX.search(synth):
        return True
    return False


def looks_like_tabel_manfaat(columns: list[str]) -> bool:
    has_manfaat = any(is_manfaat_header(c) for c in columns)
    has_plan = sum(1 for c in columns if is_plan_header(c)) >= 1
    return has_manfaat and has_plan


def detect_plan_columns(columns: list[str]) -> list[int]:
    return [i for i, c in enumerate(columns) if is_plan_header(c)]


def detect_manfaat_column(columns: list[str], plan_cols: list[int] | None = None) -> int:
    plan_cols = plan_cols or []
    candidates = [
        i for i, c in enumerate(columns)
        if i not in plan_cols and ("manfaat" in c.strip().lower() or "jenis manfaat" in c.strip().lower())
    ]
    # Docling renders both the "No." column and the real benefit-name column
    # with header "MANFAAT" when the source PDF merges them. When the first
    # two manfaat-tagged columns have identical labels, that's the merge
    # signature — prefer the second column, since it carries the benefit
    # text and not the row numbers.
    if len(candidates) >= 2 and columns[candidates[0]].strip().lower() == columns[candidates[1]].strip().lower():
        return candidates[1]
    if candidates:
        return candidates[0]
    for i, c in enumerate(columns):
        if c.strip().lower() == "no.":
            return i + 1 if i + 1 < len(columns) else i
    return 0


def detect_penjelasan_column(columns: list[str], manfaat_col: int, plan_cols: list[int]) -> int | None:
    for i, c in enumerate(columns):
        if i == manfaat_col or i in plan_cols:
            continue
        cl = c.strip().lower()
        if "penjelasan" in cl or "deskripsi" in cl:
            return i
    return None


def map_category(label: str) -> str | None:
    for cat, pat in CATEGORY_PATTERNS:
        if pat.search(label):
            return cat
    return None


def parse_unit(text: str) -> str | None:
    for unit, pat in UNIT_PATTERNS:
        if pat.search(text):
            return unit
    return None


def parse_amount(cell: str, multiplier: int = 1000) -> int | None:
    if not cell or cell.strip() in ("-", "—", "n/a", "N/A"):
        return None
    # Descriptive prose (e.g. "Mana yang lebih besar antara Kamar terendah dengan 1 tempat tidur") — don't extract a number.
    if len(cell) > 40 and cell.count(" ") >= 5:
        return None
    s = cell.replace(".", "").replace(",", ".").strip()
    m = re.search(r"\d+(?:\.\d+)?", s)
    if not m:
        return None
    val = float(m.group(0))
    return int(val * multiplier)


def is_section_header_row(row: list[str], manfaat_col: int, penjelasan_col: int | None, plan_cols: list[int]) -> bool:
    plans_empty = all(not row[i].strip() or row[i].strip() in ("-", "—") for i in plan_cols)
    label = row[manfaat_col].strip()
    if penjelasan_col is not None:
        same = label == row[penjelasan_col].strip()
        return plans_empty or same
    return plans_empty


_GLUED_WORD_BOUNDARIES = re.compile(r"\b(MANFAAT|RAWAT|INAP|JALAN|BIAYA|DOKTER|KAMAR|HARIAN|MENINGGAL|BEDAH|PERAWATAN)(?=[A-Z])", re.IGNORECASE)


def normalize_label(s: str) -> str:
    # Docling sometimes drops spaces — handle two cases:
    #   "DokterUmum" → camelCase boundary
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", s)
    #   "MANFAATMENINGGAL" → all-caps, insert space before the next Indonesian medical-insurance word.
    s = _GLUED_WORD_BOUNDARIES.sub(r"\1 ", s)
    # Strip leading bullet/dash and No. column bleeds.
    s = re.sub(r"^\s*[-•]\s*", "", s)
    s = re.sub(r"^\s*\d+\s+", "", s)
    return s.strip()


def should_skip_label(s: str) -> bool:
    if any(pat.search(s) for pat in SKIP_LABEL_PATTERNS):
        return True
    # Reject labels that look like raw values rather than benefit names.
    s_stripped = s.strip()
    if re.fullmatch(r"[\d.,]+", s_stripped):
        return True
    if s_stripped.lower() in ("sesuai tagihan", "as charged", "ditanggung", "-", "—"):
        return True
    return False


INTEGER_HEADER_RE = re.compile(r"^\d+$")
BARE_PLAN_LETTER_RE = re.compile(r"^[A-H]$")


def promote_header_if_integer_indexed(table: dict) -> dict:
    columns = table["columns"]
    if not columns or not all(INTEGER_HEADER_RE.match(c) for c in columns):
        return table
    for idx, row in enumerate(table["rows"]):
        joined = " ".join(row).lower()
        if "manfaat" not in joined:
            continue
        has_explicit_plan = any(PLAN_COLUMN_REGEX.search(c) for c in row)
        bare_letter_count = sum(1 for c in row if BARE_PLAN_LETTER_RE.match(c.strip()))
        if not has_explicit_plan and bare_letter_count < 2:
            continue
        # Rewrite bare letters to "Plan X" so downstream PLAN_COLUMN_REGEX matches.
        new_cols = ["Plan " + c.strip() if BARE_PLAN_LETTER_RE.match(c.strip()) else c for c in row]
        return {**table, "columns": new_cols, "rows": table["rows"][idx + 1:]}
    return table


def build_plans(tables: list[dict]) -> tuple[list[dict], list[dict]]:
    tables = [promote_header_if_integer_indexed(t) for t in tables]
    canonical = [t for t in tables if looks_like_tabel_manfaat(t["columns"])]
    if not canonical:
        raise ValueError("no tabel manfaat detected")
    plans: dict[str, list[dict]] = {}
    unmapped: list[dict] = []
    for t in canonical:
        columns = t["columns"]
        plan_cols = detect_plan_columns(columns)
        if not plan_cols:
            continue
        manfaat_col = detect_manfaat_column(columns, plan_cols)
        penjelasan_col = detect_penjelasan_column(columns, manfaat_col, plan_cols)
        for row in t["rows"]:
            if manfaat_col >= len(row):
                continue
            if is_section_header_row(row, manfaat_col, penjelasan_col, plan_cols):
                continue
            label = normalize_label(row[manfaat_col])
            if not label or should_skip_label(label):
                continue
            cat = map_category(label)
            penjelasan = row[penjelasan_col].strip() if penjelasan_col is not None and penjelasan_col < len(row) else ""
            unit = parse_unit(label + " " + penjelasan)
            if cat is None:
                unmapped.append({"label": label, "penjelasan": penjelasan, "row": row})
                continue
            for i in plan_cols:
                cell = row[i].strip() if i < len(row) else ""
                if not cell or cell in ("-", "—"):
                    continue
                amount = parse_amount(cell)
                cell_unit = unit or parse_unit(cell)
                note = None
                if any(t in cell.lower() for t in ("sesuai tagihan", "as charged", "ditanggung")):
                    note = cell
                    amount = None
                    cell_unit = "no_cap"
                plan_name = plan_name_from_col(columns[i])
                plans.setdefault(plan_name, []).append({
                    "category": cat,
                    "amount_rp": amount,
                    "unit": cell_unit,
                    "note": note,
                    "raw_cell": cell,
                    "raw_label": label,
                    "penjelasan": penjelasan or None,
                })
    return [{"plan_name": name, "manfaat": items} for name, items in plans.items()], unmapped


def normalize_product(product_meta: dict) -> tuple[dict | None, dict | None]:
    riplay_rel = product_meta.get("source_pdfs", {}).get("riplay")
    if not riplay_rel:
        if product_meta.get("plans"):
            # Pre-normalized record (e.g. BPJS hardcoded regulatory data).
            return product_meta, None
        return None, {
            "product_id": product_meta["product_id"],
            "reason": "no riplay PDF in product metadata",
        }
    parsed_pdf = Path(str(PROJECT_ROOT / riplay_rel).replace("/data/raw/", "/data/parsed/"))
    tables_path = parsed_pdf.with_suffix(".tables.json")
    if not tables_path.exists():
        return None, {
            "product_id": product_meta["product_id"],
            "reason": "tables.json missing",
            "expected_path": str(tables_path),
        }
    data = json.loads(tables_path.read_text())
    try:
        plans, unmapped = build_plans(data["tables"])
    except ValueError as e:
        return None, {
            "product_id": product_meta["product_id"],
            "tables_path": str(tables_path),
            "reason": str(e),
        }
    record = {
        **{k: product_meta[k] for k in ("product_id", "product_name", "insurer_slug", "insurer_name", "insurer_category", "product_type", "jenis", "product_page_url", "source_pdfs", "source_pdf_urls", "scraped_at") if k in product_meta},
        "currency": "IDR",
        "plans": plans,
    }
    failure = None
    if unmapped:
        failure = {
            "product_id": product_meta["product_id"],
            "tables_path": str(tables_path),
            "reason": "unmapped manfaat rows",
            "unmapped_count": len(unmapped),
            "unmapped_samples": unmapped[:5],
        }
    return record, failure


def main() -> None:
    ap = argparse.ArgumentParser(description="Map docling tables to canonical policies.json schema.")
    ap.add_argument("--only", nargs="*", help="Limit to product_id substrings.")
    args = ap.parse_args()
    NORMALIZED.mkdir(parents=True, exist_ok=True)
    products_files = list(RAW_INSURERS.glob("*/products.json"))
    if not products_files:
        print("no products.json files found", file=sys.stderr)
        sys.exit(1)
    policies: list[dict] = []
    failures: list[dict] = []
    for pf in sorted(products_files):
        for pm in json.loads(pf.read_text()):
            if args.only and not any(s in pm["product_id"] for s in args.only):
                continue
            record, failure = normalize_product(pm)
            if record is not None:
                policies.append(record)
                pcounts = ", ".join(f"{p['plan_name']}={len(p['manfaat'])}" for p in record["plans"])
                print(f"[OK] {pm['product_id']}  plans: {pcounts}")
            if failure is not None:
                failures.append(failure)
                print(f"[WARN] {pm['product_id']}  {failure['reason']}")
    (NORMALIZED / "policies.json").write_text(json.dumps(policies, ensure_ascii=False, indent=2))
    (NORMALIZED / "parse_failures.json").write_text(json.dumps(failures, ensure_ascii=False, indent=2))
    print(f"\nWrote {len(policies)} policies, {len(failures)} failures")


if __name__ == "__main__":
    main()
