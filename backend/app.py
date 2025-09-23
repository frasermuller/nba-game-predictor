from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)
CORS(app, origins=['http://localhost:5174', 'http://localhost:5173'])

# Load model and data
model_bundle = joblib.load('models/logistic_model.pkl')
model = model_bundle['model'] 
scaler = model_bundle['scaler']
all_features = model_bundle['predictors']

team_stats = pd.read_csv('data/team_stats.csv')
game_stats = pd.read_csv('data/game_stats.csv')

# Remove ALL 8 usage rate features - they don't make sense for team stats
USAGE_FEATURES_TO_REMOVE = [
    'usg%', 'usg%_opp', 'usg%_10_x', 'usg%_opp_10_x', 
    'usg%_max_opp_10_x', 'usg%_10_y', 'usg%_opp_10_y', 'usg%_max_opp_10_y'
]

# These 22 features have good variance and make sense for teams
GOOD_FEATURES = [
    'fga', 'fg_opp', 'orb_opp', 'stl%_opp', 'pf_max_opp', 'orb%_max_opp', 
    'efg%_10_x', 'fg_max_10_x', '+/-_max_10_x', 'trb%_max_10_x', 'blk_opp_10_x', 
    'drb%_opp_10_x', 'ft%_max_opp_10_x', '+/-_max_opp_10_x', 'efg%_max_opp_10_x', 
    'home_next', 'mp_10_y', 'gmsc_max_10_y', 'blk%_opp_10_y', 
    'ft%_max_opp_10_y', 'ast_max_opp_10_y', '+/-_max_opp_10_y'
]

print(f"  Removing {len(USAGE_FEATURES_TO_REMOVE)} usage features")
print(f" Using {len(GOOD_FEATURES)} good team features")

def get_feature_value(feature, home_recent, away_recent):
    """Get feature value from game data"""
    
    if feature == 'home_next':
        return 1  # Home court advantage
    
    # Use good features from game data
    if feature in home_recent.index:
        if not feature.endswith('_y'):
            return float(home_recent[feature])
        else:
            # For _y features (away team stats), use away team's _x equivalent
            away_feature = feature.replace('_y', '_x')
            if away_feature in away_recent.index:
                return float(away_recent[away_feature])
            else:
                return float(home_recent.get(feature, 0.5))
    elif feature in away_recent.index:
        return float(away_recent[feature])
    else:
        return 0.5

@app.route('/api/predict', methods=['POST'])
def predict_game():
    data = request.get_json()
    home_team = data['home_team']
    away_team = data['away_team']
    
    try:
        home_games = game_stats[game_stats['team'] == home_team]
        away_games = game_stats[game_stats['team'] == away_team]
        
        if len(home_games) == 0 or len(away_games) == 0:
            raise ValueError(f"No game data found for {home_team} or {away_team}")
        
        home_recent = home_games.iloc[-1]
        away_recent = away_games.iloc[-1]
        
        # Create features array for the model (30 features expected)
        features = []
        
        for feature in all_features:
            if feature in USAGE_FEATURES_TO_REMOVE:
                # Replace removed usage features with neutral values
                features.append(20.0)  # Neutral usage rate
            elif feature in GOOD_FEATURES:
                # Use actual data for good features
                value = get_feature_value(feature, home_recent, away_recent)
                features.append(value)
            else:
                # Default for any other missing features
                features.append(0.5)
        
        print(f"\n PREDICTION: {home_team} (home) vs {away_team} (away)")
        print(f" Using {len(GOOD_FEATURES)} real features + {len(USAGE_FEATURES_TO_REMOVE)} neutral replacements")
        
        # Show key features being used
        key_examples = []
        sample_features = ['fga', 'fg_opp', 'efg%_10_x', '+/-_max_10_x', 'orb_opp']
        for sf in sample_features:
            if sf in GOOD_FEATURES:
                value = get_feature_value(sf, home_recent, away_recent)
                key_examples.append(f"{sf}: {value:.2f}")
        
        print(f" Key features: {', '.join(key_examples)}")
        
        # Make prediction
        features_scaled = scaler.transform([features])
        home_win_prob = model.predict_proba(features_scaled)[0][1]
        away_win_prob = 1 - home_win_prob
        
        winner = home_team if home_win_prob > 0.5 else away_team
        
        # Enhanced score prediction using team stats
        home_team_stats = team_stats[team_stats['Team'] == home_team].iloc[0]
        away_team_stats = team_stats[team_stats['Team'] == away_team].iloc[0]
        
        # Base on team averages, adjust by prediction confidence
        home_base = home_team_stats['PTS']
        away_base = away_team_stats['PTS']
        
        # Adjust scores based on win probability
        prob_impact = (home_win_prob - 0.5) * 20  # Scale factor
        home_score = int(home_base + prob_impact)
        away_score = int(away_base - prob_impact)
        
        print(f" RESULT: {home_team} {home_win_prob:.1%} vs {away_team} {away_win_prob:.1%}")
        print(f" SCORE: {home_team} {home_score} - {away_team} {away_score}")
        
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
        print(f" Prediction error: {e}")
        
        # Enhanced fallback using current team performance
        try:
            home_team_stats = team_stats[team_stats['Team'] == home_team].iloc[0]
            away_team_stats = team_stats[team_stats['Team'] == away_team].iloc[0]
            
            # Calculate team strength based on multiple factors
            home_win_pct = home_team_stats['W'] / home_team_stats['GP']
            away_win_pct = away_team_stats['W'] / away_team_stats['GP']
            
            # Factor in offensive and defensive efficiency
            home_off_rating = home_team_stats['PTS'] / 110  # Relative to league average
            away_off_rating = away_team_stats['PTS'] / 110
            
            # Calculate win probability
            strength_diff = (home_win_pct - away_win_pct) * 0.4
            efficiency_diff = (home_off_rating - away_off_rating) * 0.2
            home_advantage = 0.06  # 6% home court advantage
            
            home_win_prob = 0.5 + strength_diff + efficiency_diff + home_advantage
            home_win_prob = max(0.20, min(0.80, home_win_prob))  # Realistic bounds
            
            away_win_prob = 1 - home_win_prob
            winner = home_team if home_win_prob > 0.5 else away_team
            
            print(f"🔄 FALLBACK: Using team stats - {home_team} {home_win_prob:.1%}")
            
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
        except Exception as fallback_error:
            print(f" Fallback error: {fallback_error}")
            return jsonify({
                'winner': home_team,
                'home_team': home_team,
                'away_team': away_team,
                'home_win_probability': 0.55,
                'away_win_probability': 0.45,
                'predicted_score': {'home': 110, 'away': 105}
            })

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