import { useState } from 'react'
import UpcomingGames from '../components/UpcomingGames'
import { API_BASE_URL } from '../config'

function Predictions() {
  const [homeTeam, setHomeTeam] = useState('')
  const [awayTeam, setAwayTeam] = useState('')
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // All NBA teams for dropdown selection
  const teams = [
    'ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
    'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
    'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
  ]

  const handlePredict = async () => {
    if (!homeTeam || !awayTeam) {
      setError('Please select both teams')
      return
    }

    if (homeTeam === awayTeam) {
      setError('Please select different teams')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          home_team: homeTeam,
          away_team: awayTeam,
        }),
      })

      if (!response.ok) {
        throw new Error('Prediction failed')
      }

      const data = await response.json()
      setPrediction(data)
    } catch (err) {
      setError('Failed to get prediction. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const resetPrediction = () => {
    setPrediction(null)
    setHomeTeam('')
    setAwayTeam('')
    setError('')
  }

  return (
    <div className="predictions-page">
      <div className="page-header">
        <h1>Game Predictions</h1>
      </div>

      {/* Team selection interface */}
      <div className="prediction-selector">
        <div className="selector-header">
          <h2>Select Teams</h2>
          <p>Choose two teams to predict the game outcome</p>
        </div>

        <div className="team-selection">
          <div className="team-select-container">
            <label>Home Team</label>
            <select 
              className="team-select" 
              value={homeTeam} 
              onChange={(e) => setHomeTeam(e.target.value)}
            >
              <option value="">Select Home Team</option>
              {teams.map(team => (
                <option key={team} value={team}>{team}</option>
              ))}
            </select>
          </div>

          <div className="vs-divider">VS</div>

          <div className="team-select-container">
            <label>Away Team</label>
            <select 
              className="team-select" 
              value={awayTeam} 
              onChange={(e) => setAwayTeam(e.target.value)}
            >
              <option value="">Select Away Team</option>
              {teams.map(team => (
                <option key={team} value={team}>{team}</option>
              ))}
            </select>
          </div>
        </div>

        <button 
          className={`predict-button ${loading || !homeTeam || !awayTeam ? 'disabled' : ''}`}
          onClick={handlePredict}
          disabled={loading || !homeTeam || !awayTeam}
        >
          {loading ? (
            <>
              <div className="loading-spinner small"></div>
              Analyzing...
            </>
          ) : (
            'Get Prediction'
          )}
        </button>

        {error && (
          <div className="error-message">{error}</div>
        )}
      </div>

      {/* Prediction results display */}
      {prediction && (
        <div className="prediction-results">
          <div className="prediction-header">
            <h2>Prediction Results</h2>
            <div className="matchup-display">
              {prediction.home_team} <span className="vs">vs</span> {prediction.away_team}
            </div>
          </div>

          {/* Winner announcement */}
          <div className="winner-announcement">
            <div className="winner-card">
              <h3>Predicted Winner</h3>
              <div className="winner-name">{prediction.winner}</div>
            </div>
          </div>

          {/* Detailed prediction breakdown */}
          <div className="prediction-details">
            <div className="detail-card">
              <h4>Predicted Score</h4>
              <div className="score-prediction">
                <div className="team-score">
                  <span className="team-name">{prediction.home_team}</span>
                  <span className="score">{prediction.predicted_score.home}</span>
                </div>
                <span className="score-divider">-</span>
                <div className="team-score">
                  <span className="team-name">{prediction.away_team}</span>
                  <span className="score">{prediction.predicted_score.away}</span>
                </div>
              </div>
            </div>

            <div className="detail-card">
              <h4>Win Probabilities</h4>
              <div className="probability-bars">
                <div className="probability-item">
                  <div className="prob-header">
                    <span>{prediction.home_team}</span>
                    <span>{(prediction.home_win_probability * 100).toFixed(1)}%</span>
                  </div>
                  <div className="probability-bar">
                    <div 
                      className="probability-fill"
                      style={{ width: `${prediction.home_win_probability * 100}%` }}
                    ></div>
                  </div>
                </div>

                <div className="probability-item">
                  <div className="prob-header">
                    <span>{prediction.away_team}</span>
                    <span>{(prediction.away_win_probability * 100).toFixed(1)}%</span>
                  </div>
                  <div className="probability-bar">
                    <div 
                      className="probability-fill"
                      style={{ width: `${prediction.away_win_probability * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <button className="new-prediction-button" onClick={resetPrediction}>
            Make New Prediction
          </button>
        </div>
      )}

      <UpcomingGames />
    </div>
  )
}

export default Predictions