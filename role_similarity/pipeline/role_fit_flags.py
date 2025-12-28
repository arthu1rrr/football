import pandas as pd
import numpy as np

Z_SPAN = 2.5

def role_fit_flags(df_features,rules,min_score=0.7):
    """
    Structure of a rule::
    { 
       "feature" : "nameofstat",
       "type" : "percentile" | "absolute", 
       "threshold" : 0.65,
       "op" : "gte" | "lte",
       "weight" : 0.0-1.0,
       "required" : bool,
    }
    Rules = list of rule dicts
    Produce metrics for defining when a player represents a good example of the selected role (e.g strikers who do not make wide runs are not good examples of channel forwards)
    We want to produce:
    1. per rule pass/fail flags
    2. severity score for each rule (how much over the threshold)
    3. summary score for each player
    4. final fit flag based on min_score (is_good_example)
    5. cutoff score for each rule
    NaNs already dropped, assume good input.
    Return dataframe and metadata about cutoffs
    If a required rule is failed, player automatically fails
    Use z scores to determine severity
    Percentile rules, threshold is percentile cutoff
    Absolute rules, threshold is absolute value cutoff
    1. for percentile rules, compute the cutoff value for the given percentile

    """
    columns_to_keep = df_features.columns.tolist()
    metadata = {}
    required_flag_cols = []
    out = df_features.copy()
    contrib_cols = []
    for i,rule in enumerate(rules):
        feature = rule["feature"]
        rule_id = f"{i}_{feature}"
        rule_type = rule["type"]
        threshold = rule["threshold"]
        op = rule["op"]
        weight = rule.get("weight", 1.0)
        required = rule.get("required", False)
        flag_col = f"rule_{rule_id}_pass"
        severity_col = f"rule_{rule_id}_severity"
        contrib_col = f"rule_{rule_id}_contrib"
        z_col = f"{feature}_z"
        columns_to_keep.extend([flag_col, severity_col])
        # Determine cutoff
        if rule_type == "percentile":
            cutoff_value = np.percentile(out[feature], threshold*100)
        elif rule_type == "absolute":
            cutoff_value = threshold
        else:
            raise ValueError(f"Unknown rule type: {rule_type}")
        metadata[rule_id] = {
            "feature": feature,
            "type": rule_type,
            "op": op,
            "threshold": threshold,
            "cutoff_value": cutoff_value,
            "weight": weight,
            "required": required,
            }
        #Compute pass/fail column
        if op == "gte":
            out[flag_col] = out[feature] >= cutoff_value
        elif op == "lte":
            out[flag_col] = out[feature] <= cutoff_value
        if required:
            required_flag_cols.append(flag_col)
        mean = out[feature].mean()
        std = out[feature].std(ddof=0)
        #compute z cutoff
        z_cutoff = (cutoff_value - mean) / std if std > 0 else 0.0
        #we already have z scores for feature stored in z_col
        #severity is distance past cutoff in z-units clipped to [0,1]
        if op == "gte":
            out[severity_col] = np.clip((out[z_col] - z_cutoff) / Z_SPAN, 0, 1)
        elif op == "lte":
            out[severity_col] = np.clip((z_cutoff - out[z_col]) / Z_SPAN, 0, 1)
        out[contrib_col] = out[severity_col] * weight
        contrib_cols.append(contrib_col)
    total_weight = sum([rule.get("weight",1.0) for rule in rules])




    #after loop
    #compute a single required pass column 
    if required_flag_cols:
        out["required_pass"] = out[required_flag_cols].all(axis=1)
    else:
        out["required_pass"] = True
    #compute total score column
    if total_weight == 0:
        out["fit_score"] = 0.0
    else:
        out["fit_score"] = out[contrib_cols].sum(axis=1) / total_weight
    
    #compute final is_good_example flag
    out["is_good_example"] = (out["fit_score"] >= min_score) & out["required_pass"]
    columns_to_keep.extend(["fit_score","is_good_example","required_pass"])
    out = out[columns_to_keep]
    return out, metadata



    

        
        


        