import React from 'react'

function About() {
  return (
    <div className="about-page">
      <div className="page-header">
        <h1>About NBA Game Predictor</h1>
      </div>
      
      <div className="about-content">
        <section>
          <h2>🏀 What This Does</h2>
          <p>
            NBA Game Predictor uses advanced machine learning to forecast NBA game outcomes with win probabilities and predicted scores. 
            The model analyzes 7 complete seasons of NBA data (2018-2019 through 2024-2025) to identify patterns 
            and predict future matchups between any two teams.
          </p>
        </section>

        <section>
          <h2>📊 The Dataset</h2>
          <p>
            These predictions are powered by an extensive dataset containing:
          </p>
          <ul>
            <li><strong>8,910 individual NBA games</strong> (17,819 rows of data)</li>
            <li><strong>7 complete seasons</strong> from 2018-2019 through 2024-2025</li>
            <li><strong>150+ statistical features</strong> per game including shooting percentages, rebounds, assists, turnovers, and advanced metrics</li>
            <li><strong>All 30 NBA teams</strong> with comprehensive coverage</li>
            <li><strong>Home/away splits</strong> and situational factors</li>
          </ul>
          <p>
            This massive dataset represents nearly every regular season and playoff game over 7 years, 
            providing the model with deep insights into team performance patterns, matchup dynamics, and seasonal trends.
          </p>
        </section>

        <section>
          <h2>🔬 How Games Are Predicted</h2>
          
          <h3>Step 1: Data Collection & Processing</h3>
          <p>
            Detailed box scores and advanced statistics were scraped for all 8,910 games in the dataset. 
            Each game includes 150+ metrics covering every aspect of basketball performance:
          </p>
          <ul>
            <li><strong>Shooting:</strong> Field goal percentages, three-point shooting, free throw accuracy</li>
            <li><strong>Possession:</strong> Rebounds (offensive/defensive), turnovers, steals</li>
            <li><strong>Playmaking:</strong> Assists, assist-to-turnover ratios, ball movement</li>
            <li><strong>Efficiency:</strong> True shooting percentage, effective field goal percentage, pace</li>
            <li><strong>Impact:</strong> Plus/minus ratings, usage rates, game score metrics</li>
          </ul>

          <h3>Step 2: Rolling Averages & Feature Engineering</h3>
          <p>
            Raw game statistics can be misleading due to one-off performances. Instead, the system calculates 
            <strong> rolling 10-game averages</strong> for every metric, which provides:
          </p>
          <ul>
            <li><strong>Smooth performance trends</strong> rather than single-game outliers</li>
            <li><strong>Recent form emphasis</strong> while maintaining statistical stability</li>
            <li><strong>Injury/roster change adaptation</strong> as the averages adjust to lineup changes</li>
            <li><strong>Momentum capture</strong> for teams getting hot or cold</li>
          </ul>
          <p>
            For example, if the Lakers have shot 45%, 38%, 52%, 41%, 48% from three in their last 5 games, 
            the system doesn't just use 48% (most recent). It uses their rolling 10-game average which smooths out 
            the outliers while still reflecting recent trends.
          </p>

          <h3>Step 3: Opponent Context Integration</h3>
          <p>
            The analysis doesn't just look at Team A vs Team B in isolation. The model incorporates:
          </p>
          <ul>
            <li><strong>Head-to-head historical performance</strong> between specific teams</li>
            <li><strong>Opponent-adjusted statistics</strong> (how teams perform against similar opponents)</li>
            <li><strong>Matchup-specific factors</strong> (pace compatibility, style clashes)</li>
            <li><strong>Home court advantage</strong> quantified from 7 years of data</li>
          </ul>

          <h3>Step 4: Machine Learning Model</h3>
          <p>
            The system uses a <strong>Logistic Regression model</strong> enhanced with feature selection:
          </p>
          <ul>
            <li><strong>Sequential Feature Selection:</strong> Automatically identifies the 30 most predictive statistics from 150+ features</li>
            <li><strong>Time Series Cross-Validation:</strong> Trains on past seasons and tests on future seasons to prevent data leakage</li>
            <li><strong>MinMax Scaling:</strong> Ensures all statistics are weighted fairly regardless of their natural scale</li>
          </ul>

          <h3>Step 5: Future Matchup Prediction</h3>
          <p>
            When two teams are selected for prediction, the model:
          </p>
          <ol>
            <li>Retrieves the latest rolling 10-game averages for both teams</li>
            <li>Applies the same preprocessing used during training</li>
            <li>Feeds the 30 most important features into the trained model</li>
            <li>Generates win probabilities and predicted scores</li>
            <li>Estimates final scores based on pace and efficiency metrics</li>
          </ol>
        </section>

        <section>
          <h2>🎯 Model Performance</h2>
          <p>
            The model has been backtested across multiple seasons with <strong>time series validation</strong>, 
            meaning it trains on past data and tests on future games (just like real-world usage).
          </p>
          
          <p>
            <strong>Overall Model Accuracy:</strong> Based on backtesting across 7 seasons of data, 
            the model maintains approximately <strong>68% accuracy</strong> on game predictions.
          </p>
        </section>

        <section>
          <h2>🚀 Key Features</h2>
          <ul>
            <li><strong>Real-time Predictions:</strong> Generate predictions for any team matchup instantly</li>
            <li><strong>Win Probabilities:</strong> See the percentage chance each team has to win</li>
            <li><strong>Score Projections:</strong> Estimated final scores based on pace and efficiency</li>
            <li><strong>Team Analytics:</strong> Detailed statistics for all 30 NBA teams</li>
            <li><strong>Recent Form:</strong> Visual representation of each team's last 5 games</li>
          </ul>
        </section>

        <section>
          <h2>⚡ Technology Stack</h2>
          <ul>
            <li><strong>Data Processing:</strong> Python, Pandas, NumPy</li>
            <li><strong>Machine Learning:</strong> Scikit-learn, Logistic Regression</li>
            <li><strong>Backend:</strong> Flask API with real-time predictions</li>
            <li><strong>Frontend:</strong> React with responsive design</li>
            <li><strong>Data Storage:</strong> CSV with efficient data structures</li>
          </ul>
        </section>

        <section>
          <h2>⚠️ Important Disclaimers</h2>
          <p>
            While this model uses sophisticated analysis of 8,910 games across 7 seasons, 
            basketball remains beautifully unpredictable. These predictions cannot account for:
          </p>
          <ul>
            <li>Last-minute injuries or lineup changes</li>
            <li>Weather conditions, travel fatigue, or scheduling factors</li>
            <li>Emotional factors, rivalries, or playoff implications</li>
            <li>Individual player hot/cold streaks on game day</li>
            <li>Coaching adjustments and game-specific strategies</li>
            <li>Referee tendencies or unusual circumstances</li>
          </ul>
          <p>
            <strong>This tool is designed for entertainment and educational purposes. </strong> 
            Any team can win on any given night - that's what makes basketball exciting! 
            The model provides data-driven insights, but the human element and game-day factors 
            will always introduce uncertainty.
          </p>
        </section>

        <section>
          <h2>📈 Future Development Plans</h2>
          <p>
            While the current model provides solid predictions with 68% accuracy using 7 seasons of data, 
            several improvements are planned for future releases:
          </p>
          
          <ul>
            <li><strong>Extended Dataset:</strong> Incorporating 10+ seasons of NBA data to improve accuracy beyond 75%</li>
            <li><strong>Real-Time Schedule:</strong> Automatic predictions for actual upcoming NBA games instead of mock matchups</li>
            <li><strong>Enhanced Features:</strong> Player injury reports and advanced metrics integration for more precise predictions</li>
          </ul>

          <p>
            The foundation built with 8,910 games across 7 seasons provides an excellent starting point 
            for these future enhancements.
          </p>
        </section>
      </div>
    </div>
  )
}

export default About