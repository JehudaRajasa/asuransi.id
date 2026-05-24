type Props = {
  label?: string
  page?: number | string | null
  href?: string
}

export function SourceLink({ label = 'Buka RIPLAY', page = null, href = '#' }: Props) {
  return (
    <a
      href={href}
      target={href.startsWith('http') ? '_blank' : undefined}
      rel={href.startsWith('http') ? 'noopener noreferrer' : undefined}
      className="inline-flex items-center gap-1.5 border-b border-hairline pb-0.5 font-mono text-[12px] text-ink-secondary hover:text-ink-primary"
    >
      <span>{label}</span>
      {page !== null && page !== undefined && page !== '' && (
        <span className="text-ink-tertiary">· hal. {page}</span>
      )}
      <span className="text-brand">↗</span>
    </a>
  )
}
