import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
import sys
import os

# Add parent directory to path so we can import feature_extractor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from feature_extractor import NBAFeatureExtractor
import joblib

def create_simple_model():
    """Create a simple model using the feature extractor's 22 features"""
    
    print("🎯 CREATING SIMPLE MODEL WITH 22 CLEAN FEATURES...")
    
    # Use the feature extractor to get clean data
    extractor = NBAFeatureExtractor()
    
    # Get all unique teams
    teams = extractor.df['team'].unique()
    print(f"Found {len(teams)} teams: {teams}")
    
    # Create training data by extracting features for historical matchups
    print("📊 Creating training dataset...")
    
    X_data = []
    y_data = []
    
    # Sample recent games to create training pairs
    recent_games = extractor.df[extractor.df['season'] >= 2023].copy()
    
    for idx, row in recent_games.iterrows():
        if idx % 500 == 0:
            print(f"Processing game {idx}/{len(recent_games)}")
            
        home_team = row['team']
        away_team = row['team_opp']
        
        # Extract features for this matchup
        features = extractor.get_prediction_features(home_team, away_team)
        
        if features is not None and len(features) == 22:
            X_data.append(features)
            y_data.append(int(row['won']))  # 1 if home team won, 0 if lost
    
    print(f"✅ Created {len(X_data)} training samples")
    
    if len(X_data) == 0:
        print("❌ No training data created!")
        return None
    
    # Convert to arrays
    X = np.array(X_data)
    y = np.array(y_data)
    
    print(f"Training data shape: {X.shape}")
    print(f"Target distribution: {np.bincount(y)}")
    
    # Scale features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train simple logistic regression
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_scaled, y)
    
    # Test accuracy
    predictions = model.predict(X_scaled)
    accuracy = accuracy_score(y, predictions)
    print(f"📈 Training accuracy: {accuracy:.1%}")
    
    # Feature names that match what the extractor provides
    feature_names = [
        'fga', 'fg_opp', 'orb_opp', 'stl%_opp', 'pf_max_opp', 'orb%_max_opp',
        'efg%_10_x', 'fg_max_10_x', '+/-_max_10_x', 'trb%_max_10_x', 'blk_opp_10_x',
        'drb%_opp_10_x', 'ft%_max_opp_10_x', '+/-_max_opp_10_x', 'efg%_max_opp_10_x',
        'home_next', 'mp_10_y', 'gmsc_max_10_y', 'blk%_opp_10_y',
        'ft%_max_opp_10_y', 'ast_max_opp_10_y', '+/-_max_opp_10_y'
    ]
    
    # Save model bundle (note the path change - now we're in scripts/ so go up one level)
    models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_bundle = {
        'model': model,
        'scaler': scaler,
        'predictors': feature_names
    }
    
    model_path = os.path.join(models_dir, 'simple_clean_model.pkl')
    joblib.dump(model_bundle, model_path)
    print(f"💾 Simple model saved to {model_path}")
    
    # Test a few predictions
    print("\n🧪 Testing predictions...")
    test_teams = [('CLE', 'UTA'), ('GSW', 'LAL'), ('BOS', 'MIA')]
    
    for home, away in test_teams:
        test_features = extractor.get_prediction_features(home, away)
        if test_features:
            test_scaled = scaler.transform([test_features])
            prob = model.predict_proba(test_scaled)[0][1]
            print(f"{home} vs {away}: {prob:.1%} home win probability")
    
    return model_bundle

if __name__ == "__main__":
    create_simple_model()