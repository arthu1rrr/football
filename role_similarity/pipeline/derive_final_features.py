import numpy as np
import pandas as pd
from role_similarity.core.config import TRANSFORM_POLICY
from role_similarity.core.features import add_stat_p90, add_stat_padj,add_stat_ratio,drop_players_with_nan_stats

def derive_final_features(df,rolespec):
    """
    Derives final features for a given rolespec
    Inputs:
        df - input data 
        rolespec - RoleSpec object defining the role
    Output:
        DataFrame with final features added

    Ratio features must be split into their components first
    1. Identify ratio features in rolespec.final_features
    2. For each ratio feature, identify the numerator and denominator stats
    
    3. Find base stats from rest of final features
    4. apply p90 to applicable base stats using the TRANSFORM_POLICY
    5. apply padj to applicable p90 stats using the TRANSFORM_POLICY
    6. compute ratio features from their components
    7. drop players with NaN in any final feature
    8. return final DataFrame 
    """
    out = df.copy()
    features = rolespec.final_features

    base_stats = []
    # Step 1: Identify ratio features
    for feature in features:
        if "_to_" in feature:
            stat_x, stat_y = feature.split("_to_")
            
            base_stats.extend([stat_x.replace("_p90","").replace("_padj",""), stat_y.replace("_p90","").replace("_padj","")])
        else:
            base_stats.append(feature.replace("_p90","").replace("_padj",""))
    base_stats = list(set(base_stats)) #unique base stats
    p_90_stats = []
    p_adj_stats = []
    for stat in base_stats:

        transform_cfg = TRANSFORM_POLICY.get(stat, {})
        marker = False
        if transform_cfg.get("per90", False):
            p_90_stats.append(stat)
            marker = True

        if transform_cfg.get("padj", False):
            if marker:
                p_adj_stats.append(f"{stat}_p90")
            else:
                p_adj_stats.append(stat)
    # Step 4: apply p90 to applicable base stats

    out = add_stat_p90(out, p_90_stats)
    # Step 5: apply padj to applicable stats
    out = add_stat_padj(out, p_adj_stats)
    # Step 6: compute ratio features from their components
    for feature in features:
        if "_to_" in feature:
            stat_x, stat_y = feature.split("_to_")
            out = add_stat_ratio(out, stat_x, stat_y)

    # Step 7: drop players with NaN in any final feature
    out = drop_players_with_nan_stats(out, features)

    return out


