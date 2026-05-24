import { Chip } from './Chip'

type Props = {
  examples: string[]
  onPick: (q: string) => void
}

export function IntentPillRow({ examples, onPick }: Props) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="micro-label mr-3 self-center">Contoh</span>
      {examples.map((q) => (
        <Chip key={q} onClick={() => onPick(q)}>
          {q}
        </Chip>
      ))}
    </div>
  )
}
