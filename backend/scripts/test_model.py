import pandas as pd
import joblib
import numpy as np
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_confidence_scores():
    """Test that confidence scores are reasonable"""
    print("Testing Confidence Scores")
    print("=" * 50)

    

import pandas as pd
import joblib
import numpy as np

def test_confidence_scores():
    """Test that confidence scores are reasonable"""
    print("🧪 Testing Confidence Scores")
    print("=" * 50)
    
    # Load model
    model_bundle = joblib.load('logistic_model.pkl')
    model = model_bundle['model']
    predictors = model_bundle['predictors']
    scaler = model_bundle['scaler']
    
    # Load game data
    game_data = pd.read_csv('game_stats.csv')
    
    print(f"Loaded model with {len(predictors)} features")
    print(f"Loaded {len(game_data)} games")
    
    # Test on recent games
    test_games = game_data.tail(100).dropna(subset=predictors)
    
    if len(test_games) == 0:
        print("No valid test games found")
        return
    
    X = test_games[predictors]
    X_scaled = scaler.transform(X)
    
    # Get predictions and probabilities
    predictions = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)
    
    # Calculate confidence for each prediction
    confidences = probabilities.max(axis=1)
    
    print(f"\n Confidence Score Analysis:")
    print(f"  Mean: {confidences.mean():.3f}")
    print(f"  Std Dev: {confidences.std():.3f}")
    print(f"  Min: {confidences.min():.3f}")
    print(f"  Max: {confidences.max():.3f}")
    
    print(f"\n Confidence Distribution:")
    bins = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    hist, _ = np.histogram(confidences, bins=bins)
    
    for i in range(len(bins)-1):
        pct = (hist[i] / len(confidences)) * 100
        print(f"  {bins[i]:.0%} - {bins[i+1]:.0%}: {hist[i]:3d} games ({pct:5.1f}%)")
    
    # Show some example predictions
    print(f"\n Sample Predictions:")
    sample_indices = np.random.choice(len(test_games), min(5, len(test_games)), replace=False)
    
    for idx in sample_indices:
        game = test_games.iloc[idx]
        pred = predictions[idx]
        conf = confidences[idx]
        prob_win = probabilities[idx][1]
        
        print(f"\n  Game: {game['team']} vs {game['team_opp']}")
        print(f"  Prediction: {'Win' if pred == 1 else 'Loss'}")
        print(f"  Confidence: {conf:.1%}")
        print(f"  Win Probability: {prob_win:.1%}")

def test_specific_matchup(team1, team2):
    """Test a specific matchup"""
    print(f"\n Testing Matchup: {team1} vs {team2}")
    print("-" * 40)
    
    # Load model and data
    model_bundle = joblib.load('logistic_model.pkl')
    model = model_bundle['model']
    predictors = model_bundle['predictors']
    scaler = model_bundle['scaler']
    
    game_data = pd.read_csv('game_stats.csv')
    
    # Get latest stats for both teams
    team1_games = game_data[game_data['team'] == team1].tail(1)
    team2_games = game_data[game_data['team'] == team2].tail(1)
    
    if len(team1_games) == 0 or len(team2_games) == 0:
        print(f" Could not find data for one or both teams")
        return
    
    # Create feature vector (simplified for demo purposes)
    features = {}
    
    # Use team1's features as base
    for pred in predictors:
        if pred in team1_games.columns:
            features[pred] = team1_games.iloc[0][pred]
        else:
            features[pred] = 0
    
    # Make prediction
    X = pd.DataFrame([features])[predictors]
    X_scaled = scaler.transform(X)
    
    prediction = model.predict(X_scaled)[0]
    probabilities = model.predict_proba(X_scaled)[0]
    confidence = probabilities.max()
    
    print(f"  Predicted Winner: {team1 if prediction == 1 else team2}")
    print(f"  Confidence: {confidence:.1%}")
    print(f"  {team1} Win Probability: {probabilities[1]:.1%}")
    print(f"  {team2} Win Probability: {probabilities[0]:.1%}")

if __name__ == "__main__":
    # Test overall confidence distribution
    test_confidence_scores()
    
    # Test specific matchups
    test_specific_matchup("LAL", "GSW")
    test_specific_matchup("BOS", "MIA")
    test_specific_matchup("DEN", "PHO")




if __name__ == "__main__":
    test_confidence_scores()
