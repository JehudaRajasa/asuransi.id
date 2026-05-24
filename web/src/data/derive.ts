import insurersRaw from './normalized/insurers.json'
import policiesRaw from './normalized/policies.json'
import type { BenefitGroup, Insurer, Policy } from '../types/policy'

export const policies = policiesRaw as Policy[]
export const allInsurers = insurersRaw as Insurer[]

const BPJS_SLUG = 'bpjs-kesehatan'

export const BENEFIT_GROUPS: BenefitGroup[] = [
  {
    slug: 'rawat-inap',
    label: 'Rawat inap',
    categories: ['kamar_rs', 'rawat_inap_umum', 'dokter_inpatient', 'icu', 'tindakan_bedah'],
  },
  {
    slug: 'rawat-jalan',
    label: 'Rawat jalan',
    categories: ['rawat_jalan', 'dokter_umum', 'dokter_spesialis', 'telehealth'],
  },
  {
    slug: 'penyakit-kritis',
    label: 'Penyakit kritis',
    categories: ['penyakit_kritis'],
  },
  {
    slug: 'kanker',
    label: 'Kanker',
    categories: ['kanker'],
  },
  {
    slug: 'dental-optical',
    label: 'Dental & optical',
    categories: ['dental', 'optical'],
  },
  {
    slug: 'maternity',
    label: 'Maternity',
    categories: ['maternity'],
  },
]

const BENEFIT_SUBLABELS: Record<string, string> = {
  'rawat-inap': 'kamar, ICU & pembedahan',
  'rawat-jalan': 'kunjungan & resep',
  'penyakit-kritis': 'kondisi terdaftar',
  kanker: 'kemoterapi & radiasi',
  'dental-optical': 'rider opsional',
  maternity: 'persalinan normal & SC',
}

export type InsurerCardData = {
  slug: string
  name: string
  shortName: string
  productCount: number
  isPublic: boolean
}

export type BenefitCardData = {
  slug: string
  label: string
  sublabel: string
  productCount: number
}

const SHORT_NAME_OVERRIDES: Record<string, string> = {
  'aia-financial': 'AIA',
  'allianz-life': 'Allianz',
  'allianz-life-syariah': 'Allianz Syariah',
  'bca-life': 'BCA Life',
  'bni-life': 'BNI Life',
  'bpjs-kesehatan': 'BPJS Kesehatan',
  car: 'CAR',
  generali: 'Generali',
  'jiwa-manulife': 'Manulife',
  'jiwa-manulife-syariah': 'Manulife Syariah',
  'prudential-life-assurance': 'Prudential',
  'prudential-sharia-life-assurance': 'Prudential Syariah',
  sequis: 'Sequis',
  'sun-life': 'Sun Life',
  'zurich-topas': 'Zurich Topas',
}

export function shortName(slug: string, fallback: string): string {
  if (slug in SHORT_NAME_OVERRIDES) return SHORT_NAME_OVERRIDES[slug]
  return fallback.replace(/^PT\.?\s+/, '')
}

export function getInsurerCards(): InsurerCardData[] {
  const productCounts = new Map<string, number>()
  for (const p of policies) {
    productCounts.set(p.insurer_slug, (productCounts.get(p.insurer_slug) ?? 0) + 1)
  }

  const insurerBySlug = new Map(allInsurers.map((i) => [i.slug, i]))
  const cards: InsurerCardData[] = []

  for (const [slug, count] of productCounts) {
    const insurer = insurerBySlug.get(slug)
    const name = insurer?.name ?? slug
    cards.push({
      slug,
      name,
      shortName: shortName(slug, name),
      productCount: count,
      isPublic: slug === BPJS_SLUG,
    })
  }

  return cards.sort((a, b) => {
    if (a.isPublic !== b.isPublic) return a.isPublic ? -1 : 1
    if (b.productCount !== a.productCount) return b.productCount - a.productCount
    return a.shortName.localeCompare(b.shortName, 'id')
  })
}

export function getBenefitCards(): BenefitCardData[] {
  return BENEFIT_GROUPS.map((group) => {
    const categorySet = new Set(group.categories)
    const count = policies.filter((p) =>
      p.plans.some((plan) => plan.manfaat.some((m) => categorySet.has(m.category))),
    ).length
    return {
      slug: group.slug,
      label: group.label,
      sublabel: BENEFIT_SUBLABELS[group.slug] ?? '',
      productCount: count,
    }
  })
}

export type FeaturedProduct = {
  productId: string
  productName: string
  insurerSlug: string
  insurerShortName: string
  jenis: 'konvensional' | 'syariah'
  riplayUrl?: string
  brosurUrl?: string
}

export function getFeaturedProducts(limit = 3): FeaturedProduct[] {
  const insurerOrder = getInsurerCards()
    .filter((c) => !c.isPublic)
    .map((c) => c.slug)

  const seen = new Set<string>()
  const out: FeaturedProduct[] = []

  for (const slug of insurerOrder) {
    if (out.length >= limit) break
    if (seen.has(slug)) continue
    const product = policies.find((p) => p.insurer_slug === slug)
    if (!product) continue
    seen.add(slug)
    out.push({
      productId: product.product_id,
      productName: product.product_name,
      insurerSlug: product.insurer_slug,
      insurerShortName: shortName(product.insurer_slug, product.insurer_name),
      jenis: product.jenis,
      riplayUrl: product.source_pdf_urls?.riplay,
      brosurUrl: product.source_pdf_urls?.brosur,
    })
  }

  return out
}

export const TOTAL_PRODUCTS = policies.length
export const TOTAL_INSURERS = new Set(policies.map((p) => p.insurer_slug)).size

const SCRAPED_DATES = policies
  .map((p) => p.scraped_at)
  .filter(Boolean)
  .sort()
export const LATEST_SCRAPE = SCRAPED_DATES[SCRAPED_DATES.length - 1] ?? null
