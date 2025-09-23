import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import Predictions from './pages/Predictions'
import Teams from './pages/Teams'
import About from './pages/About'
import './styles/index.css'
import './styles/components.css'

function Navbar() {
  const location = useLocation()
  
  const isActive = (path) => location.pathname === path

  return (
    <nav className="navbar">
      <Link to="/" className={`nav-link ${isActive('/') ? 'active' : ''}`}>
        Home
      </Link>
      <Link to="/predictions" className={`nav-link ${isActive('/predictions') ? 'active' : ''}`}>
        Predictions
      </Link>
      <Link to="/teams" className={`nav-link ${isActive('/teams') ? 'active' : ''}`}>
        Teams
      </Link>
      <Link to="/about" className={`nav-link ${isActive('/about') ? 'active' : ''}`}>
        About
      </Link>
    </nav>
  )
}

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App