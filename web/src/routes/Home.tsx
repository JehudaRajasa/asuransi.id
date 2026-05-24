import { useCallback, useState } from 'react'
import { BrowseBenefits } from '../components/BrowseBenefits'
import { BrowseInsurers } from '../components/BrowseInsurers'
import { HomeFeatured } from '../components/HomeFeatured'
import { HomeHero } from '../components/HomeHero'

export function Home() {
  const [, setLastQuery] = useState<string>('')

  const handleSubmit = useCallback((q: string) => {
    setLastQuery(q)
    // POST /api/query lands in next pass
    console.log('[query]', q)
  }, [])

  return (
    <main className="pb-32 md:pb-24">
      <HomeHero onSubmit={handleSubmit} />
      <BrowseInsurers />
      <BrowseBenefits />
      <HomeFeatured />
      <div className="h-32" aria-hidden="true" />
    </main>
  )
}
