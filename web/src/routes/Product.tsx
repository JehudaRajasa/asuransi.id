import { useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { FailureBanner } from '../components/FailureBanner'
import { InsurerMark } from '../components/InsurerMark'
import { SourceLink } from '../components/SourceLink'
import { Tag } from '../components/Tag'
import { formatUnit, shortName } from '../data/derive'
import {
  getParseFailure,
  getPolicy,
  groupPlanManfaat,
  totalManfaatCount,
} from '../data/productDetail'

const BPJS_SLUG = 'bpjs-kesehatan'

function NotFound({ slug }: { slug: string }) {
  return (
    <main className="mx-auto max-w-[720px] px-6 py-20 md:px-20">
      <div className="micro-label mb-6">Tidak ditemukan</div>
      <h1 className="m-0 font-serif text-[32px] font-normal leading-[1.1] tracking-[-0.02em] text-ink-primary md:text-[40px]">
        Produk dengan id <span className="font-mono text-[26px]">{slug}</span> tidak ada di
        database.
      </h1>
      <p className="mt-6 text-[16px] text-ink-secondary">
        Cek halaman <Link to="/penyedia" className="text-brand underline">daftar penyedia</Link> atau{' '}
        <Link to="/" className="text-brand underline">kembali ke beranda</Link>.
      </p>
    </main>
  )
}

export function Product() {
  const { slug } = useParams<{ slug: string }>()
  const policy = useMemo(() => (slug ? getPolicy(slug) : undefined), [slug])
  const failure = useMemo(() => (slug ? getParseFailure(slug) : undefined), [slug])

  const [activePlanIdx, setActivePlanIdx] = useState(0)

  if (!policy) return <NotFound slug={slug ?? '?'} />

  const insurerShort = shortName(policy.insurer_slug, policy.insurer_name)
  const activePlan = policy.plans[activePlanIdx] ?? policy.plans[0]
  const groups = activePlan ? groupPlanManfaat(activePlan) : []
  const stats: [string, string, string][] = [
    ['Penyedia', insurerShort, policy.insurer_slug === BPJS_SLUG ? 'Publik' : 'Swasta'],
    ['Jumlah plan', String(policy.plans.length), 'pilihan tingkatan'],
    ['Kategori manfaat', String(totalManfaatCount(policy)), 'di seluruh plan'],
    ['Jenis', policy.jenis === 'syariah' ? 'Syariah' : 'Konvensional', 'sesuai akad'],
  ]

  return (
    <main className="pb-32">
      <section className="mx-auto max-w-[1180px] px-6 pb-8 pt-12 md:px-20 md:pb-10 md:pt-14">
        <div className="micro-label mb-5 text-ink-tertiary">
          <Link to="/" className="no-underline hover:underline">Beranda</Link>{' '}
          /{' '}
          <Link to={`/penyedia/${policy.insurer_slug}`} className="no-underline hover:underline">
            {insurerShort}
          </Link>{' '}
          / {policy.product_name}
        </div>

        <div className="grid grid-cols-1 items-end gap-12 md:grid-cols-[1fr_320px] md:gap-16">
          <div>
            <div className="mb-6 flex items-center gap-3">
              <InsurerMark name={insurerShort} slug={policy.insurer_slug} size={44} />
              <div>
                <div className="text-[13px] text-ink-secondary">{insurerShort}</div>
                <div className="font-mono text-[11px] text-ink-tertiary">
                  {policy.product_type.replace(/_/g, ' ')} ·{' '}
                  {policy.jenis === 'syariah' ? 'Syariah' : 'Konvensional'}
                </div>
              </div>
            </div>
            <h1 className="m-0 font-serif text-[36px] font-normal leading-[1.05] tracking-[-0.025em] text-ink-primary md:text-[56px]">
              {policy.product_name}
            </h1>
            <div className="mt-5 flex flex-wrap gap-2">
              {policy.jenis === 'syariah' ? <Tag>Syariah</Tag> : <Tag>Konvensional</Tag>}
              {policy.insurer_slug === BPJS_SLUG && <Tag tone="public">Publik</Tag>}
              <Tag>
                {policy.plans.length} {policy.plans.length === 1 ? 'plan' : 'plan'}
              </Tag>
            </div>
          </div>

          <aside className="border-t border-ink-primary pt-4">
            <div className="micro-label mb-2">Dokumen sumber</div>
            <div className="mb-4 flex flex-col gap-2">
              {policy.source_pdf_urls?.riplay && (
                <SourceLink label="Buka RIPLAY" href={policy.source_pdf_urls.riplay} />
              )}
              {policy.source_pdf_urls?.brosur && (
                <SourceLink label="Buka brosur produk" href={policy.source_pdf_urls.brosur} />
              )}
            </div>
            <div className="font-mono text-[11px] leading-[1.6] text-ink-tertiary">
              Setiap nilai di halaman ini diambil dari sel di RIPLAY. Dokumen
              sumber tetap diutamakan.
            </div>
          </aside>
        </div>

        <div className="mt-10 flex flex-wrap gap-3">
          <Link
            to={`/compare?products=${policy.product_id}`}
            className="inline-flex items-center gap-2 rounded-sm bg-brand px-5 py-3 font-mono text-[12px] uppercase tracking-[0.08em] text-ink-inverse no-underline"
          >
            + Bandingkan dengan…
          </Link>
        </div>
      </section>

      <section className="mx-auto max-w-[1180px] px-6 md:px-20">
        <div className="grid grid-cols-2 border-y border-ink-primary md:grid-cols-4">
          {stats.map(([k, v, n], i) => (
            <div
              key={k}
              className={`p-6 ${i === 0 ? '' : 'border-l border-hairline'} ${
                i >= 2 ? 'border-t md:border-t-0' : ''
              }`}
            >
              <div className="micro-label mb-2">{k}</div>
              <div className="font-mono text-[20px] tracking-[-0.01em] tnum text-ink-primary md:text-[22px]">
                {v}
              </div>
              <div className="mt-1 text-[13px] text-ink-secondary">{n}</div>
            </div>
          ))}
        </div>
      </section>

      {failure && (
        <section className="mx-auto mt-12 max-w-[1180px] px-6 md:px-20">
          <FailureBanner
            riplayUrl={policy.source_pdf_urls?.riplay}
            brosurUrl={policy.source_pdf_urls?.brosur}
            reason={`${failure.unmapped_count} baris dari RIPLAY belum dapat kami petakan ke tabel manfaat (${failure.reason}). Sisanya tetap kami tampilkan di bawah.`}
          />
        </section>
      )}

      <section className="mx-auto mt-16 max-w-[1180px] px-6 md:px-20">
        <div className="mb-2 flex items-baseline justify-between border-b border-ink-primary pb-4">
          <h2 className="m-0 font-serif text-[24px] font-normal text-ink-primary md:text-[32px]">
            Tabel manfaat
          </h2>
          <span className="micro-label">Diparse dari RIPLAY</span>
        </div>

        {policy.plans.length > 1 && (
          <div className="mt-6 flex flex-wrap gap-2">
            {policy.plans.map((pl, i) => (
              <button
                key={pl.plan_name}
                type="button"
                onClick={() => setActivePlanIdx(i)}
                className={`rounded-sm border px-3 py-1.5 font-mono text-[12px] uppercase tracking-[0.06em] ${
                  i === activePlanIdx
                    ? 'border-ink-primary bg-ink-primary text-ink-inverse'
                    : 'border-hairline text-ink-secondary hover:border-brand hover:text-brand'
                }`}
              >
                {pl.plan_name}
              </button>
            ))}
          </div>
        )}

        {groups.length === 0 && (
          <p className="mt-10 text-[15px] text-ink-secondary">
            Tabel manfaat plan ini belum tersedia. Buka dokumen sumber di atas.
          </p>
        )}

        {groups.map((g, gi) => (
          <div key={g.groupLabel}>
            <div className="flex items-baseline gap-4 py-7 pb-3">
              <span className="font-mono text-[11px] text-ink-tertiary">
                {String(gi + 1).padStart(2, '0')}
              </span>
              <span className="font-serif text-[20px] md:text-[22px]">{g.groupLabel}</span>
              <div className="h-px flex-1 bg-hairline" />
              <span className="micro-label">{g.items.length} item</span>
            </div>
            <table className="w-full border-collapse">
              <tbody>
                {g.items.map((it) => (
                  <tr key={it.category} className="border-b border-hairline">
                    <td className="w-[40%] py-3.5 pr-4 text-[14px] align-top">
                      <div>{it.label}</div>
                      {it.manfaat.raw_label && it.manfaat.raw_label !== it.label && (
                        <div className="mt-1 font-mono text-[11px] text-ink-tertiary">
                          {it.manfaat.raw_label}
                        </div>
                      )}
                    </td>
                    <td className="w-[30%] py-3.5 px-4 text-right">
                      {it.manfaat.raw_cell ? (
                        <span className="font-mono text-[15px] font-medium tnum">
                          {/[0-9]/.test(it.manfaat.raw_cell) ? `Rp ${it.manfaat.raw_cell}` : it.manfaat.raw_cell}
                        </span>
                      ) : (
                        <span className="font-mono text-ink-tertiary">—</span>
                      )}
                    </td>
                    <td className="py-3.5 pl-4 text-[13px] text-ink-secondary">
                      {formatUnit(it.manfaat.unit)}
                      {it.manfaat.note ? ` · ${it.manfaat.note}` : ''}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </section>

      <div className="h-32" aria-hidden="true" />
    </main>
  )
}
