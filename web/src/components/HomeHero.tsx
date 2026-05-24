import { useRef, useState } from 'react'
import { LATEST_SCRAPE, TOTAL_INSURERS, TOTAL_PRODUCTS } from '../data/derive'
import { HeroSearch, type HeroSearchHandle } from './HeroSearch'
import { IntentPillRow } from './IntentPillRow'

const READING_STEPS = [
  'Tanyakan dalam bahasa biasa',
  'Telusuri tabel manfaat',
  'Buka dokumen RIPLAY asli',
  'Bandingkan 2–4 produk',
]

const EXAMPLES = [
  'rawat inap minimal Rp 500rb / hari',
  'kanker tak terbatas',
  'BPJS Kelas I vs Prudential',
  'maternity konvensional',
]

function formatScrapeDate(iso: string | null): string {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })
}

type Props = { onSubmit: (q: string) => void }

export function HomeHero({ onSubmit }: Props) {
  const scrapeLabel = formatScrapeDate(LATEST_SCRAPE)
  const [query, setQuery] = useState('')
  const searchRef = useRef<HeroSearchHandle>(null)

  const handlePick = (q: string) => {
    setQuery(q)
    searchRef.current?.focus()
  }

  return (
    <section className="mx-auto max-w-[1340px] px-6 pb-16 pt-12 md:px-20 md:pb-20 md:pt-24">
      <div className="grid grid-cols-1 items-end gap-16 md:grid-cols-[1fr_360px] md:gap-24">
        <div>
          <div className="mb-6 font-mono text-[12px] tracking-[0.02em] text-ink-secondary">
            Database RIPLAY · {TOTAL_PRODUCTS} produk · {TOTAL_INSURERS} penyedia
            {scrapeLabel && ` · diperbarui ${scrapeLabel}`}
          </div>
          <h1 className="m-0 font-serif text-[44px] font-normal leading-[1.04] tracking-[-0.025em] text-ink-primary md:text-[80px] md:leading-[1.02]">
            Baca polis kesehatan
            <br />
            sebelum kamu beli.
          </h1>
          <p className="mt-6 max-w-[560px] text-[16px] leading-[1.55] text-ink-secondary md:text-[18px]">
            Cari, bandingkan, dan buka dokumen asli setiap produk asuransi
            kesehatan individu di Indonesia. Gratis, tanpa akun, tanpa
            rekomendasi agen.
          </p>
        </div>
        <aside className="border-l border-hairline pl-8">
          <div className="micro-label mb-3">Cara membaca</div>
          <ol className="m-0 list-none p-0 font-mono text-[12px] leading-[1.7] text-ink-secondary">
            {READING_STEPS.map((s, i) => (
              <li
                key={s}
                className={`grid grid-cols-[32px_1fr] border-b border-hairline py-2 ${
                  i === 0 ? 'border-t' : ''
                }`}
              >
                <span className="text-ink-tertiary">0{i + 1}</span>
                <span className="text-ink-primary">{s}</span>
              </li>
            ))}
          </ol>
        </aside>
      </div>

      <div className="mt-16 md:mt-20">
        <HeroSearch ref={searchRef} value={query} onChange={setQuery} onSubmit={onSubmit} />
        <div className="mt-5">
          <IntentPillRow examples={EXAMPLES} onPick={handlePick} />
        </div>
      </div>
    </section>
  )
}
