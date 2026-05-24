export type Manfaat = {
  category: string
  amount_rp: number | null
  unit: string | null
  note: string | null
  raw_cell: string | null
  raw_label: string | null
  penjelasan: string | null
}

export type Plan = {
  plan_name: string
  manfaat: Manfaat[]
}

export type Policy = {
  product_id: string
  product_name: string
  insurer_slug: string
  insurer_name: string
  insurer_category: string
  product_type: string
  jenis: 'konvensional' | 'syariah'
  product_page_url: string | null
  source_pdfs: { riplay?: string; brosur?: string }
  source_pdf_urls: { riplay?: string; brosur?: string }
  scraped_at: string
  currency: string
  plans: Plan[]
}

export type Insurer = {
  category: string
  source_quarter: string
  name: string
  jenis_perusahaan: string
  jenis_kantor: string
  license_no: string
  license_date: string
  address: string
  city: string
  postal_code: string
  phone: string
  email: string
  website: string
  slug: string
}

export type BenefitGroup = {
  slug: string
  label: string
  categories: string[]
}
