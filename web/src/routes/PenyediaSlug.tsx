import { useMemo } from 'react'
import { Link, useParams } from 'react-router-dom'
import { InsurerMark } from '../components/InsurerMark'
import { SourceLink } from '../components/SourceLink'
import { Tag } from '../components/Tag'
import { allInsurers, getInsurerCards, policies } from '../data/derive'

export function PenyediaSlug() {
  const { slug = '' } = useParams<{ slug: string }>()

  const insurer = useMemo(() => allInsurers.find((i) => i.slug === slug), [slug])
  const card = useMemo(() => getInsurerCards().find((c) => c.slug === slug), [slug])
  const products = useMemo(() => policies.filter((p) => p.insurer_slug === slug), [slug])

  if (!insurer || !card) {
    return (
      <main className="mx-auto max-w-[720px] px-6 py-20 md:px-20">
        <div className="micro-label mb-6">Tidak ditemukan</div>
        <h1 className="m-0 font-serif text-[32px] font-normal leading-[1.1] tracking-[-0.02em] text-ink-primary">
          Penyedia <span className="font-mono">{slug}</span> tidak ada.
        </h1>
        <p className="mt-6">
          <Link to="/penyedia" className="text-brand underline">
            Lihat semua penyedia
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
          / <Link to="/penyedia" className="no-underline hover:underline">Penyedia</Link>{' '}
          / {card.shortName}
        </div>
        <div className="mb-6 flex items-center gap-3">
          <InsurerMark name={card.shortName} slug={card.slug} size={48} />
          <div>
            <div className="text-[13px] text-ink-secondary">{insurer.name}</div>
            <div className="font-mono text-[11px] text-ink-tertiary">
              {insurer.city} · {insurer.jenis_perusahaan.replace(/_/g, ' ')}
            </div>
          </div>
        </div>
        <h1 className="m-0 font-serif text-[36px] font-normal leading-[1.05] tracking-[-0.025em] text-ink-primary md:text-[56px]">
          {card.shortName}
        </h1>
        <div className="mt-4 flex flex-wrap gap-2">
          <Tag tone={card.isPublic ? 'public' : 'default'}>
            {card.isPublic ? 'Publik' : 'Swasta'}
          </Tag>
          <Tag>{card.productCount} produk</Tag>
        </div>
      </section>

      <section className="mx-auto max-w-[1180px] px-6 md:px-20">
        <div className="mb-6 flex items-baseline justify-between border-b border-ink-primary pb-4">
          <h2 className="m-0 font-serif text-[24px] font-normal md:text-[32px]">Produk</h2>
          <span className="micro-label">{products.length} produk</span>
        </div>
        <ul className="grid list-none grid-cols-1 border-l border-t border-hairline p-0 md:grid-cols-2">
          {products.map((p) => (
            <li key={p.product_id} className="contents">
              <Link
                to={`/produk/${p.product_id}`}
                className="flex flex-col gap-3 border-b border-r border-hairline p-6 text-ink-primary no-underline hover:bg-brand-soft/30 md:p-8"
              >
                <div className="font-mono text-[11px] uppercase tracking-[0.06em] text-ink-tertiary">
                  {p.jenis === 'syariah' ? 'Syariah' : 'Konvensional'} · {p.plans.length} plan
                </div>
                <div className="font-serif text-[22px] leading-[1.2] md:text-[26px]">
                  {p.product_name}
                </div>
                <div className="mt-auto flex flex-wrap gap-4 border-t border-hairline pt-4">
                  {p.source_pdf_urls?.riplay && (
                    <SourceLink label="RIPLAY" href={p.source_pdf_urls.riplay} />
                  )}
                  {p.source_pdf_urls?.brosur && (
                    <SourceLink label="Brosur" href={p.source_pdf_urls.brosur} />
                  )}
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}
