import { useMemo } from 'react'
import { Link, useParams } from 'react-router-dom'
import { SourceLink } from '../components/SourceLink'
import { Tag } from '../components/Tag'
import { BENEFIT_GROUPS, getBenefitCards, shortName } from '../data/derive'
import { getProductsByBenefitGroup } from '../data/compare'

export function ManfaatSlug() {
  const { slug = '' } = useParams<{ slug: string }>()

  const group = useMemo(() => BENEFIT_GROUPS.find((g) => g.slug === slug), [slug])
  const card = useMemo(() => getBenefitCards().find((c) => c.slug === slug), [slug])
  const products = useMemo(
    () => (group ? getProductsByBenefitGroup(group.categories) : []),
    [group],
  )

  if (!group || !card) {
    return (
      <main className="mx-auto max-w-[720px] px-6 py-20 md:px-20">
        <div className="micro-label mb-6">Tidak ditemukan</div>
        <h1 className="m-0 font-serif text-[32px] font-normal leading-[1.1] tracking-[-0.02em] text-ink-primary">
          Kategori manfaat <span className="font-mono">{slug}</span> tidak ada.
        </h1>
        <p className="mt-6">
          <Link to="/manfaat" className="text-brand underline">
            Lihat semua kategori
          </Link>
        </p>
      </main>
    )
  }

  return (
    <main className="pb-32">
      <section className="mx-auto max-w-[1180px] px-6 pb-10 pt-12 md:px-20 md:pt-16">
        <div className="micro-label mb-5 text-ink-tertiary">
          <Link to="/" className="no-underline hover:underline">Beranda</Link>{' '}
          / <Link to="/manfaat" className="no-underline hover:underline">Manfaat</Link>{' '}
          / {card.label}
        </div>
        <h1 className="m-0 font-serif text-[36px] font-normal leading-[1.05] tracking-[-0.025em] text-ink-primary md:text-[56px]">
          {card.label}
        </h1>
        <p className="mt-4 max-w-[600px] text-[16px] leading-[1.55] text-ink-secondary">
          {card.sublabel}
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          <Tag>{card.productCount} produk menanggung</Tag>
          <Tag>{group.categories.length} sub-kategori</Tag>
        </div>
      </section>

      <section className="mx-auto max-w-[1180px] px-6 md:px-20">
        <div className="mb-6 flex items-baseline justify-between border-b border-ink-primary pb-4">
          <h2 className="m-0 font-serif text-[24px] font-normal md:text-[32px]">Produk</h2>
          <span className="micro-label">{products.length} produk</span>
        </div>
        <ul className="flex list-none flex-col border-t border-hairline p-0">
          {products.map((p) => (
            <li key={p.product_id} className="contents">
              <Link
                to={`/produk/${p.product_id}`}
                className="grid grid-cols-1 gap-3 border-b border-hairline py-5 text-ink-primary no-underline hover:bg-brand-soft/30 md:grid-cols-[1fr_auto_auto] md:items-center md:gap-6"
              >
                <div>
                  <div className="font-mono text-[11px] uppercase tracking-[0.06em] text-ink-tertiary">
                    {shortName(p.insurer_slug, p.insurer_name)}
                  </div>
                  <div className="mt-1 font-serif text-[20px] md:text-[22px]">
                    {p.product_name}
                  </div>
                </div>
                <div className="flex gap-2">
                  <Tag>{p.jenis === 'syariah' ? 'Syariah' : 'Konvensional'}</Tag>
                  <Tag>{p.plans.length} plan</Tag>
                </div>
                {p.source_pdf_urls?.riplay && (
                  <SourceLink label="RIPLAY" href={p.source_pdf_urls.riplay} />
                )}
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}
