from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

IDENTIFIERS = ['player_id','player_name','season','league','team','primary_position']

def find_similar_players(df,rolespec,target_player_ids,top_n=10,target_leagues=None):
    """
    Finds players similar to the target players based on z scores of key features.
    Find top n similar players for each target player in each league in the dataframe.

    """
    similarity_df = pd.DataFrame()
    if not target_leagues:
        target_leagues = df['league'].unique().tolist()
    features = rolespec.final_features
    z_cols = [f"{c}_z" for c in features]
    identifiers = IDENTIFIERS
    cols = identifiers + z_cols
    df = df[cols].copy()
    for player_id in target_player_ids:
        candidates = df.copy()
        candidates = candidates[candidates["player_id"] != player_id]
        target_player = df[df['player_id'] == player_id]
        if target_player.empty:
            print(f"Player ID {player_id} not found in dataframe.")
            continue
        target_vec = target_player[z_cols].values[0]
        #compute cosine similarity 
        candidate_matrix = candidates[z_cols].values
        similarities = cosine_similarity([target_vec],candidate_matrix)[0]
        candidates['similarity'] = similarities
        for league in target_leagues:
            league_candidates = candidates[candidates['league'] == league]
            if league_candidates.empty:
                continue
            top_similar = league_candidates.nlargest(top_n,'similarity')
            top_similar = top_similar[identifiers + ['similarity']]
            top_similar['target_player_id'] = player_id
            similarity_df = pd.concat([similarity_df,top_similar],ignore_index=True)
    return similarity_df


