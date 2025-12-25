def cleanup(df,identifiers,features):
    """
    Drops intermediate columns (columns which have been further processed using p90 and/or team pos adjusted)
    """
    keep = identifiers + features + [f"{c}_z" for c in features]
    return df[keep]

