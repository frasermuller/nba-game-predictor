import { Link } from 'react-router-dom'
import { FaBasketballBall, FaChartLine, FaUsers, FaRocket } from 'react-icons/fa'
import { useState, useEffect } from 'react'
import { API_BASE_URL } from '../config'

function Home() {
  const [apiTest, setApiTest] = useState('Testing...')

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/teams`)
      .then(res => res.json())
      .then(data => setApiTest(`API Working! Found ${data.length} teams`))
      .catch(err => setApiTest(`API Error: ${err.message}`))
  }, [])

  return (
    <div className="home">
      {/* Hero section with main title and stats */}
      <div className="hero">
        <div className="hero-content">
          <h1>NBA GAME PREDICTOR</h1>
          <p className="hero-subtitle">Advanced ML predictions powered by 8,910 games across 7 NBA seasons</p>
          
          {/* Key statistics display */}
          <div className="hero-stats">
            <div className="stat-item">
              <span className="stat-number">8,910</span>
              <span className="stat-label">Games Analyzed</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">7</span>
              <span className="stat-label">NBA Seasons</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">30</span>
              <span className="stat-label">Teams Covered</span>
            </div>
          </div>
          
          <Link to="/predictions" className="cta-button">
            <FaRocket className="button-icon" />
            START PREDICTING
          </Link>
        </div>
      </div>
      
      {/* Feature cards showing main capabilities */}
      <div className="features">
        <div className="feature-card">
          <div className="feature-icon">
            <FaBasketballBall size={48} />
          </div>
          <h3>Game Predictions</h3>
          <p>Get accurate predictions with win probabilities for any matchup</p>
          <div className="feature-highlight">Real-time Analysis</div>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">
            <FaChartLine size={48} />
          </div>
          <h3>Team Analytics</h3>
          <p>View detailed statistics and recent performance trends</p>
          <div className="feature-highlight">Advanced Metrics</div>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">
            <FaUsers size={48} />
          </div>
          <h3>All 30 Teams</h3>
          <p>Complete coverage of every NBA team with up-to-date data</p>
          <div className="feature-highlight">Complete Coverage</div>
        </div>
      </div>

    </div>
  )
}

export default Home