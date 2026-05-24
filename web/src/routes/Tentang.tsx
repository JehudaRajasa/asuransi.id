import { Link } from 'react-router-dom'
import { TOTAL_INSURERS, TOTAL_PRODUCTS } from '../data/derive'

export function Tentang() {
  return (
    <main className="mx-auto max-w-[720px] px-6 pb-32 pt-12 md:px-20 md:pt-16">
      <div className="micro-label mb-5">Tentang</div>
      <h1 className="m-0 font-serif text-[36px] font-normal leading-[1.05] tracking-[-0.025em] text-ink-primary md:text-[48px]">
        Apa itu asuransi.id?
      </h1>

      <p className="mt-8 text-[18px] leading-[1.55] text-ink-secondary">
        Situs publik gratis untuk membaca polis asuransi kesehatan individu di
        Indonesia. Setiap penyedia menerbitkan{' '}
        <strong className="font-medium text-ink-primary">RIPLAY</strong> — dokumen
        regulator 30–100 halaman — untuk setiap produk konsumen. Kami parse
        RIPLAY, normalkan tabel manfaatnya, dan sajikan sehingga bisa dibaca dan
        dibandingkan.
      </p>

      <div className="mt-12 grid grid-cols-3 border-y border-ink-primary">
        {[
          ['Produk', TOTAL_PRODUCTS],
          ['Penyedia', TOTAL_INSURERS],
          ['Versi', 'v0.4'],
        ].map(([k, v], i) => (
          <div key={String(k)} className={`p-5 ${i === 0 ? '' : 'border-l border-hairline'}`}>
            <div className="micro-label mb-1">{k}</div>
            <div className="font-mono text-[22px] tracking-[-0.01em] tnum">{v}</div>
          </div>
        ))}
      </div>

      <h2 className="mt-16 font-serif text-[24px] font-normal text-ink-primary md:text-[28px]">
        Yang kami lakukan
      </h2>
      <ol className="mt-4 list-none p-0">
        {[
          ['Cari dalam bahasa biasa', 'Tanya dalam Indonesia, dapatkan jawaban terstruktur dari Gemma 4.'],
          ['Telusuri tabel manfaat', 'Setiap nilai diambil dari sel di RIPLAY. Sumber selalu disebut.'],
          ['Buka dokumen asli', 'Setiap halaman produk menautkan ke RIPLAY dan brosur dalam satu klik.'],
          ['Bandingkan 2–4 produk', 'Tabel side-by-side dengan sticky kolom dan baris yang sama.'],
        ].map(([k, v], i) => (
          <li
            key={k}
            className="grid grid-cols-[40px_1fr] gap-2 border-b border-hairline py-4"
          >
            <span className="font-mono text-[11px] text-ink-tertiary">0{i + 1}</span>
            <div>
              <div className="text-[15px] font-medium">{k}</div>
              <div className="mt-1 text-[14px] text-ink-secondary">{v}</div>
            </div>
          </li>
        ))}
      </ol>

      <h2 className="mt-16 font-serif text-[24px] font-normal text-ink-primary md:text-[28px]">
        Yang tidak kami lakukan
      </h2>
      <ul className="mt-4 flex flex-col gap-3 text-[15px] text-ink-secondary">
        <li>· Kami tidak menjual produk. Tidak ada agen, tidak ada komisi.</li>
        <li>· Kami tidak memberi nasihat keuangan. RIPLAY tetap mengikat.</li>
        <li>· Kami tidak menyimpan riwayat pencarian.</li>
      </ul>

      <p className="mt-16 text-[15px] text-ink-secondary">
        Dibangun untuk{' '}
        <a
          href="https://www.kaggle.com/competitions/google-gemma-4-good-hackathon"
          target="_blank"
          rel="noopener noreferrer"
          className="text-brand underline"
        >
          Kaggle Gemma 4 Good Hackathon
        </a>{' '}
        — Digital Equity &amp; Inclusivity. Kembali ke{' '}
        <Link to="/" className="text-brand underline">
          beranda
        </Link>
        .
      </p>
    </main>
  )
}
