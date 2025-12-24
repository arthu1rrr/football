import pandas as pd
from role_similarity.pipeline.cleanup import cleanup
from role_similarity.pipeline.add_zscores import add_zscores
df = pd.DataFrame({
# identifiers
"player_id": [1, 2],
"player_name": ["A", "B"],
"season": [2023, 2023],

# base features
"npxG_p90": [0.4, 0.2],
"shots_p90": [3.1, 2.4],

# z features
"npxG_p90_z": [1.2, -0.4],
"shots_p90_z": [0.9, -0.1],

# intermediate / junk columns
"minutes": [1800, 1900],
"team_pos_pct": [55.0, 48.0],
"npxG": [8.0, 4.2],
})

id_cols = ["player_id", "player_name", "season"]
feature_cols = ["npxG_p90", "shots_p90"]

# Act
out = cleanup(df, id_cols, feature_cols)

#-----------------------------------

df = pd.DataFrame({
    "player_id": [1, 2, 3],
    "npxG_p90": [0.50, 1.00, 1.50],
})
feature_cols = ["npxG_p90"]
out = add_zscores(df, feature_cols)
print(out)


