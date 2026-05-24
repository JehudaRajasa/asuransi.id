export const CATEGORY_LABELS: Record<string, string> = {
  kamar_rs: 'Biaya kamar & akomodasi',
  rawat_inap_umum: 'Rawat inap umum',
  dokter_inpatient: 'Kunjungan dokter di RS',
  icu: 'Perawatan ICU',
  tindakan_bedah: 'Pembedahan',
  obat_inpatient: 'Obat selama rawat inap',
  diagnostik_inpatient: 'Diagnostik selama rawat inap',
  ambulans: 'Ambulans',
  akomodasi_pendamping: 'Akomodasi pendamping',
  gawat_darurat: 'Gawat darurat',
  pre_hospitalization: 'Sebelum rawat inap',
  post_hospitalization: 'Setelah rawat inap',
  perawatan_di_rumah: 'Perawatan di rumah',

  rawat_jalan: 'Rawat jalan',
  dokter_umum: 'Kunjungan dokter umum',
  dokter_spesialis: 'Kunjungan dokter spesialis',
  telehealth: 'Telehealth',
  second_opinion: 'Pendapat kedua',
  preventive: 'Pemeriksaan pencegahan',

  penyakit_kritis: 'Penyakit kritis',
  kanker: 'Kanker',
  dialisis: 'Dialisis',
  hiv_aids: 'HIV/AIDS',

  dental: 'Rawat gigi',
  optical: 'Kacamata & lensa',
  maternity: 'Persalinan',

  annual_limit: 'Plafon tahunan',
  deductible: 'Risiko sendiri (deductible)',
  limit_booster: 'Penambah plafon',
  santunan_harian: 'Santunan harian',
  kesehatan_mental: 'Kesehatan mental',
  rehabilitasi: 'Rehabilitasi',
  prostesis_implan: 'Prostesis & implan',
  alat_medis: 'Alat medis',
  pemakaman: 'Santunan pemakaman',
  pengobatan_tradisional: 'Pengobatan tradisional',
  infeksi_tropis: 'Infeksi tropis',
}

export type CategoryGroup = {
  label: string
  categories: string[]
}

export const COMPARE_GROUPS: CategoryGroup[] = [
  {
    label: 'Rawat inap',
    categories: [
      'kamar_rs',
      'rawat_inap_umum',
      'icu',
      'dokter_inpatient',
      'tindakan_bedah',
      'obat_inpatient',
      'diagnostik_inpatient',
      'ambulans',
      'gawat_darurat',
      'pre_hospitalization',
      'post_hospitalization',
      'perawatan_di_rumah',
      'akomodasi_pendamping',
    ],
  },
  {
    label: 'Rawat jalan',
    categories: [
      'rawat_jalan',
      'dokter_umum',
      'dokter_spesialis',
      'telehealth',
      'second_opinion',
      'preventive',
    ],
  },
  {
    label: 'Penyakit kritis & kanker',
    categories: ['penyakit_kritis', 'kanker', 'dialisis', 'hiv_aids'],
  },
  {
    label: 'Dental, optical & maternity',
    categories: ['dental', 'optical', 'maternity'],
  },
  {
    label: 'Ketentuan & lainnya',
    categories: [
      'annual_limit',
      'deductible',
      'limit_booster',
      'santunan_harian',
      'kesehatan_mental',
      'rehabilitasi',
      'prostesis_implan',
      'alat_medis',
      'pemakaman',
      'pengobatan_tradisional',
      'infeksi_tropis',
    ],
  },
]

export function categoryLabel(cat: string): string {
  return CATEGORY_LABELS[cat] ?? cat
}
