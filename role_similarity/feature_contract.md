Transformations:
2) stat->statp90    TODO
    input: count stat column, player minutes
    output: statp90 column
3) possession adjustment TODO
    input: statp90 column, team_pos_pct
    output: statp90_padj column (do not adjust stats which do not depend on team possession as much)
    detail:
        scale to a 50% baseline (ie stat_padj = stat / (team_pos_pct/50))
        stats to adjust: pressures, defensive actions, touches carries, key passes (add if necessary)
4) ratio features   TODO
    input: stat x, stat y (e.g touches wide and touches central)
    output: number of ys per x 
    ratio = y / (x+eps)
    detail:
        add small epsilon to avoid divide by 0
        cap large ratios
5) Standardisation TODO
    input: list of feature columns
    output: *_z columns 
    detail:
        standardise accross combined sample (possibly add alternate within league in future)
        standardise after all adjustments
        drop players with missing values for now
        keep originals, standardisation helpful for similarity but want to be able to also look at specific numbers to compare 
        standardise on analysis dataset (sample)

RoleSpec contains base stats and which transforms to apply 

Name Scheme:
    stat
    stat_p90
    stat_p90_padj
    stat_p90_padj_z


    