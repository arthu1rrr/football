import numpy as np
import pandas as pd

def add_stat_p90(
        df: pd.DataFrame, 
        stats_cols: list[str], #e.g ['shots','xG']
        minutes_col: str = "minutes",) -> pd.DataFrame:
    """
    Adds per-90 versions of count stats
    Inputs:
        df - input data 
        stats_cols - list of columns to convert to per-90
        minutes_col - column with minutes played
    Output:
        DataFrame with new per-90 columns added for each applicable stat for each player
    Conventions:
        - minutes NaN -> per-90 stat = NaN
        - minutes < 900 -> per-90 stat = NaN
    
    """
    for col in [minutes_col, *stats_cols]:
        if col not in df.columns:
            raise ValueError(f"Column {col} not in DataFrame") #makes sure all columns are present
    out = df.copy() #to avoid modifying original df
    minutes = pd.to_numeric(out[minutes_col], errors="coerce").astype(float) #convert minutes to numeric
    valid = minutes > 899  # at least 900 minutes played
    for stat in stats_cols:
        stat_values = pd.to_numeric(out[stat], errors="coerce").astype(float) #convert stat to numeric
        per90 = np.full(len(out), np.nan) #initialize per90 array with NaNs
        per90[valid.to_numpy()] = stat_values[valid] * 90 / (minutes[valid]).to_numpy() #calculate per90 only for valid entries
        out[f"{stat}_p90"] = per90 #add new per90 column to DataFrame
    return out

def add_stat_padj(
        df: pd.DataFrame, # input data which includes team and team_pos_pct columns despite wasted memory for ease of programming
        stats_cols: list[str], #e.g ['pressures_p90','touches_p90','carries'] (relevant stats to adjust)
        )-> pd.DataFrame:
    """
    Adds team average possession adjusted versions of applicable stats
    Inputs:
        df - input data 
        stats_cols - list of columns to convert to possession adjusted
        teamdf - DataFrame with team possession percentages

    Output:
        DataFrame with new possession adjusted columns added for each applicable stat for each player
    Conventions:
        - scale to a 50% baseline (ie stat_padj = stat / (team_pos_pct/50))
    """
    for col in stats_cols:
        if col not in df.columns:
            raise ValueError(f"Column {col} not in DataFrame") #makes sure all columns are present
    
    out = df.copy() #to avoid modifying original df
    team_pos_pct = pd.to_numeric(out["team_pos_pct"], errors="coerce").astype(float) #convert team_pos_pct to numeric
    for stat in stats_cols:
        stat_values = pd.to_numeric(out[stat], errors="coerce").astype(float) #convert stat to numeric
        padj = stat_values * (50 / team_pos_pct) #calculate possession adjusted stat
        out[f"{stat}_padj"] = padj #add new possession adjusted column to DataFrame
    return out

def add_stat_ratio(
        df: pd.DataFrame,
        stat_x: str, # e.g 'passes_completed_p90'
        stat_y: str, # e.g 'passes_attempted_p90'
) -> pd.DataFrame:
    """
    Adds ratio of two stats as a new column
    Inputs:
        df - input data 
        stat_x - numerator stat column
        stat_y - denominator stat column

    Output:
        DataFrame with new ratio column added for each applicable stat for each player
    Conventions:
        - add small epsilon to avoid divide by 0
        - cap large ratios
    """
    EPSILON = 0.001
    MAX_RATIO = 20.0


    for col in [stat_x, stat_y]:
        if col not in df.columns:
            raise ValueError(f"Column {col} not in DataFrame") #makes sure all columns are present
    
    out = df.copy() #to avoid modifying original df
    x_values = pd.to_numeric(out[stat_x], errors="coerce").astype(float) #convert stat_x to numeric
    y_values = pd.to_numeric(out[stat_y], errors="coerce").astype(float) #convert stat_y to numeric
    ratio = x_values / (y_values + EPSILON) #calculate ratio, add epsilon to denominator to avoid divide by 0
    ratio = np.clip(ratio, 0, MAX_RATIO) #cap large ratios
    out[f"{stat_x}_to_{stat_y}_ratio"] = ratio #add new ratio column to DataFrame
    return out

def drop_players_with_nan_stats(
        df: pd.DataFrame,
        stats_cols: list[str], #e.g ['xG_p90','touches_p90_padj','widetouches_p90_padj_to_touches_p90_padj']
) -> pd.DataFrame:
    """
    Drops players with NaN stats in any of the specified columns
    Inputs:
        df - input data 
        stats_cols - list of columns to check for NaN values
    Output:
        DataFrame with players with NaN stats dropped
    """
    for col in stats_cols:
        if col not in df.columns:
            raise ValueError(f"Column {col} not in DataFrame") #makes sure all columns are present
    
    out = df.copy() #to avoid modifying original df
    out = out.dropna(subset=stats_cols) #drop players with NaN in any of the specified columns
    return out

def add_z_standardisation(
        df: pd.DataFrame,
        stats_cols: list[str], #e.g[xG_p90,touches_p90_padj,widetouches_p90_padj_to_touches_p90_padj]
) -> pd.DataFrame:
    """
    Adds z-score standardisation for specified stats so that similar players can be compared
    Inputs:
        df - input data (NaN stats already dropped)
        stats_cols - list of columns to standardise
    Output:
        DataFrame with new z-score columns added for each applicable stat for each player
    Conventions:
        - Standardise across combined sample
        - Standardise across analysis dataset (ie strikers or midfielders)
        - drop players with NaN stats from dataset before standardisation
        - stat_z = (stat - mean) / std
    """
    for col in stats_cols:
        if col not in df.columns:
            raise ValueError(f"Column {col} not in DataFrame") #makes sure all columns are present
    
    out = df.copy() #to avoid modifying original df
    for stat in stats_cols:
        stat_values = pd.to_numeric(out[stat], errors="coerce").astype(float) #convert stat to numeric
        valid = ~stat_values.isna() #identify valid (non-NaN) entries
        mean = stat_values[valid].mean() #calculate mean for valid entries
        std = stat_values[valid].std(ddof=0) #calculate std for valid entries
        z_scores = np.full(len(out), np.nan) #initialize z-scores array with NaNs
        z_scores[valid.to_numpy()] = (stat_values[valid] - mean) / std #calculate z-scores only for valid entries
        out[f"{stat}_z"] = z_scores #add new z-score column to DataFrame
    return out