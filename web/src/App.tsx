import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { DisclaimerStrip } from './components/DisclaimerStrip'
import { Nav } from './components/Nav'
import { Compare } from './routes/Compare'
import { Home } from './routes/Home'
import { Manfaat } from './routes/Manfaat'
import { ManfaatSlug } from './routes/ManfaatSlug'
import { Penyedia } from './routes/Penyedia'
import { PenyediaSlug } from './routes/PenyediaSlug'
import { Product } from './routes/Product'
import { Tentang } from './routes/Tentang'

export default function App() {
  return (
    <BrowserRouter>
      <Nav />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/penyedia" element={<Penyedia />} />
        <Route path="/penyedia/:slug" element={<PenyediaSlug />} />
        <Route path="/manfaat" element={<Manfaat />} />
        <Route path="/manfaat/:slug" element={<ManfaatSlug />} />
        <Route path="/produk/:slug" element={<Product />} />
        <Route path="/compare" element={<Compare />} />
        <Route path="/tentang" element={<Tentang />} />
      </Routes>
      <DisclaimerStrip />
    </BrowserRouter>
  )
}
