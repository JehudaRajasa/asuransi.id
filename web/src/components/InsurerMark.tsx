type Props = {
  name: string
  slug?: string
  size?: number
}

export function InsurerMark({ name, slug, size = 32 }: Props) {
  const source = slug ?? name
  const initials = source
    .split(/[\s-]/)
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase() ?? '')
    .join('')

  return (
    <div
      aria-hidden="true"
      className="inline-flex items-center justify-center bg-brand text-ink-inverse font-mono font-medium tnum"
      style={{
        width: size,
        height: size,
        fontSize: size * 0.36,
        letterSpacing: '0.04em',
      }}
    >
      {initials}
    </div>
  )
}
