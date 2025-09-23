import pandas as pd
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from feature_extractor import NBAFeatureExtractor

app = Flask(__name__)
CORS(app, origins=['http://localhost:5174', 'http://localhost:5173'])

# Load model and feature extractor
print("🚀 Loading simple model and feature extractor...")
try:
    model_bundle = joblib.load('models/simple_clean_model.pkl')
    model = model_bundle['model']
    scaler = model_bundle['scaler']
    predictors = model_bundle['predictors']
    print(f"✅ Simple model loaded with {len(predictors)} features")
except:
    print("❌ Simple model not found, please run retrain_simple_model.py first")
    model_bundle = None

extractor = NBAFeatureExtractor()
team_stats = pd.read_csv('data/team_stats.csv')

@app.route('/api/predict', methods=['POST'])
def predict_game():
    data = request.get_json()
    home_team = data['home_team']
    away_team = data['away_team']
    
    if model_bundle is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        print(f"\n🏀 CLEAN PREDICTION: {home_team} (home) vs {away_team} (away)")
        
        # Extract real features using actual game data
        features = extractor.get_prediction_features(home_team, away_team)
        
        if features is None:
            raise Exception("Could not extract features for these teams")
        
        print(f"📊 Extracted {len(features)} clean features (no usage rates)")
        print(f"Sample features: {features[:5]}")
        
        # Scale and predict
        features_scaled = scaler.transform([features])
        home_win_prob = model.predict_proba(features_scaled)[0][1]
        away_win_prob = 1 - home_win_prob
        
        winner = home_team if home_win_prob > 0.5 else away_team
        
        # Score prediction based on team stats
        home_team_stats = team_stats[team_stats['Team'] == home_team].iloc[0]
        away_team_stats = team_stats[team_stats['Team'] == away_team].iloc[0]
        
        base_home = home_team_stats['PTS']
        base_away = away_team_stats['PTS']
        
        # Realistic score adjustments
        home_score = int(base_home + (home_win_prob - 0.5) * 20)
        away_score = int(base_away + (away_win_prob - 0.5) * 20)
        
        print(f"🎯 RESULT: {home_team} {home_win_prob:.1%} vs {away_team} {away_win_prob:.1%}")
        print(f"📊 Feature range: {min(features):.2f} to {max(features):.2f}")
        
        return jsonify({
            'winner': winner,
            'home_team': home_team,
            'away_team': away_team,
            'home_win_probability': float(home_win_prob),
            'away_win_probability': float(away_win_prob),
            'predicted_score': {
                'home': home_score,
                'away': away_score
            }
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Enhanced fallback using team stats
        try:
            home_team_stats = team_stats[team_stats['Team'] == home_team].iloc[0]
            away_team_stats = team_stats[team_stats['Team'] == away_team].iloc[0]
            
            home_win_rate = home_team_stats['W'] / home_team_stats['GP']
            away_win_rate = away_team_stats['W'] / away_team_stats['GP']
            
            # Factor in team strength and home advantage
            strength_diff = (home_win_rate - away_win_rate) * 0.4
            home_advantage = 0.06
            
            home_win_prob = 0.5 + strength_diff + home_advantage
            home_win_prob = max(0.25, min(0.75, home_win_prob))
            away_win_prob = 1 - home_win_prob
            
            winner = home_team if home_win_prob > 0.5 else away_team
            
            return jsonify({
                'winner': winner,
                'home_team': home_team,
                'away_team': away_team,
                'home_win_probability': float(home_win_prob),
                'away_win_probability': float(away_win_prob),
                'predicted_score': {
                    'home': int(home_team_stats['PTS']),
                    'away': int(away_team_stats['PTS'])
                }
            })
        except:
            return jsonify({'error': str(e)}), 500

@app.route('/api/teams', methods=['GET'])
def get_teams():
    teams_data = []
    
    for _, team in team_stats.iterrows():
        teams_data.append({
            'name': team['Team'],
            'games_played': int(team['GP']),
            'wins': int(team['W']),
            'losses': int(team['L']),
            'win_percentage': team['W'] / team['GP'],
            'points_per_game': float(team['PTS']),
            'field_goal_percentage': float(team['FG%']),
            'three_point_percentage': float(team['3P%']),
            'free_throw_percentage': float(team['FT%']),
            'rebounds_per_game': float(team['TRB']),
            'assists_per_game': float(team['AST']),
            'steals_per_game': float(team['STL']),
            'blocks_per_game': float(team['BLK']),
            'turnovers_per_game': float(team['TOV'])
        })
    
    return jsonify(teams_data)

if __name__ == '__main__':
    app.run(debug=True, port=3001)