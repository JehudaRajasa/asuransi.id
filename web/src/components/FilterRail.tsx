import { Chip } from './Chip'

type FilterGroup = {
  label: string
  items: { name: string; active?: boolean }[]
}

const FILTER_GROUPS: FilterGroup[] = [
  {
    label: 'Penyedia',
    items: [
      { name: 'Allianz', active: true },
      { name: 'Prudential', active: true },
      { name: 'Manulife', active: true },
      { name: 'AIA' },
      { name: 'BPJS', active: true },
    ],
  },
  {
    label: 'Tipe',
    items: [
      { name: 'Konvensional', active: true },
      { name: 'Syariah' },
      { name: 'Publik (BPJS)', active: true },
    ],
  },
  {
    label: 'Manfaat utama',
    items: [
      { name: 'Rawat inap', active: true },
      { name: 'Rawat jalan', active: true },
      { name: 'Kanker' },
      { name: 'Kritis' },
      { name: 'Maternity' },
      { name: 'Dental' },
    ],
  },
]

export function FilterRail() {
  return (
    <aside className="w-full shrink-0 px-6 py-8 md:w-[240px] md:px-0 md:pl-20 md:pr-8">
      <div className="micro-label mb-4">Filter</div>
      {FILTER_GROUPS.map((g) => (
        <div key={g.label} className="mb-8">
          <div className="mb-3 text-[13px] font-medium">{g.label}</div>
          <div className="flex flex-wrap gap-1.5">
            {g.items.map((it) => (
              <Chip
                key={it.name}
                active={!!it.active}
                removable
                className="px-2.5 py-1 text-[11px]"
              >
                {it.name}
              </Chip>
            ))}
          </div>
        </div>
      ))}

      <div className="mt-10 border-t border-hairline pt-6">
        <div className="micro-label mb-2">Tampilan</div>
        <div className="flex flex-col gap-1.5 text-[13px]">
          <label className="flex items-center gap-2">
            <input type="checkbox" defaultChecked className="accent-brand" />
            Sembunyikan baris kosong
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" className="accent-brand" />
            Tandai nilai terbaik
          </label>
        </div>
      </div>
    </aside>
  )
}
