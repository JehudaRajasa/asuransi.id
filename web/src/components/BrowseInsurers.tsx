import { Link } from 'react-router-dom'
import { getInsurerCards, TOTAL_PRODUCTS } from '../data/derive'
import { InsurerMark } from './InsurerMark'
import { Tag } from './Tag'

export function BrowseInsurers() {
  const cards = getInsurerCards()

  return (
    <section
      aria-labelledby="penyedia-heading"
      className="mx-auto mt-16 max-w-[1340px] px-6 md:mt-20 md:px-20"
    >
      <div className="mb-6 flex items-baseline justify-between gap-4 border-b border-ink-primary pb-4">
        <h2
          id="penyedia-heading"
          className="m-0 font-serif text-[24px] font-normal text-ink-primary md:text-[32px]"
        >
          Telusuri menurut penyedia
        </h2>
        <span className="micro-label">
          {cards.length} penyedia · {TOTAL_PRODUCTS} produk
        </span>
      </div>

      <ul className="grid list-none grid-cols-2 border-l border-t border-hairline p-0 md:grid-cols-3 lg:grid-cols-4">
        {cards.map((c) => (
          <li key={c.slug} className="contents">
            <Link
              to={`/penyedia/${c.slug}`}
              className="flex flex-col gap-4 border-b border-r border-hairline bg-page px-6 py-8 text-ink-primary no-underline transition-colors hover:bg-brand-soft/30"
            >
              <div className="flex items-center justify-between">
                <InsurerMark name={c.shortName} slug={c.slug} size={36} />
                <Tag tone={c.isPublic ? 'public' : 'default'}>
                  {c.isPublic ? 'Publik' : 'Swasta'}
                </Tag>
              </div>
              <div>
                <div className="font-serif text-[20px] leading-[1.2] md:text-[22px]">
                  {c.shortName}
                </div>
                <div className="mt-1.5 font-mono text-[11px] tracking-[0.06em] text-ink-tertiary">
                  {String(c.productCount).padStart(2, '0')} produk
                </div>
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}
