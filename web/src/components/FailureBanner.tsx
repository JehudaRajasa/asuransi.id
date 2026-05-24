import { SourceLink } from './SourceLink'

type Props = {
  riplayUrl?: string
  brosurUrl?: string
  reason?: string
}

const DEFAULT_REASON =
  'Tabel manfaat produk ini belum dapat kami baca otomatis. Format dokumen menggunakan kolom bergabung yang masih kami pelajari. Buka dokumen sumber untuk membaca sendiri:'

export function FailureBanner({ riplayUrl, brosurUrl, reason = DEFAULT_REASON }: Props) {
  return (
    <div
      role="status"
      className="grid grid-cols-1 items-start gap-5 rounded-sm border border-warning bg-warning-soft px-6 py-5 md:grid-cols-[auto_1fr_auto] md:px-7 md:py-6"
    >
      <div className="inline-block whitespace-nowrap border border-warning px-2 py-1 font-mono text-[10px] uppercase tracking-[0.1em] text-warning">
        Belum dapat dibaca
      </div>
      <div>
        <p className="m-0 mb-2 text-[15px] leading-[1.55] text-ink-primary">{reason}</p>
        <div className="mt-3 flex flex-wrap gap-6">
          {riplayUrl && <SourceLink label="Buka RIPLAY" href={riplayUrl} />}
          {brosurUrl && <SourceLink label="Buka brosur" href={brosurUrl} />}
        </div>
      </div>
      <div className="hidden max-w-[200px] text-right font-mono text-[11px] leading-[1.6] text-ink-secondary md:block">
        Kuning, bukan merah.
        <br />
        Gagal baca bukan gagal produk.
      </div>
    </div>
  )
}
