from pathlib import Path

IDENTIFIERS = ['player_id','player_name','season','league','team','primary_position']
def output_data(df,rolespec,metadata=None):
    """
    
    Cleans up Data for further use.
    Dataframe provided is that produced by role_fit_flags.py
    Provides the following files:
    - analysisdetail.txt
    - players_all.csv (all players with: identifiers, fit_score, is_good_example, key role features)
    - players_good.csv (only good examples, sorted by fit_score descending)
    """
    PROJECT_ROOT = Path(__file__).resolve().parents[3]

    output_dir = PROJECT_ROOT / "outputs" / rolespec.role_name

    output_dir.mkdir(parents=True,exist_ok=True)
    key_features = rolespec.final_features
    identifiers = IDENTIFIERS
    all_columns = identifiers + ['fit_score','is_good_example'] + key_features
    df_out = df[all_columns].copy()
    df_out.to_csv(f"{output_dir}/players_all.csv",index=False)
    df_good = df_out[df_out['is_good_example']].copy()
    df_good = df_good.sort_values('fit_score',ascending=False)
    df_good.to_csv(f"{output_dir}/players_good.csv",index=False)

    with open(f"{output_dir}/analysisdetail.txt","w") as f:
        f.write("Role Analysis Detail\n")
        f.write("====================\n\n")
        f.write(f"Role Name: {rolespec.role_name}\n\n")
        f.write(f"Description:\n{rolespec.description}\n\n")
        f.write(f"Number of players analysed: {len(df)}\n")
        f.write(f"Number of good examples found: {df['is_good_example'].sum()}\n\n")
        if metadata:
            f.write("Additional Metadata:\n")
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")
        