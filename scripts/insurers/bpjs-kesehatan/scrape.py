import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "insurers" / "bpjs-kesehatan"

REGULATORY_SOURCE = {
    "name": "Peraturan Presiden Nomor 64 Tahun 2020",
    "url": "https://peraturan.bpk.go.id/Details/137139/perpres-no-64-tahun-2020",
    "note": "Iuran JKN nasional. Tarif dapat berubah seiring revisi Perpres.",
}

JKN_MANFAAT = [
    {"category": "rawat_jalan", "amount_rp": None, "unit": "no_cap", "note": "Pelayanan kesehatan tingkat pertama (FKTP) dan rujukan (FKRTL) tanpa biaya tambahan untuk peserta aktif"},
    {"category": "rawat_inap_umum", "amount_rp": None, "unit": "no_cap", "note": "Sesuai kelas perawatan kepesertaan"},
    {"category": "tindakan_bedah", "amount_rp": None, "unit": "no_cap", "note": "Sesuai indikasi medis dan rujukan"},
    {"category": "gawat_darurat", "amount_rp": None, "unit": "no_cap", "note": "Pelayanan IGD di FKTP dan FKRTL"},
    {"category": "ambulans", "amount_rp": None, "unit": "no_cap", "note": "Antar fasilitas kesehatan rujukan"},
    {"category": "maternity", "amount_rp": None, "unit": "no_cap", "note": "Pemeriksaan kehamilan, persalinan, dan nifas"},
    {"category": "kanker", "amount_rp": None, "unit": "no_cap", "note": "Termasuk kemoterapi dan radioterapi"},
    {"category": "hiv_aids", "amount_rp": None, "unit": "no_cap", "note": "Obat ARV dan pemeriksaan rutin"},
    {"category": "kesehatan_mental", "amount_rp": None, "unit": "no_cap", "note": "Konsultasi psikiatri dan obat sesuai formularium"},
    {"category": "dental", "amount_rp": None, "unit": "no_cap", "note": "Tindakan dasar dan rujukan tertentu"},
    {"category": "optical", "amount_rp": 330000, "unit": "per_2_years", "note": "Subsidi kacamata. Plafon bervariasi per kelas."},
]

PLANS = [
    {
        "plan_name": "Kelas I (Mandiri PBPU)",
        "annual_limit_rp": None,
        "premium_rp_per_month": 150000,
        "kamar_rs_class": "Kelas I (1-2 tempat tidur per kamar)",
        "manfaat": JKN_MANFAAT + [
            {"category": "kamar_rs", "amount_rp": None, "unit": "no_cap", "note": "Kelas I"},
        ],
    },
    {
        "plan_name": "Kelas II (Mandiri PBPU)",
        "annual_limit_rp": None,
        "premium_rp_per_month": 100000,
        "kamar_rs_class": "Kelas II (3-4 tempat tidur per kamar)",
        "manfaat": JKN_MANFAAT + [
            {"category": "kamar_rs", "amount_rp": None, "unit": "no_cap", "note": "Kelas II"},
        ],
    },
    {
        "plan_name": "Kelas III (Mandiri PBPU)",
        "annual_limit_rp": None,
        "premium_rp_per_month": 35000,
        "kamar_rs_class": "Kelas III (5+ tempat tidur per kamar)",
        "manfaat": JKN_MANFAAT + [
            {"category": "kamar_rs", "amount_rp": None, "unit": "no_cap", "note": "Kelas III"},
        ],
        "note": "Tarif mandiri Rp 42.000/bulan dengan subsidi pemerintah Rp 7.000 menjadi Rp 35.000",
    },
]


def build_record() -> dict:
    return {
        "product_id": "bpjs-kesehatan-jkn",
        "product_name": "Jaminan Kesehatan Nasional (JKN)",
        "insurer_slug": "bpjs-kesehatan",
        "insurer_name": "BPJS Kesehatan",
        "insurer_category": "asuransi_sosial",
        "product_type": "kesehatan_sosial",
        "jenis": "sosial",
        "product_page_url": "https://bpjs-kesehatan.go.id/#/",
        "regulatory_source": REGULATORY_SOURCE,
        "currency": "IDR",
        "coverage_regions": ["Indonesia"],
        "age_entry": {"min_months": 0, "max_years": None, "note": "Wajib untuk seluruh penduduk Indonesia"},
        "coverage_until_age": None,
        "payment_modes": ["bulanan"],
        "plans": PLANS,
        "waiting_periods": {"general_days": 14},
        "exclusions": [
            "Pelayanan kesehatan tanpa melalui prosedur sesuai ketentuan",
            "Pelayanan di fasilitas kesehatan yang tidak bekerja sama dengan BPJS (kecuali kasus gawat darurat)",
            "Pelayanan kesehatan akibat kejadian tidak diharapkan yang dapat dicegah",
            "Pelayanan kesehatan akibat tindak pidana",
            "Pelayanan kesehatan dalam rangka percobaan/eksperimen",
            "Pengobatan kemandulan/infertilitas",
            "Pengobatan dan tindakan untuk meratakan gigi (ortodonsi)",
            "Pelayanan kesehatan dengan tujuan estetika",
            "Pelayanan kesehatan akibat ketergantungan obat dan/atau alkohol",
            "Pelayanan kesehatan akibat cedera atas tujuan menyakiti diri sendiri",
            "Pelayanan komplementer/tradisional yang belum dinyatakan efektif",
        ],
        "claim_procedure": ["cashless"],
        "hospital_network": {
            "name": "Fasilitas Kesehatan Tingkat Pertama (FKTP) + Fasilitas Kesehatan Rujukan Tingkat Lanjutan (FKRTL)",
            "url_or_note": "https://faskes.bpjs-kesehatan.go.id/aplicares/#/app/peta",
        },
        "claim_illustrations": [],
        "scraped_at": datetime.now(UTC).isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit BPJS Kesehatan record (regulatory hardcoded tiers).")
    parser.add_argument("--out-dir", type=Path, default=RAW_DIR)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_json = args.out_dir / "products.json"
    out_json.write_text(json.dumps([build_record()], ensure_ascii=False, indent=2))
    print(f"Wrote {out_json} (1 product, 3 plans)")


if __name__ == "__main__":
    main()
