type Props = {
  title: string
  description?: string
  suggestions?: { label: string; description: string; href: string }[]
}

export function EmptyState({ title, description, suggestions = [] }: Props) {
  return (
    <section className="mx-auto max-w-[720px] px-6 py-20 md:px-20">
      <div className="micro-label mb-6">Tidak ada hasil</div>
      <h1 className="m-0 font-serif text-[32px] font-normal leading-[1.1] tracking-[-0.02em] text-ink-primary md:text-[48px]">
        {title}
      </h1>
      {description && (
        <p className="mt-6 max-w-[600px] text-[16px] leading-[1.55] text-ink-secondary md:text-[18px]">
          {description}
        </p>
      )}
      {suggestions.length > 0 && (
        <div className="mt-8">
          <div className="micro-label mb-3">Saran</div>
          <ul className="flex list-none flex-col border-t border-hairline p-0">
            {suggestions.map((s) => (
              <li key={s.label} className="contents">
                <a
                  href={s.href}
                  className="grid grid-cols-[1fr_auto] items-center gap-6 border-b border-hairline py-4 text-ink-primary no-underline hover:bg-brand-soft/30"
                >
                  <div>
                    <div className="text-[15px] font-medium">{s.label}</div>
                    <div className="mt-0.5 text-[13px] text-ink-secondary">{s.description}</div>
                  </div>
                  <span className="text-brand">→</span>
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  )
}
