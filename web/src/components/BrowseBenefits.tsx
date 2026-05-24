import { Link } from 'react-router-dom'
import { getBenefitCards } from '../data/derive'

export function BrowseBenefits() {
  const cards = getBenefitCards()

  return (
    <section
      aria-labelledby="manfaat-heading"
      className="mx-auto mt-16 max-w-[1340px] px-6 md:mt-20 md:px-20"
    >
      <div className="mb-6 flex items-baseline justify-between gap-4 border-b border-ink-primary pb-4">
        <h2
          id="manfaat-heading"
          className="m-0 font-serif text-[24px] font-normal text-ink-primary md:text-[32px]"
        >
          Telusuri menurut manfaat
        </h2>
        <span className="micro-label">{cards.length} kategori</span>
      </div>

      <ul className="grid list-none grid-cols-1 border-l border-t border-hairline p-0 md:grid-cols-3">
        {cards.map((c) => (
          <li key={c.slug} className="contents">
            <Link
              to={`/manfaat/${c.slug}`}
              className="flex flex-col gap-3 border-b border-r border-hairline p-8 text-ink-primary no-underline transition-colors hover:bg-brand-soft/30"
            >
              <div className="font-serif text-[24px] leading-[1.15] md:text-[26px]">{c.label}</div>
              <div className="text-[13px] text-ink-secondary">{c.sublabel}</div>
              <div className="mt-auto flex items-end justify-between border-t border-hairline pt-6">
                <div>
                  <div className="micro-label mb-1">Produk tersedia</div>
                  <div className="font-mono text-[13px] tnum text-ink-primary">
                    {c.productCount} dari 37
                  </div>
                </div>
                <div className="font-mono text-[11px] text-ink-tertiary">→</div>
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
