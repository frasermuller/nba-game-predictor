import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class NBAFeatureExtractor:
    def __init__(self, nba_games_path='data/nba_games.csv'):
        """Load and prepare NBA games data for feature extraction"""
        print("🏀 Loading NBA games data...")
        
        self.df = pd.read_csv(nba_games_path, index_col=0)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values(['team', 'date']).reset_index(drop=True)
        
        # Remove all usage rate columns completely
        self.remove_usage_columns()
        
        # Create rolling averages for clean features only
        self.create_rolling_features()
        
        print(f"✅ Loaded {len(self.df)} games, prepared rolling features")
    
    def remove_usage_columns(self):
        """Remove all usage rate related columns"""
        print("🗑️ Removing all usage rate columns...")
        
        usage_cols = [col for col in self.df.columns if 'usg' in col.lower()]
        print(f"Removing {len(usage_cols)} usage columns: {usage_cols}")
        
        self.df = self.df.drop(columns=usage_cols, errors='ignore')
        
        print(f"Remaining columns: {len(self.df.columns)}")
    
    def create_rolling_features(self):
        """Create rolling 10-game averages for clean numeric features"""
        print("📊 Creating rolling 10-game averages...")
        
        # Core basketball stats that are always numeric
        core_features = [
            'fg', 'fga', 'fg%', '3p', '3pa', '3p%', 'ft', 'fta', 'ft%',
            'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts',
            'ts%', 'efg%', '+/-'
        ]
        
        # Only use features that actually exist and are numeric
        available_features = []
        for feature in core_features:
            if feature in self.df.columns and pd.api.types.is_numeric_dtype(self.df[feature]):
                available_features.append(feature)
        
        print(f"Creating rolling averages for {len(available_features)} features")
        
        # Add won column (boolean converted to numeric)
        if 'won' in self.df.columns:
            self.df['won'] = self.df['won'].astype(float)
            available_features.append('won')
        
        # Create rolling averages
        for feature in available_features:
            self.df[f'{feature}_10_x'] = (
                self.df.groupby('team')[feature]
                .rolling(10, min_periods=1)
                .mean()
                .reset_index(0, drop=True)
            )
        
        # Rolling for max player stats (only numeric ones)
        max_features = []
        for col in self.df.columns:
            if col.endswith('_max') and not col.endswith('_opp') and pd.api.types.is_numeric_dtype(self.df[col]):
                if 'usg' not in col.lower():  # Skip any remaining usage stats
                    max_features.append(col)
        
        print(f"Creating rolling averages for {len(max_features)} max features")
        
        for feature in max_features:
            self.df[f'{feature}_10_x'] = (
                self.df.groupby('team')[feature]
                .rolling(10, min_periods=1)
                .mean()
                .reset_index(0, drop=True)
            )
        
        # Rolling for opponent stats (clean numeric only)
        opp_features = []
        for col in self.df.columns:
            if col.endswith('_opp') and not col.endswith('_max_opp') and pd.api.types.is_numeric_dtype(self.df[col]):
                if 'usg' not in col.lower():
                    opp_features.append(col)
        
        print(f"Creating rolling averages for {len(opp_features)} opponent features")
        
        for feature in opp_features:
            base_name = feature.replace('_opp', '')
            self.df[f'{base_name}_opp_10_x'] = (
                self.df.groupby('team')[feature]
                .rolling(10, min_periods=1)
                .mean()
                .reset_index(0, drop=True)
            )
        
        print("✅ Rolling features created successfully")
    
    def get_team_features(self, team, opponent, is_home=True):
        """Extract available features for a team vs opponent matchup"""
        
        # Get recent games for both teams
        team_games = self.df[self.df['team'] == team].tail(5)
        opp_games = self.df[self.df['team'] == opponent].tail(5)
        
        if len(team_games) == 0 or len(opp_games) == 0:
            print(f"⚠️ No recent games found for {team} or {opponent}")
            return None
        
        # Use most recent game's rolling averages
        latest_team = team_games.iloc[-1]
        latest_opp = opp_games.iloc[-1]
        
        features = {}
        
        # Basic team stats
        features['fga'] = latest_team.get('fga', 85.0)
        features['fg_opp'] = latest_opp.get('fg', 40.0)
        features['orb_opp'] = latest_opp.get('orb', 10.0)
        features['stl%_opp'] = latest_opp.get('stl%', 0.08)
        features['pf_max_opp'] = latest_opp.get('pf_max', 6.0)
        features['orb%_max_opp'] = latest_opp.get('orb%_max', 0.15)
        
        # Rolling features that exist (avoiding usage rates)
        features['efg%_10_x'] = latest_team.get('efg%_10_x', latest_team.get('efg%', 0.52))
        features['fg_max_10_x'] = latest_team.get('fg_max_10_x', latest_team.get('fg_max', 15.0))
        features['+/-_max_10_x'] = latest_team.get('+/-_max_10_x', latest_team.get('+/-_max', 5.0))
        features['trb%_max_10_x'] = latest_team.get('trb%_max_10_x', latest_team.get('trb%_max', 0.25))
        
        # Rolling opponent features
        features['blk_opp_10_x'] = latest_team.get('blk_opp_10_x', latest_team.get('blk_opp', 5.0))
        features['drb%_opp_10_x'] = latest_team.get('drb%_opp_10_x', latest_team.get('drb%_opp', 0.75))
        features['ft%_max_opp_10_x'] = latest_team.get('ft%_max_opp_10_x', latest_team.get('ft%_max_opp', 0.8))
        features['+/-_max_opp_10_x'] = latest_team.get('+/-_max_opp_10_x', latest_team.get('+/-_max_opp', -5.0))
        features['efg%_max_opp_10_x'] = latest_team.get('efg%_max_opp_10_x', latest_team.get('efg%_max_opp', 0.55))
        
        # Home court advantage
        features['home_next'] = 1 if is_home else 0
        
        # Team Y features (opponent perspective)
        features['mp_10_y'] = latest_opp.get('mp_10_x', 240.0)
        features['gmsc_max_10_y'] = latest_opp.get('gmsc_max_10_x', latest_opp.get('gmsc_max', 15.0))
        features['blk%_opp_10_y'] = latest_opp.get('blk%_opp_10_x', latest_opp.get('blk%_opp', 0.06))
        features['ft%_max_opp_10_y'] = latest_opp.get('ft%_max_opp_10_x', latest_opp.get('ft%_max_opp', 0.8))
        features['ast_max_opp_10_y'] = latest_opp.get('ast_max_opp_10_x', latest_opp.get('ast_max_opp', 8.0))
        features['+/-_max_opp_10_y'] = latest_opp.get('+/-_max_opp_10_x', latest_opp.get('+/-_max_opp', -3.0))
        
        return features
    
    def get_prediction_features(self, home_team, away_team):
        """Get features in order the model expects (excluding usage rates)"""
        
        # Get features for home team vs away team
        feature_dict = self.get_team_features(home_team, away_team, is_home=True)
        
        if feature_dict is None:
            return None
        
        # Create a list of available features (no usage rates)
        available_features = [
            'fga', 'fg_opp', 'orb_opp', 'stl%_opp', 'pf_max_opp', 'orb%_max_opp',
            'efg%_10_x', 'fg_max_10_x', '+/-_max_10_x', 'trb%_max_10_x', 'blk_opp_10_x',
            'drb%_opp_10_x', 'ft%_max_opp_10_x', '+/-_max_opp_10_x', 'efg%_max_opp_10_x',
            'home_next', 'mp_10_y', 'gmsc_max_10_y', 'blk%_opp_10_y',
            'ft%_max_opp_10_y', 'ast_max_opp_10_y', '+/-_max_opp_10_y'
        ]
        
        # Return features in order
        features = []
        for feature_name in available_features:
            if feature_name in feature_dict:
                features.append(feature_dict[feature_name])
            else:
                # Reasonable defaults based on NBA averages
                if 'fg%' in feature_name:
                    features.append(0.45)
                elif 'ft%' in feature_name:
                    features.append(0.75)
                elif '%' in feature_name:
                    features.append(0.1)
                elif feature_name == 'home_next':
                    features.append(1)
                elif feature_name == 'mp_10_y':
                    features.append(240.0)
                else:
                    features.append(5.0)
        
        return features

# Test the feature extractor
if __name__ == "__main__":
    extractor = NBAFeatureExtractor()
    
    # Test feature extraction
    features = extractor.get_prediction_features('CLE', 'UTA')
    print(f"\n🎯 Features for CLE vs UTA:")
    print(f"Length: {len(features)}")
    print(f"Sample: {features[:10]}")
    
    # Show feature names and values
    available_features = [
        'fga', 'fg_opp', 'orb_opp', 'stl%_opp', 'pf_max_opp', 'orb%_max_opp',
        'efg%_10_x', 'fg_max_10_x', '+/-_max_10_x', 'trb%_max_10_x', 'blk_opp_10_x',
        'drb%_opp_10_x', 'ft%_max_opp_10_x', '+/-_max_opp_10_x', 'efg%_max_opp_10_x',
        'home_next', 'mp_10_y', 'gmsc_max_10_y', 'blk%_opp_10_y',
        'ft%_max_opp_10_y', 'ast_max_opp_10_y', '+/-_max_opp_10_y'
    ]
    
    print(f"\n📊 Feature breakdown:")
    for i, (name, value) in enumerate(zip(available_features, features)):
        print(f"{i+1:2d}. {name:<20}: {value:.3f}")