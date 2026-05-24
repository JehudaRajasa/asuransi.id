import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { Nav } from './components/Nav'
import { DisclaimerStrip } from './components/DisclaimerStrip'
import { Home } from './routes/Home'

export default function App() {
  return (
    <BrowserRouter>
      <Nav />
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
      <DisclaimerStrip />
    </BrowserRouter>
  )
}
