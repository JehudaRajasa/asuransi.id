import parseFailuresRaw from './normalized/parse_failures.json'
import { policies } from './derive'
import { COMPARE_GROUPS, categoryLabel } from './categoryLabels'
import type { Manfaat, Plan, Policy } from '../types/policy'

type ParseFailure = {
  product_id: string
  tables_path: string
  reason: string
  unmapped_count: number
  unmapped_samples: { label: string; penjelasan: string; row: string[] }[]
}

const parseFailures = parseFailuresRaw as ParseFailure[]

export function getPolicy(productId: string): Policy | undefined {
  return policies.find((p) => p.product_id === productId)
}

export function getParseFailure(productId: string): ParseFailure | undefined {
  return parseFailures.find((f) => f.product_id === productId)
}

export type PlanManfaatGroup = {
  groupLabel: string
  items: { category: string; label: string; manfaat: Manfaat }[]
}

export function groupPlanManfaat(plan: Plan): PlanManfaatGroup[] {
  const seen = new Set<string>()
  const groups: PlanManfaatGroup[] = []

  for (const group of COMPARE_GROUPS) {
    const items: PlanManfaatGroup['items'] = []
    for (const cat of group.categories) {
      const m = plan.manfaat.find((x) => x.category === cat)
      if (!m) continue
      seen.add(cat)
      items.push({ category: cat, label: categoryLabel(cat), manfaat: m })
    }
    if (items.length === 0) continue
    groups.push({ groupLabel: group.label, items })
  }

  const leftover = plan.manfaat.filter((m) => !seen.has(m.category))
  if (leftover.length > 0) {
    groups.push({
      groupLabel: 'Lainnya',
      items: leftover.map((m) => ({
        category: m.category,
        label: categoryLabel(m.category),
        manfaat: m,
      })),
    })
  }

  return groups
}

export function totalManfaatCount(policy: Policy): number {
  const cats = new Set<string>()
  for (const plan of policy.plans) {
    for (const m of plan.manfaat) cats.add(m.category)
  }
  return cats.size
}
