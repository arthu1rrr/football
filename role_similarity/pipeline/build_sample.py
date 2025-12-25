def build_sample(df,rolespec):
    """
    filter dataset according to rolespec requirements 
    
    """
    positions = rolespec.positions
    min_minutes = rolespec.min_minutes
    required_columns = rolespec.required_columns
    needed = set(required_columns)
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"Input dataframe is missing required columns: {missing}")
    new = df.copy()
    # filter by position
    new = new[new['primary_position'].isin(positions)]
    # filter by minutes
    new = new[new['minutes'] >= min_minutes]
    # select required columns
    new = new[required_columns]
    return new