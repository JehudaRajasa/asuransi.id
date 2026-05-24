const VERSION = 'v0.4 · 2026-05'

export function DisclaimerStrip() {
  return (
    <aside
      role="note"
      aria-label="Disclaimer"
      className="fixed inset-x-0 bottom-0 z-[5] bg-ink-primary text-ink-inverse"
    >
      <div className="mx-auto flex max-w-[1340px] items-center justify-between gap-6 px-6 py-3 font-mono text-[12px] md:gap-8 md:px-20 md:py-3.5">
        <span className="hidden text-[10px] uppercase tracking-[0.08em] text-[#C9C4B8] md:inline">
          Disclaimer
        </span>
        <span className="flex-1">
          asuransi.id adalah alat bantu baca, bukan nasihat keuangan. Dokumen RIPLAY tetap
          diutamakan.
        </span>
        <span className="hidden text-[10px] uppercase tracking-[0.08em] text-[#C9C4B8] opacity-60 md:inline">
          {VERSION}
        </span>
      </div>
    </aside>
  )
}
