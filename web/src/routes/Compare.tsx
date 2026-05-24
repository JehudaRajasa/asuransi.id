import { useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import { CompareTable } from '../components/CompareTable'
import { EmptyState } from '../components/EmptyState'
import { FilterRail } from '../components/FilterRail'
import { buildCompareMatrix } from '../data/compare'
import { getFeaturedProducts } from '../data/derive'

function parseProductIds(raw: string | null): string[] {
  if (!raw) return []
  return raw
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

export function Compare() {
  const [searchParams] = useSearchParams()
  const productIds = useMemo(() => parseProductIds(searchParams.get('products')), [searchParams])

  const fallbackIds = useMemo(() => getFeaturedProducts(3).map((p) => p.productId), [])
  const effectiveIds = productIds.length > 0 ? productIds : fallbackIds

  const matrix = useMemo(() => buildCompareMatrix(effectiveIds), [effectiveIds])

  if (matrix.products.length === 0) {
    return (
      <main>
        <EmptyState
          title="Belum ada produk yang dipilih untuk dibandingkan."
          description="Tambahkan 2–4 produk lewat halaman penyedia atau gunakan saran berikut."
          suggestions={fallbackIds.map((id) => ({
            label: `Bandingkan ${id}`,
            description: 'produk unggulan',
            href: `/compare?products=${id}`,
          }))}
        />
      </main>
    )
  }

  const title = matrix.products.map((p) => p.product_name).join(' · ')

  return (
    <main className="pb-32">
      <section className="border-b border-hairline">
        <div className="mx-auto flex max-w-[1340px] flex-col gap-6 px-6 py-8 md:flex-row md:items-end md:justify-between md:gap-12 md:px-20 md:py-10">
          <div className="min-w-0">
            <div className="micro-label mb-3">
              Bandingkan · {matrix.products.length} produk
            </div>
            <h1 className="m-0 font-serif text-[28px] font-normal leading-[1.1] tracking-[-0.02em] text-ink-primary md:text-[40px]">
              {title}
            </h1>
          </div>
          <div className="flex shrink-0 items-center gap-3">
            <button
              type="button"
              className="font-mono text-[12px] uppercase tracking-[0.08em] text-brand"
            >
              + Tambah produk
            </button>
            <button
              type="button"
              className="inline-flex items-center gap-2 rounded-sm bg-brand px-5 py-3 font-mono text-[12px] uppercase tracking-[0.08em] text-ink-inverse"
            >
              Ekspor PDF
            </button>
          </div>
        </div>
      </section>

      <div className="flex flex-col md:flex-row">
        <FilterRail />
        <CompareTable matrix={matrix} />
      </div>
    </main>
  )
}
