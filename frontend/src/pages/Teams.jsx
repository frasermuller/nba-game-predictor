import { useState, useEffect } from 'react'
import { teamColors } from '../teamColors'
import { API_BASE_URL } from '../config'

const Teams = () => {
  const [teams, setTeams] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Helper function to convert abbreviation to full team name
  const getFullTeamName = (abbr) => {
    const teamNameMap = {
      'ATL': 'Atlanta Hawks',
      'BOS': 'Boston Celtics',
      'BRK': 'Brooklyn Nets',
      'CHO': 'Charlotte Hornets',
      'CHI': 'Chicago Bulls',
      'CLE': 'Cleveland Cavaliers',
      'DAL': 'Dallas Mavericks',
      'DEN': 'Denver Nuggets',
      'DET': 'Detroit Pistons',
      'GSW': 'Golden State Warriors',
      'HOU': 'Houston Rockets',
      'IND': 'Indiana Pacers',
      'LAC': 'Los Angeles Clippers',
      'LAL': 'Los Angeles Lakers',
      'MEM': 'Memphis Grizzlies',
      'MIA': 'Miami Heat',
      'MIL': 'Milwaukee Bucks',
      'MIN': 'Minnesota Timberwolves',
      'NOP': 'New Orleans Pelicans',
      'NYK': 'New York Knicks',
      'OKC': 'Oklahoma City Thunder',
      'ORL': 'Orlando Magic',
      'PHI': 'Philadelphia 76ers',
      'PHO': 'Phoenix Suns',
      'POR': 'Portland Trail Blazers',
      'SAC': 'Sacramento Kings',
      'SAS': 'San Antonio Spurs',
      'TOR': 'Toronto Raptors',
      'UTA': 'Utah Jazz',
      'WAS': 'Washington Wizards'
    }
    return teamNameMap[abbr] || abbr
  }

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/teams`)
        if (!response.ok) {
          throw new Error('Failed to fetch teams')
        }
        const data = await response.json()
        setTeams(data)
      } catch (err) {
        setError('Failed to load teams. Please try again later.')
        console.error('Error fetching teams:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchTeams()
  }, [])

  if (loading) {
    return (
      <div className="teams-page">
        <div className="page-header">
          <h1>NBA Teams</h1>
        </div>
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <div className="loading-spinner"></div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="teams-page">
        <div className="page-header">
          <h1>NBA Teams</h1>
        </div>
        <div style={{ textAlign: 'center', padding: '2rem', color: 'red' }}>
          {error}
        </div>
      </div>
    )
  }

  return (
    <div className="teams-page">
      <div className="page-header">
        <h1>NBA Teams</h1>
        <p className="teams-page-subtitle">Statistics shown are from the most recent 2024-2025 NBA season</p>
      </div>
      
      {/* Team cards grid */}
      <div className="teams-grid">
        {teams.map((team, index) => {
          const fullTeamName = getFullTeamName(team.name)
          const colors = teamColors[fullTeamName] || { primary: '#17408B', secondary: '#C9082A' }
          
          return (
            <div
              key={team.name || index}
              className="team-card"
              style={{
                background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.primary} 60%, ${colors.secondary} 100%)`,
                color: 'white'
              }}
            >
              <div className="team-name">
                {fullTeamName}
              </div>
              
              {/* Team statistics overlay (shown on hover) */}
              <div className="team-stats">
                <div className="stats-header">2024-25 Season Stats</div>
                <div className="stat-label">Record:</div>
                <div className="stat-value">{team.wins}-{team.losses}</div>
                <div className="stat-label">Win %:</div>
                <div className="stat-value">{(team.win_percentage * 100).toFixed(1)}%</div>
                <div className="stat-label">PPG:</div>
                <div className="stat-value">{team.points_per_game.toFixed(1)}</div>
                <div className="stat-label">FG%:</div>
                <div className="stat-value">{(team.field_goal_percentage * 100).toFixed(1)}%</div>
                <div className="stat-label">3P%:</div>
                <div className="stat-value">{(team.three_point_percentage * 100).toFixed(1)}%</div>
                <div className="stat-label">RPG:</div>
                <div className="stat-value">{team.rebounds_per_game.toFixed(1)}</div>
                <div className="stat-label">APG:</div>
                <div className="stat-value">{team.assists_per_game.toFixed(1)}</div>
                <div className="stat-label">SPG:</div>
                <div className="stat-value">{team.steals_per_game.toFixed(1)}</div>
              </div>
            </div>
          )
        })}
      </div>
      
      {/* Statistics explanation guide */}
      <div className="stats-guide">
        <h2>Statistics Guide</h2>
        <p>Understanding the 2024-25 NBA season statistics displayed for each team:</p>
        
        <div className="stats-grid">
          <div className="stat-explanation">
            <h3>🏆 Team Record</h3>
            <p><strong>Record (W-L):</strong> Wins and losses for the 2024-25 season</p>
            <p><strong>Win %:</strong> Percentage of games won this season</p>
          </div>
          
          <div className="stat-explanation">
            <h3>🏀 Offensive Stats</h3>
            <p><strong>PPG (Points Per Game):</strong> Average points scored per game</p>
            <p><strong>FG% (Field Goal %):</strong> Percentage of all field goals made</p>
            <p><strong>3P% (3-Point %):</strong> Percentage of three-point shots made</p>
            <p><strong>APG (Assists Per Game):</strong> Average assists made per game</p>
          </div>
          
          <div className="stat-explanation">
            <h3>🛡️ Defensive & Hustle Stats</h3>
            <p><strong>RPG (Rebounds Per Game):</strong> Average rebounds collected per game</p>
            <p><strong>SPG (Steals Per Game):</strong> Average steals made per game</p>
          </div>
          
          <div className="stat-explanation">
            <h3>🤖 How Our AI Uses These Stats</h3>
            <p>These statistics represent each team's 2024-25 season performance. Our prediction model analyzes these metrics alongside rolling averages, opponent matchups, and historical data to forecast game outcomes with high accuracy.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Teams