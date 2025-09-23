import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
import joblib
import warnings
import os
import sys

warnings.filterwarnings('ignore')

def load_and_prepare_data(filepath='data/nba_games.csv'):  # Changed back to 'data/nba_games.csv'
    """Load and prepare NBA games data following the video approach"""
    print("📊 Loading NBA games data...")
    df = pd.read_csv(filepath, index_col=0)
    df = df.sort_values("date").reset_index(drop=True)
    cols_to_drop = ["mp.1", "mp_opp.1", "index_opp", "gmsc", "+/-", "mp_max", 
                    "mp_max.1", "gmsc_opp", "+/-_opp", "mp_max_opp", "mp_max_opp.1"]
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns], errors='ignore')
    print(f"Loaded {len(df)} games")
    return df

def create_target_variable(df):
    df = df.copy()
    df["target"] = df.groupby("team")["won"].shift(-1)
    df.loc[pd.isnull(df["target"]), "target"] = 2
    df["target"] = df["target"].astype(int, errors="ignore")
    return df

def handle_missing_values(df):
    df.loc[df["ft%"].isna(), "ft%"] = 0.75
    df.loc[df["ft%_max"].isna(), "ft%_max"] = 1.0
    df.loc[df["+/-_max"].isna(), "+/-_max"] = 0
    df.loc[df["ft%_opp"].isna(), "ft%_opp"] = 0.75
    df.loc[df["ft%_max_opp"].isna(), "ft%_max_opp"] = 1.0
    df.loc[df["+/-_max_opp"].isna(), "+/-_max_opp"] = 0
    return df

def remove_null_columns(df):
    nulls = pd.isnull(df).sum()
    nulls = nulls[nulls > 0]
    valid_columns = df.columns[~df.columns.isin(nulls.index)]
    return df[valid_columns].copy()

def create_rolling_features(df, window=10):
    print(f"Creating rolling features (window={window})...")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    exclude_cols = ['target', 'won', 'season', 'home', 'home_opp']
    rolling_cols = [col for col in numeric_cols if col not in exclude_cols]
    def calculate_rolling_avg(team_df):
        rolling_df = pd.DataFrame(index=team_df.index)
        for col in rolling_cols:
            if col in team_df.columns:
                rolling_df[f"{col}_10"] = team_df[col].shift(1).rolling(window, min_periods=3).mean()
        rolling_df["won_10"] = team_df["won"].shift(1).rolling(window, min_periods=3).mean()
        rolling_df["season_10"] = team_df["season"].shift(window-1)
        return rolling_df
    rolling_dfs = []
    for team in df["team"].unique():
        team_df = df[df["team"] == team].copy()
        team_rolling = calculate_rolling_avg(team_df)
        rolling_dfs.append(team_rolling)
    all_rolling = pd.concat(rolling_dfs).sort_index()
    df = pd.concat([df, all_rolling], axis=1)
    df["won_10"] = df["won_10"].round(1)
    print(f"Added {len([c for c in df.columns if '_10' in c])} rolling features")
    return df

def add_opponent_next_game_info(df):
    print("Adding next game opponent info...")
    def add_col(df, col_name):
        return df.groupby("team")[col_name].transform(lambda x: x.shift(-1))
    df = df.copy()
    df["home_next"] = add_col(df, "home")
    df["team_opp_next"] = add_col(df, "team_opp")
    df["date_next"] = add_col(df, "date")
    return df

def merge_opponent_rolling_stats(df):
    print("Merging opponent rolling statistics...")
    rolling_cols = [col for col in df.columns if col.endswith('_10') and col not in ['won_10', 'season_10']]
    full = df.merge(
        df[rolling_cols + ["team_opp_next", "date_next", "team"]],
        left_on=["team", "date_next"],
        right_on=["team_opp_next", "date_next"],
        suffixes=("_x", "_y")
    )
    print(f" Merged data shape: {full.shape}")
    return full

