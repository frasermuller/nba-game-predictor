# NBA Game Predictor

A full-stack web application that predicts NBA game outcomes using machine learning based on historical game data and team statistics.

## Features

- **Real-time Predictions**: Predict NBA game winners with win probabilities
- **Team Statistics**: View comprehensive team stats and performance metrics
- **Historical Data**: Uses rolling averages from thousands of NBA games (2019-2025)
- **Clean Interface**: Modern React frontend with team colors and responsive design
- **Advanced ML**: Logistic regression model with 22 carefully selected features

## Tech Stack

**Frontend:**
- React 18 + Vite
- Modern CSS with team-specific styling
- Responsive design

**Backend:**
- Flask (Python)
- scikit-learn for machine learning
- pandas for data processing
- Real NBA game data with rolling statistics

**Model:**
- Logistic Regression with feature selection
- 22 features including team stats, opponent stats, and rolling averages
- MinMax scaling for optimal performance

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment (use python3 on macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the model (first time only - optional, model already included)
python scripts/train_model.py

# Start the API server
python app.py
```

The backend will run on `http://localhost:3001`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will run on `http://localhost:5174`

## How It Works

1. **Data Processing**: Uses real NBA game data with rolling 10-game averages
2. **Feature Extraction**: Extracts 22 key features including:
   - Team shooting percentages
   - Opponent defensive stats
   - Rolling averages for key metrics
   - Home court advantage
3. **Machine Learning**: Logistic regression model trained on historical matchups
4. **Prediction**: Outputs win probabilities and predicted scores

## Model Features

The model uses these key feature categories:
- **Shooting Stats**: FGA, FG%, EFG%
- **Opponent Defense**: Blocks, steals, defensive rebounds
- **Rolling Averages**: 10-game performance trends
- **Player Impact**: Max player statistics
- **Home Advantage**: Home court factor

## Project Structure

```
nba-game-predictor/
├── backend/
│   ├── app.py                 # Flask API
│   ├── feature_extractor.py   # ML feature extraction
│   ├── scripts/
│   │   └── train_model.py     # Model training
│   ├── models/
│   │   └── simple_clean_model.pkl
│   └── data/
│       ├── nba_games.csv      # Historical game data
│       └── team_stats.csv     # Current team stats
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   └── styles/           # CSS styling
│   └── public/
└── README.md
```

## Development

To retrain the model with new data:

```bash
cd backend
python scripts/train_model.py
```

To add new features:
1. Update `feature_extractor.py`
2. Retrain the model
3. Update the frontend if needed

## Performance

- **Training Accuracy**: ~60-65% (realistic for NBA predictions)
- **Features**: 22 carefully selected features
- **Data**: 8910 NBA games across 7 seasons
- **Response Time**: <100ms per prediction

## Troubleshooting

### Common Issues

**Backend won't start:**
- Make sure you're using `python3` instead of `python` on macOS/Linux
- Ensure virtual environment is activated: `source .venv/bin/activate`

**Frontend styling missing:**
- Make sure you ran `npm install` in the frontend directory
- Try clearing browser cache or hard refresh (Cmd+Shift+R / Ctrl+Shift+R)

**Module not found errors:**
- Activate virtual environment: `source .venv/bin/activate` 
- Reinstall dependencies: `pip install -r requirements.txt`

## License

This project is licensed under the MIT License.

## Acknowledgments

- NBA data sourced from basketball-reference.com
- Built with React and Flask
- ML powered by scikit-learn
