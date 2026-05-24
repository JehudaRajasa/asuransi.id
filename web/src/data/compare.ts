import type { Manfaat, Policy } from '../types/policy'
import { COMPARE_GROUPS, categoryLabel } from './categoryLabels'
import { policies } from './derive'

export type CompareCellData = {
  value: string
  unit: string | null
  isNote: boolean
  rawLabel: string | null
} | null

export type CompareRow = {
  category: string
  label: string
  cells: CompareCellData[]
}

export type CompareGroupRow = {
  groupLabel: string
  rows: CompareRow[]
}

export type CompareMatrix = {
  products: Policy[]
  groups: CompareGroupRow[]
  totalRowCount: number
}

function pickPrimaryPlan(policy: Policy) {
  return policy.plans[0] ?? null
}

function cellFromManfaat(m: Manfaat): CompareCellData {
  if (!m.raw_cell || m.raw_cell.trim() === '') {
    return null
  }

  const looksNumeric = /[0-9]/.test(m.raw_cell)
  return {
    value: looksNumeric ? `Rp ${m.raw_cell}` : m.raw_cell,
    unit: m.unit,
    isNote: !looksNumeric,
    rawLabel: m.raw_label,
  }
}

function findManfaat(policy: Policy, category: string): Manfaat | null {
  const plan = pickPrimaryPlan(policy)
  if (!plan) return null
  return plan.manfaat.find((m) => m.category === category) ?? null
}

export function buildCompareMatrix(productIds: string[]): CompareMatrix {
  const products = productIds
    .map((id) => policies.find((p) => p.product_id === id))
    .filter((p): p is Policy => p !== undefined)

  const groups: CompareGroupRow[] = []
  let totalRowCount = 0

  for (const group of COMPARE_GROUPS) {
    const rows: CompareRow[] = []
    for (const cat of group.categories) {
      const cells: CompareCellData[] = products.map((p) => {
        const m = findManfaat(p, cat)
        return m ? cellFromManfaat(m) : null
      })
      const hasAny = cells.some((c) => c !== null)
      if (!hasAny) continue
      rows.push({ category: cat, label: categoryLabel(cat), cells })
    }
    if (rows.length === 0) continue
    groups.push({ groupLabel: group.label, rows })
    totalRowCount += rows.length
  }

  return { products, groups, totalRowCount }
}

export function getProductsByCategory(category: string): Policy[] {
  return policies.filter((p) =>
    p.plans.some((plan) => plan.manfaat.some((m) => m.category === category)),
  )
}

export function getProductsByBenefitGroup(categories: string[]): Policy[] {
  const set = new Set(categories)
  return policies.filter((p) =>
    p.plans.some((plan) => plan.manfaat.some((m) => set.has(m.category))),
  )
}
