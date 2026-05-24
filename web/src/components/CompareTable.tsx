import { Fragment } from 'react'
import type { CompareCellData, CompareMatrix } from '../data/compare'
import { formatUnit, shortName } from '../data/derive'
import { InsurerMark } from './InsurerMark'
import { SourceLink } from './SourceLink'
import { Tag } from './Tag'

const BPJS_SLUG = 'bpjs-kesehatan'

function Cell({ data }: { data: CompareCellData }) {
  if (!data) {
    return (
      <span className="font-mono text-ink-tertiary" aria-label="tidak ada data">
        —
      </span>
    )
  }
  if (data.isNote) {
    return <span className="text-[14px] text-ink-primary">{data.value}</span>
  }
  return (
    <span>
      <span className="font-mono text-[15px] font-medium tnum text-ink-primary">{data.value}</span>
      {data.unit && (
        <span className="ml-1 font-mono text-[11px] text-ink-tertiary">/ {formatUnit(data.unit)}</span>
      )}
    </span>
  )
}

type Props = { matrix: CompareMatrix }

export function CompareTable({ matrix }: Props) {
  const { products, groups, totalRowCount } = matrix
  const groupCount = groups.length
  const colCount = products.length + 1

  return (
    <div className="min-w-0 flex-1 overflow-x-auto pb-16 pt-8 pr-6 md:pr-20">
      <table
        className="w-full border-collapse bg-page"
        style={{ tableLayout: 'fixed' }}
      >
        <thead>
          <tr>
            <th
              scope="col"
              className="sticky left-0 top-0 z-[2] w-[240px] border-b border-ink-primary bg-page py-5 pl-0 pr-4 text-left align-bottom"
            >
              <div className="micro-label">Manfaat</div>
              <div className="mt-1 font-mono text-[11px] text-ink-tertiary">
                {totalRowCount} baris · {groupCount} kategori
              </div>
            </th>
            {products.map((p) => (
              <th
                key={p.product_id}
                scope="col"
                className="sticky top-0 z-[1] border-b border-l border-ink-primary border-l-hairline bg-page p-4 text-left align-bottom"
              >
                <div className="mb-2 flex items-center gap-2">
                  <InsurerMark name={p.insurer_name} slug={p.insurer_slug} size={22} />
                  <span className="text-[13px] text-ink-secondary">{shortName(p.insurer_slug, p.insurer_name)}</span>
                  {p.insurer_slug === BPJS_SLUG && <Tag tone="public">Publik</Tag>}
                </div>
                <div className="mb-1 font-serif text-[18px] font-normal leading-[1.2] text-ink-primary">
                  {p.product_name}
                </div>
                <div className="mt-2 font-mono text-[11px] text-ink-tertiary">
                  {p.jenis === 'syariah' ? 'Syariah' : 'Konvensional'}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {groups.map((grp, gi) => (
            <Fragment key={grp.groupLabel}>
              <tr>
                <td colSpan={colCount} className="pb-2 pt-7">
                  <div className="flex items-baseline gap-4">
                    <span className="font-mono text-[11px] text-ink-tertiary">
                      {String(gi + 1).padStart(2, '0')}
                    </span>
                    <span className="font-serif text-[18px] tracking-[-0.01em] md:text-[20px]">
                      {grp.groupLabel}
                    </span>
                    <div className="h-px flex-1 bg-hairline" />
                    <span className="micro-label">{grp.rows.length} baris</span>
                  </div>
                </td>
              </tr>
              {grp.rows.map((r) => (
                <tr key={r.category} className="border-b border-hairline">
                  <th
                    scope="row"
                    className="sticky left-0 z-[1] bg-page py-4 pl-0 pr-4 text-left align-top font-normal"
                  >
                    <div className="text-[14px] font-medium text-ink-primary">{r.label}</div>
                  </th>
                  {r.cells.map((c, ci) => (
                    <td
                      key={ci}
                      className="border-l border-hairline p-4 align-top"
                    >
                      <Cell data={c} />
                    </td>
                  ))}
                </tr>
              ))}
            </Fragment>
          ))}
        </tbody>
      </table>

      <div className="mt-12 border-t border-ink-primary pt-6">
        <div className="micro-label mb-4">Sumber data</div>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
          {products.map((p) => (
            <div key={p.product_id}>
              <div className="mb-1 text-[13px] font-medium">{p.product_name}</div>
              {p.source_pdf_urls?.riplay ? (
                <SourceLink label="RIPLAY" href={p.source_pdf_urls.riplay} />
              ) : (
                <span className="font-mono text-[12px] text-ink-tertiary">— tanpa dokumen</span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
