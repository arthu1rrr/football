from role_similarity.core.features import add_z_standardisation
def add_zscores(df,features):
    """
    Adds z-scores for specified columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    score_columns (list): List of column names to compute z-scores for.

    Returns:
    pd.DataFrame: DataFrame with added z-score columns.
    """
    return add_z_standardisation(df, features)
    