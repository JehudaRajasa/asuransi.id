import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react'
import { TOTAL_PRODUCTS } from '../data/derive'

type Props = {
  onSubmit?: (q: string) => void
  placeholder?: string
  value: string
  onChange: (q: string) => void
}

export type HeroSearchHandle = {
  focus: () => void
}

const DEFAULT_PLACEHOLDER =
  'rawat inap di atas Rp 1 juta per hari, kanker tak terbatas…'

export const HeroSearch = forwardRef<HeroSearchHandle, Props>(function HeroSearch(
  { onSubmit, placeholder = DEFAULT_PLACEHOLDER, value, onChange },
  ref,
) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [submitting, setSubmitting] = useState(false)

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current?.focus(),
  }), [])

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== '/') return
      const t = e.target as HTMLElement | null
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return
      e.preventDefault()
      inputRef.current?.focus()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const q = value.trim()
    if (!q || submitting) return
    setSubmitting(true)
    onSubmit?.(q)
    window.setTimeout(() => setSubmitting(false), 1200)
  }

  return (
    <form onSubmit={handleSubmit} className="w-full" aria-label="Tanya dalam Bahasa Indonesia">
      <div className="mb-3.5 font-mono text-[12px] tracking-[0.02em] text-ink-secondary">
        Tanya dalam Bahasa Indonesia · Didukung oleh Gemma 4
      </div>
      <div className="flex items-center gap-4 border-b-2 border-ink-primary py-4 focus-within:border-brand">
        <span className="font-mono text-[14px] text-ink-tertiary" aria-hidden="true">
          ?
        </span>
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          disabled={submitting}
          className="min-w-0 flex-1 bg-transparent text-[22px] font-normal tracking-[-0.01em] text-ink-primary placeholder:text-ink-tertiary focus:outline-none disabled:text-ink-tertiary md:text-[24px]"
          aria-label="Pertanyaan kamu"
        />
        <span className="hidden border border-hairline px-2 py-1 font-mono text-[11px] uppercase tracking-[0.08em] text-ink-tertiary md:inline">
          ⏎ tanya
        </span>
      </div>
      <div className="mt-3 min-h-[1rem]" aria-live="polite">
        {submitting && (
          <span className="font-mono text-[12px] text-ink-secondary">
            mencari di {TOTAL_PRODUCTS} produk…
          </span>
        )}
      </div>
    </form>
  )
})
