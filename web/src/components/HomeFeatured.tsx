import { Link } from 'react-router-dom'
import { getFeaturedProducts } from '../data/derive'
import { InsurerMark } from './InsurerMark'
import { SourceLink } from './SourceLink'
import { Tag } from './Tag'

export function HomeFeatured() {
  const products = getFeaturedProducts(3)
  if (products.length === 0) return null

  return (
    <section
      aria-labelledby="featured-heading"
      className="mx-auto mt-16 max-w-[1340px] px-6 md:mt-20 md:px-20"
    >
      <div className="mb-6 flex items-baseline justify-between gap-4 border-b border-ink-primary pb-4">
        <h2
          id="featured-heading"
          className="m-0 font-serif text-[24px] font-normal text-ink-primary md:text-[32px]"
        >
          Mulai dari produk ini
        </h2>
        <Link
          to="/penyedia"
          className="micro-label text-brand no-underline hover:underline"
          style={{ color: 'var(--color-brand)' }}
        >
          LIHAT SEMUA →
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
        {products.map((p) => (
          <article
            key={p.productId}
            className="flex flex-col gap-5 rounded-[4px] bg-surface p-6 shadow-card"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <InsurerMark name={p.insurerShortName} slug={p.insurerSlug} size={24} />
                <span className="text-[13px] text-ink-secondary">{p.insurerShortName}</span>
              </div>
              <Tag>{p.jenis === 'syariah' ? 'Syariah' : 'Konvensional'}</Tag>
            </div>
            <div>
              <Link
                to={`/produk/${p.productId}`}
                className="font-serif text-[20px] leading-[1.25] text-ink-primary no-underline hover:underline"
              >
                {p.productName}
              </Link>
            </div>
            <div className="border-t border-hairline pt-4">
              <div className="micro-label mb-1.5">Dokumen sumber</div>
              <div className="flex flex-col gap-2">
                {p.riplayUrl && <SourceLink label="RIPLAY" href={p.riplayUrl} />}
                {p.brosurUrl && <SourceLink label="Brosur" href={p.brosurUrl} />}
              </div>
            </div>
            <div className="mt-auto flex items-center justify-between">
              <Link
                to={`/produk/${p.productId}`}
                className="font-mono text-[12px] uppercase tracking-[0.08em] text-brand no-underline hover:underline"
              >
                Buka detail →
              </Link>
              <Link
                to={`/compare?products=${p.productId}`}
                className="font-mono text-[12px] uppercase tracking-[0.08em] text-ink-secondary no-underline hover:text-ink-primary"
              >
                + Bandingkan
              </Link>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
