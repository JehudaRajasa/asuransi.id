import type { ReactNode } from 'react'

type Tone = 'default' | 'brand' | 'public'

const TONE: Record<Tone, string> = {
  default: 'border-hairline text-ink-secondary',
  brand: 'border-brand text-brand bg-brand-soft',
  public: 'border-ink-primary text-ink-primary',
}

export function Tag({ children, tone = 'default' }: { children: ReactNode; tone?: Tone }) {
  return (
    <span
      className={`inline-block border px-2 py-[3px] font-mono text-[10px] uppercase tracking-[0.1em] ${TONE[tone]}`}
    >
      {children}
    </span>
  )
}
