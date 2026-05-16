import argparse
import sys
import time
from pathlib import Path

from docling.document_converter import DocumentConverter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW = PROJECT_ROOT / "data" / "raw" / "insurers"

TARGETS = [
    RAW / "allianz/allianz-life/allianz-preferred-medical/riplay-umum-allianz-preferred-medical.pdf",
    RAW / "allianz/allianz-life/smarthealth-maxi-violet/riplay-umum-maxi-violet-final.pdf",
    RAW / "manulife/jiwa-manulife/miultimate-healthcare/MiUltimate HealthCare (MiUHC) - Ringkasan Informasi Produk dan Layanan Umum.pdf",
    RAW / "prudential/prudential-life-assurance/prusehat/Product-Summary-PRUSehat.pdf",
    RAW / "prudential/prudential-life-assurance/pruwell-medical/PS-PRUWell-Medical.pdf",
]

OUT_DIR = PROJECT_ROOT / "scripts" / "parser_probe" / "out_docling"


def probe(pdf: Path, converter: DocumentConverter) -> dict:
    label = f"{pdf.parent.parent.name}/{pdf.parent.name}"
    print("\n== " + label + " ==", flush=True)
    if not pdf.exists():
        print("MISSING: " + str(pdf))
        return {"label": label, "ok": False, "reason": "missing"}
    t0 = time.time()
    result = converter.convert(str(pdf))
    elapsed = time.time() - t0
    doc = result.document
    md = doc.export_to_markdown()
    tables = list(doc.tables) if hasattr(doc, "tables") else []
    md_path = OUT_DIR / (label.replace("/", "__") + ".md")
    md_path.write_text(md)
    print(f"elapsed={elapsed:.1f}s  tables={len(tables)}  md_bytes={len(md)}  -> {md_path.name}")
    for i, tbl in enumerate(tables[:3]):
        try:
            df = tbl.export_to_dataframe()
            print(f"  table[{i}] shape={df.shape}  cols={list(df.columns)[:6]}")
        except Exception as e:
            print(f"  table[{i}] dataframe error: {e!r}")
    return {"label": label, "ok": True, "elapsed_s": elapsed, "n_tables": len(tables), "md_bytes": len(md)}


def main() -> None:
    ap = argparse.ArgumentParser(description="Probe docling on representative health insurance PDFs.")
    ap.add_argument("--only", nargs="*", help="Substring filter on label.")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Initializing docling converter (cold ML init may take 1-2 min)...", flush=True)
    converter = DocumentConverter()

    results: list[dict] = []
    for pdf in TARGETS:
        label = f"{pdf.parent.parent.name}/{pdf.parent.name}"
        if args.only and not any(s in label for s in args.only):
            continue
        try:
            results.append(probe(pdf, converter))
        except Exception as e:
            print(f"  ERROR: {e!r}")
            results.append({"label": label, "ok": False, "reason": repr(e)})

    print("\n=== summary ===")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
