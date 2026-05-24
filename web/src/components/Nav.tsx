import { Link, useLocation } from 'react-router-dom'

const LINKS: { label: string; href: string }[] = [
  { label: 'Beranda', href: '/' },
  { label: 'Penyedia', href: '/penyedia' },
  { label: 'Manfaat', href: '/manfaat' },
  { label: 'Bandingkan', href: '/compare' },
  { label: 'Tentang', href: '/tentang' },
]

type Props = { crumb?: string }

export function Nav({ crumb }: Props) {
  const { pathname } = useLocation()
  const isActive = (href: string) => (href === '/' ? pathname === '/' : pathname.startsWith(href))

  return (
    <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-hairline bg-page px-6 md:px-20">
      <div className="flex items-center gap-8">
        <Link
          to="/"
          className="font-serif text-[20px] font-semibold tracking-[-0.02em] text-ink-primary no-underline"
        >
          asuransi<span className="text-brand">.</span>id
        </Link>
        {crumb && (
          <span className="hidden font-mono text-[11px] uppercase tracking-[0.08em] text-ink-tertiary md:inline">
            / {crumb}
          </span>
        )}
      </div>
      <nav className="flex items-center gap-6 md:gap-8">
        <ul className="hidden items-center gap-6 md:flex md:gap-8">
          {LINKS.map((l) => {
            const active = isActive(l.href)
            return (
              <li key={l.href}>
                <Link
                  to={l.href}
                  className={`pb-1 text-[14px] no-underline ${
                    active
                      ? 'border-b border-ink-primary font-medium text-ink-primary'
                      : 'text-ink-secondary hover:text-ink-primary'
                  }`}
                >
                  {l.label}
                </Link>
              </li>
            )
          })}
        </ul>
        <span className="font-mono text-[11px] uppercase tracking-[0.08em] text-ink-secondary">
          <b className="font-medium text-ink-primary">ID</b> · EN
        </span>
      </nav>
    </header>
  )
}