def select_features(df, target_col="target", n_features=30):
    print(f"Selecting top {n_features} features...")
    removed_columns = ["season", "date", "won", "target", "team", "team_opp", 
                      "team_x", "team_y", "team_opp_next_x", "team_opp_next_y", "date_next"]
    removed_columns = list(df.columns[df.dtypes == "object"]) + removed_columns
    selected_columns = df.columns[~df.columns.isin(removed_columns)]
    df_clean = df.dropna(subset=list(selected_columns) + [target_col])
    df_clean = df_clean[df_clean[target_col] != 2]
    if len(df_clean) < 100:
        print("⚠️ Not enough data for feature selection")
        return list(selected_columns)[:n_features]
    lr = LogisticRegression(max_iter=1000, random_state=42)
    split = TimeSeriesSplit(n_splits=3)
    sfs = SequentialFeatureSelector(
        lr, 
        n_features_to_select=min(n_features, len(selected_columns)),
        direction="forward",
        cv=split,
        n_jobs=-1
    )
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(df_clean[selected_columns])
    y = df_clean[target_col]
    print("Running feature selection (this may take a few minutes)...")
    sfs.fit(X_scaled, y)
    predictors = list(selected_columns[sfs.get_support()])
    print(f"Selected {len(predictors)} features")
    return predictors

def backtest(data, model, predictors, start=2, step=1):
    all_predictions = []
    seasons = sorted(data["season"].unique())
    for i in range(start, len(seasons), step):
        season = seasons[i]
        train = data[data["season"] < season]
        test = data[data["season"] == season]
        train = train[train["target"] != 2]
        test = test[test["target"] != 2]
        if len(train) < 100 or len(test) < 10:
            continue
        model.fit(train[predictors], train["target"])
        preds = model.predict(test[predictors])
        preds = pd.Series(preds, index=test.index)
        probs = model.predict_proba(test[predictors])
        combined = pd.concat([test["target"], preds], axis=1)
        combined.columns = ["actual", "prediction"]
        combined["confidence"] = probs.max(axis=1)
        all_predictions.append(combined)
    return pd.concat(all_predictions)

def train_final_model(df, predictors):
    print("Training final model...")
    train_data = df[df["target"] != 2].copy()
    train_data = train_data.dropna(subset=predictors + ["target"])
    X = train_data[predictors]
    y = train_data["target"]
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    model = LogisticRegression(
        max_iter=1000, 
        random_state=42,
        C=0.1,
        solver='liblinear'
    )
    model.fit(X_scaled, y)
    predictions = backtest(train_data, model, predictors)
    accuracy = accuracy_score(predictions["actual"], predictions["prediction"])
    avg_confidence = predictions["confidence"].mean()
    print(f"Backtest Accuracy: {accuracy:.4f}")
    print(f"Average Confidence: {avg_confidence:.4f}")
    print("\n Confidence Distribution:")
    print(f"  < 60%: {(predictions['confidence'] < 0.6).sum()}")
    print(f"  60-70%: {((predictions['confidence'] >= 0.6) & (predictions['confidence'] < 0.7)).sum()}")
    print(f"  70-80%: {((predictions['confidence'] >= 0.7) & (predictions['confidence'] < 0.8)).sum()}")
    print(f"  80-90%: {((predictions['confidence'] >= 0.8) & (predictions['confidence'] < 0.9)).sum()}")
    print(f"  > 90%: {(predictions['confidence'] > 0.9).sum()}")
    return model, scaler

