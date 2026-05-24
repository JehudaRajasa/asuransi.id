import type { ButtonHTMLAttributes, ReactNode } from 'react'

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  active?: boolean
  removable?: boolean
  children: ReactNode
}

export function Chip({ active = false, removable = false, children, className = '', ...rest }: Props) {
  const base =
    'inline-flex items-center gap-1.5 rounded-full border px-3 py-[7px] font-mono text-[12px] transition-colors'
  const tone = active
    ? 'border-brand bg-brand-soft text-brand-ink'
    : 'border-hairline bg-transparent text-ink-primary hover:border-brand hover:bg-brand-soft/40'

  return (
    <button type="button" className={`${base} ${tone} ${className}`} {...rest}>
      {children}
      {removable && active && <span className="text-[11px] text-ink-tertiary">×</span>}
    </button>
  )
}
