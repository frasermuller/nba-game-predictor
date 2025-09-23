# NBA Game Predictor 🏀

A full-stack application that predicts NBA game outcomes using machine learning.

## Features
- Predict game outcomes with confidence scores
- View team statistics and recent performance
- Interactive UI with real-time predictions
- Historical data analysis

## Tech Stack
- **Backend**: Python, Flask, scikit-learn
- **Frontend**: React, Vite, Chart.js
- **ML Model**: Logistic Regression with rolling averages

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/train_model.py  # Train the model
python app.py  # Start Flask server