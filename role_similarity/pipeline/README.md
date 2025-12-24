Lets define our data pipeline, we need it to do a few things:
1) Ensure data is up-to-date *assert_freshness.py*
2) We need to produce our 'sample' data set, filter out unnecessary stats, only look at players in the selected positions *build_sample.py*
3) Produce our final feature columns *derive_final_features.py*
4) Produce standardised z columns *add_zscores.py*
5) drop intermediate columns (columns_to_keep =
    identifiers
  + feature_cols
  + [f"{c}_z" for c in feature_cols]) *cleanup.py*
6) Produce metrics for defining when a player represents a good example of the selected role (e.g strikers who do not make wide runs are not good examples of channel forwards) *role_fit_flags.py*
7) Provide the final features in order for further data analysis (producing graphs, ranking and comparing etc) *output_dfs.py*
8) Use the z values to find similarities between prem and championship players (ie who is the championship version of player x, would he make a good replacement) *find_similar_players.py*

Inputs:
    df (dataframe containing player-season-league table)
    rolespec (declares required columns etc for the role)
    transform_policy (which functions must we apply to which stat)
    identifiers (player id, player name, team etc)
Outputs:
    df_features
    df_z
    df_similarity 

