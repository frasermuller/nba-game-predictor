import React from 'react'

function About() {
  return (
    <div className="about-page">
      <div className="page-header">
        <h1>About NBA Game Predictor</h1>
      </div>
      
      <div className="about-content">
        <section>
          <h2>Project Overview</h2>
          <p>
            NBA Game Predictor is a full-stack web application that combines machine learning with modern web development 
            to predict NBA game outcomes. Built with a Python Flask backend and React frontend, it analyzes historical 
            NBA game data to generate win probabilities for any team matchup.
          </p>
          <p>
            This project demonstrates the complete data science pipeline - from raw data collection and cleaning to 
            feature engineering, model training, and deployment in a production-ready web application.
          </p>
        </section>

        <section>
          <h2>The Dataset</h2>
          <p>
            The predictions are powered by a comprehensive dataset containing:
          </p>
          <ul>
            <li><strong>8,910 individual NBA games</strong> from multiple seasons (2019-2025)</li>
            <li><strong>150+ original statistical features</strong> per game including shooting, rebounding, assists, and advanced metrics</li>
            <li><strong>All 30 NBA teams</strong> with complete coverage</li>
            <li><strong>Home/away context</strong> for home court advantage</li>
            <li><strong>Player-level statistics</strong> aggregated to team performance</li>
          </ul>
          <p>
            This massive dataset represents nearly every regular season and playoff game over 7 years, 
            providing the model with deep insights into team performance patterns, matchup dynamics, and seasonal trends.
          </p>
        </section>

        <section>
          <h2>The Complete Process</h2>
          
          <h3>Step 1: Data Collection & Cleaning</h3>
          <p>
            Historical NBA game data is sourced from basketball-reference.com and includes detailed box scores 
            and advanced statistics for 8,910 games. The data cleaning process involves:
          </p>
          <ul>
            <li><strong>Removing inconsistent features:</strong> Usage rates and other problematic metrics are filtered out</li>
            <li><strong>Data validation:</strong> Games with missing or invalid data are excluded</li>
            <li><strong>Feature standardization:</strong> All statistics are converted to consistent formats</li>
            <li><strong>Team mapping:</strong> Standardized team abbreviations and handling of relocations</li>
          </ul>

          <h3>Step 2: Feature Engineering</h3>
          <p>
            The system transforms raw game statistics into meaningful predictive features using <strong>rolling 10-game averages</strong>:
          </p>
          <ul>
            <li><strong>Core team stats:</strong> FG%, 3P%, FT%, rebounds, assists, steals, blocks, turnovers</li>
            <li><strong>Advanced metrics:</strong> True shooting %, effective FG%, plus/minus ratings</li>
            <li><strong>Player impact:</strong> Maximum individual player statistics per game</li>
            <li><strong>Opponent context:</strong> How teams perform against their recent opponents</li>
            <li><strong>Home court advantage:</strong> Binary feature indicating home vs away team</li>
          </ul>
          <p>
            This approach reduces noise from single-game outliers while capturing recent performance trends 
            and momentum shifts throughout the season.
          </p>

          <h3>Step 3: Model Training & Selection</h3>
          <p>
            The machine learning pipeline uses <strong>22 carefully selected features</strong> with a Logistic Regression model:
          </p>
          <ul>
            <li><strong>Feature Selection:</strong> Automated selection of the 22 most predictive statistics from 150+ candidates</li>
            <li><strong>Data Preprocessing:</strong> MinMax scaling ensures all features contribute equally</li>
            <li><strong>Model Training:</strong> Logistic regression trained on thousands of historical matchups</li>
            <li><strong>Validation:</strong> Performance tested on held-out games to prevent overfitting</li>
          </ul>

          <h3>Step 4: Real-Time Prediction</h3>
          <p>
            For any team matchup, the system:
          </p>
          <ol>
            <li>Extracts the latest rolling averages for both teams</li>
            <li>Applies the same preprocessing pipeline used during training</li>
            <li>Feeds the 22 features into the trained model</li>
            <li>Generates win probabilities and confidence intervals</li>
            <li>Estimates final scores using team pace and efficiency metrics</li>
          </ol>
        </section>

        <section>
          <h2>Model Performance</h2>
          <p>
            The current model achieves approximately <strong>60-65% accuracy</strong> on NBA game predictions, 
            which is considered realistic and competitive for basketball prediction models. This performance reflects:
          </p>
          <ul>
            <li><strong>Balanced approach:</strong> The model avoids overfitting while capturing meaningful patterns</li>
            <li><strong>Real-world validation:</strong> Tested on actual historical game outcomes</li>
            <li><strong>Conservative estimates:</strong> Basketball's inherent unpredictability limits theoretical maximum accuracy</li>
            <li><strong>Consistent performance:</strong> Accuracy remains stable across different team matchups and seasons</li>
          </ul>
          <p>
            <em>Note: NBA games are inherently difficult to predict due to injuries, player rest, momentum shifts, 
            and the high variance in basketball scoring. Our 60-65% accuracy represents a significant improvement 
            over random chance (50%) while remaining realistic about the sport's unpredictability.</em>
          </p>
        </section>

        <section>
          <h2>Application Features</h2>
          <ul>
            <li><strong>Matchup Predictions:</strong> Generate win probabilities for any two NBA teams</li>
            <li><strong>Score Projections:</strong> Estimated final scores based on team pace and efficiency</li>
            <li><strong>Team Statistics:</strong> Comprehensive stats for all 30 NBA teams with current 2024-25 season data</li>
            <li><strong>Performance Metrics:</strong> Detailed breakdown of shooting, rebounding, and advanced analytics</li>
            <li><strong>Responsive Design:</strong> Fully functional on desktop and mobile devices</li>
            <li><strong>Real-time Processing:</strong> Predictions generated in under 100ms</li>
          </ul>
        </section>

        <section>
          <h2>Complete Technology Stack</h2>
          
          <h3>Data Pipeline</h3>
          <ul>
            <li><strong>Data Source:</strong> Basketball-reference.com (8,910 NBA games with 150+ features) and ESPN.com (2024/2025 season team stats for display)</li>
            <li><strong>Data Processing:</strong> Python with Pandas and NumPy for cleaning and transformation</li>
            <li><strong>Feature Engineering:</strong> Custom rolling averages and statistical calculations</li>
            <li><strong>Data Storage:</strong> CSV files with optimized data structures</li>
          </ul>

          <h3>Machine Learning</h3>
          <ul>
            <li><strong>Framework:</strong> Scikit-learn for model training and evaluation</li>
            <li><strong>Algorithm:</strong> Logistic Regression with 22 selected features</li>
            <li><strong>Preprocessing:</strong> MinMaxScaler for feature normalization</li>
            <li><strong>Model Persistence:</strong> Joblib for model serialization and loading</li>
          </ul>

          <h3>Backend Development</h3>
          <ul>
            <li><strong>Framework:</strong> Flask (Python) for RESTful API</li>
            <li><strong>CORS:</strong> Flask-CORS for cross-origin requests</li>
            <li><strong>Real-time Processing:</strong> Live feature extraction and prediction</li>
            <li><strong>Error Handling:</strong> Comprehensive exception handling and logging</li>
          </ul>

          <h3>Frontend Development</h3>
          <ul>
            <li><strong>Framework:</strong> React 19 with functional components and hooks</li>
            <li><strong>Build Tool:</strong> Vite for fast development and optimized builds</li>
            <li><strong>Routing:</strong> React Router for single-page application navigation</li>
            <li><strong>Styling:</strong> Custom CSS with NBA team colors and responsive design</li>
            <li><strong>HTTP Client:</strong> Fetch API for backend communication</li>
          </ul>

          <h3>Development & Deployment</h3>
          <ul>
            <li><strong>Version Control:</strong> Git with organized commit history</li>
            <li><strong>Environment Management:</strong> Python virtual environments</li>
            <li><strong>Package Management:</strong> pip (Python) and npm (JavaScript)</li>
            <li><strong>Development Servers:</strong> Flask dev server (port 3001) and Vite dev server (port 5174)</li>
          </ul>
        </section>

        <section>
          <h2>Educational Purpose & Learning Outcomes</h2>
          <p>
            This project demonstrates a complete end-to-end data science and web development workflow:
          </p>
          <ul>
            <li><strong>Data Science Pipeline:</strong> From raw data collection to model deployment</li>
            <li><strong>Full-Stack Development:</strong> Backend API design with frontend user interface</li>
            <li><strong>Machine Learning:</strong> Feature engineering, model selection, and performance evaluation</li>
            <li><strong>Software Engineering:</strong> Code organization, version control, and documentation</li>
            <li><strong>Problem Solving:</strong> Handling real-world data inconsistencies and edge cases</li>
          </ul>
        </section>

        <section>
          <h2>Important Disclaimers</h2>
          <p>
            This application is designed for <strong>educational and entertainment purposes only</strong>. 
            While the model uses sophisticated analysis of thousands of NBA games, basketball remains inherently unpredictable.
          </p>
          <p>
            Predictions cannot account for real-time factors such as:
          </p>
          <ul>
            <li>Player injuries, rest, or lineup changes</li>
            <li>Team motivation, rivalries, or playoff implications</li>
            <li>Coaching strategies and in-game adjustments</li>
            <li>Individual player performance variations</li>
            <li>External factors like travel, weather, or crowd influence</li>
          </ul>
          <p>
            <em>The model provides data-driven insights based on historical patterns, but basketball's 
            excitement comes from its unpredictability. Any team can win on any given night!</em>
          </p>
        </section>

        <section>
          <h2>Future Enhancements</h2>
          <p>
            Potential improvements for future versions include:
          </p>
          <ul>
            <li><strong>Real-time NBA schedule integration</strong> for actual upcoming games</li>
            <li><strong>Player injury and availability data</strong> for more accurate predictions</li>
            <li><strong>Individual player performance tracking</strong> to enhance game predictions</li>
          </ul>
        </section>
      </div>
    </div>
  )
}

export default About