def save_for_flask_app(df, model, scaler, predictors):
    print("\nSaving files for Flask app...")
    # Save model bundle
    model_bundle = {
        'model': model,
        'predictors': predictors,
        'scaler': scaler
    }
    joblib.dump(model_bundle, 'models/logistic_model.pkl')
    print("Saved logistic_model.pkl")
    # Prepare game stats for Flask app
    # Use correct team columns after merge
    team_col = 'team_x' if 'team_x' in df.columns else 'team'
    team_opp_col = 'team_opp_x' if 'team_opp_x' in df.columns else 'team_opp'
    keep_cols = ['date', team_col, team_opp_col, 'won', 'home'] + predictors
    keep_cols = [col for col in keep_cols if col in df.columns]
    game_stats = df[keep_cols].copy()
    # Rename columns for consistency
    game_stats = game_stats.rename(columns={team_col: 'team', team_opp_col: 'team_opp'})
    game_stats.to_csv('data/game_stats.csv', index=False)
    print("Saved game_stats.csv")
    # Create team stats
    team_mapping = {
        # Eastern Conference - Atlantic Division
        'BOS': ('Eastern', 'Atlantic'), 'BRK': ('Eastern', 'Atlantic'), 
        'NYK': ('Eastern', 'Atlantic'), 'PHI': ('Eastern', 'Atlantic'), 
        'TOR': ('Eastern', 'Atlantic'),
        
        # Eastern Conference - Central Division
        'CHI': ('Eastern', 'Central'), 'CLE': ('Eastern', 'Central'),
        'DET': ('Eastern', 'Central'), 'IND': ('Eastern', 'Central'),
        'MIL': ('Eastern', 'Central'),
        
        # Eastern Conference - Southeast Division
        'ATL': ('Eastern', 'Southeast'), 'CHO': ('Eastern', 'Southeast'),
        'MIA': ('Eastern', 'Southeast'), 'ORL': ('Eastern', 'Southeast'),
        'WAS': ('Eastern', 'Southeast'),
        
        # Western Conference - Northwest Division
        'DEN': ('Western', 'Northwest'), 'MIN': ('Western', 'Northwest'),
        'OKC': ('Western', 'Northwest'), 'POR': ('Western', 'Northwest'),
        'UTA': ('Western', 'Northwest'),
        
        # Western Conference - Pacific Division
        'GSW': ('Western', 'Pacific'), 'LAC': ('Western', 'Pacific'),
        'LAL': ('Western', 'Pacific'), 'PHO': ('Western', 'Pacific'),
        'SAC': ('Western', 'Pacific'),
        
        # Western Conference - Southwest Division
        'DAL': ('Western', 'Southwest'), 'HOU': ('Western', 'Southwest'),
        'MEM': ('Western', 'Southwest'), 'NOP': ('Western', 'Southwest'),
        'SAS': ('Western', 'Southwest')
    }
    teams = game_stats['team'].unique()
    team_stats = []
    for team in teams:
        team_games = game_stats[game_stats['team'] == team]
        recent_games = team_games.tail(10)
        conf, div = team_mapping.get(team, ('Unknown', 'Unknown'))
        team_info = {
            'abbreviation': team,
            'name': team,
            'conference': conf,
            'division': div,
            'games_played': len(team_games),
            'win_rate': float(team_games['won'].mean()),
            'recent_win_rate': float(recent_games['won'].mean()) if len(recent_games) > 0 else 0,
            'avg_points': 0  # Add if you have points data
        }
        team_stats.append(team_info)
    team_stats_df = pd.DataFrame(team_stats)
    team_stats_df.to_csv('data/team_stats.csv', index=False)
    print("Saved team_stats.csv")

if __name__ == "__main__":
    print("NBA Game Predictor - Training Pipeline")
    print("=" * 50)
    df = load_and_prepare_data('data/nba_games.csv')  # Changed back to 'data/nba_games.csv'
    df = create_target_variable(df)
    df = handle_missing_values(df)
    df = remove_null_columns(df)
    df = df.dropna()
    df = create_rolling_features(df)
    df = add_opponent_next_game_info(df)
    df = df.dropna()
    full = merge_opponent_rolling_stats(df)
    predictors = select_features(full)
    model, scaler = train_final_model(full, predictors)
    save_for_flask_app(full, model, scaler, predictors)
    print("\nTraining complete!")
    print("Files created:")
    print("   - models/logistic_model.pkl")
    print("   - data/game_stats.csv")
    print("   - data/team_stats.csv")