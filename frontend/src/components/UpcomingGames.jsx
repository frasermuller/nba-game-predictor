import { useState } from 'react'

function UpcomingGames() {
  // Mock data to demonstrate future feature
  const mockUpcomingGames = [
    { id: 1, team1: 'Lakers', team2: 'Warriors', date: '2025-02-15', time: '7:30 PM' },
    { id: 2, team1: 'Celtics', team2: 'Heat', date: '2025-02-16', time: '8:00 PM' },
    { id: 3, team1: 'Nuggets', team2: 'Suns', date: '2025-02-17', time: '9:00 PM' },
    { id: 4, team1: 'Bucks', team2: 'Nets', date: '2025-02-18', time: '7:00 PM' },
  ]

  return (
    <div className="upcoming-games-section">
      <div className="page-header">
        <h2>Future Feature: Real-Time NBA Schedule</h2>
        <p className="feature-subtitle">Automatic predictions for actual upcoming NBA games</p>
      </div>
      
      {/* Feature preview explanation */}
      <div className="feature-preview-card">
        <div className="preview-badge">
          Coming Soon
        </div>
        <p className="feature-description">
          In future updates, this section will automatically display predictions for real upcoming NBA games, 
          fetched directly from the official NBA schedule API.
        </p>
      </div>
      
      {/* Mock upcoming games grid */}
      <div className="upcoming-games-grid">
        {mockUpcomingGames.map(game => (
          <div key={game.id} className="upcoming-game-card">
            <div className="game-header">
              <span className="game-date">{game.date}</span>
              <span className="game-time">{game.time}</span>
            </div>
            
            <div className="game-matchup">
              <div className="team-box">
                <span className="team-name">{game.team1}</span>
              </div>
              <div className="vs-divider">VS</div>
              <div className="team-box">
                <span className="team-name">{game.team2}</span>
              </div>
            </div>
            
            <div className="prediction-status">
              <span className="status-text">AI Prediction Ready</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default UpcomingGames
