import { BrowseInsurers } from '../components/BrowseInsurers'

export function Penyedia() {
  return (
    <main className="pb-32">
      <section className="mx-auto max-w-[1340px] px-6 pt-12 md:px-20 md:pt-16">
        <div className="micro-label mb-3">Penyedia</div>
        <h1 className="m-0 font-serif text-[32px] font-normal leading-[1.1] tracking-[-0.025em] text-ink-primary md:text-[48px]">
          15 penyedia asuransi kesehatan
          <br />
          individu di Indonesia.
        </h1>
        <p className="mt-4 max-w-[600px] text-[16px] leading-[1.55] text-ink-secondary">
          Setiap penyedia diperbarui dari RIPLAY resmi yang dipublikasikan di
          situs masing-masing. BPJS Kesehatan disertakan sebagai baseline publik.
        </p>
      </section>
      <BrowseInsurers />
    </main>
  )
}
