class RoleSpec:
    """
    declares:
    - which players to include (positionally)
    - what data required
    - features which define this role

    """
    def __init__(
            self,
            role_name: str,
            description: str,
            *,
            min_minutes: int = 900,
            positions: list[str], #e.g. ['ST','CAM']
            required_columns: list[str], #Raw data and stats required
            final_features: list[str]): #feature columns derived
        self.role_name = role_name
        self.description = description
        self.min_minutes = min_minutes
        self.positions = positions
        self.required_columns = required_columns
        self.final_features = final_features


def validate_rolespec(rolespec,data_columns,feature_columns):
    """
    validates a rolespec instance 
    Inputs:
        rolespec - RoleSpec instance to validate
    Outputs:
        Exceptions
    
    Checks:
        - role_name is non-empty string
        - description is non-empty string
        - min_minutes is non-negative integer
        - positions is non-empty list of non-empty strings
        - required_columns is non-empty list of non-empty strings
        - final_features is non-empty list of non-empty strings
        - no duplicates in positions, required_columns, final_features

        - all required_columns are in data_columns
        - all final_features are in feature_columns

        

       
    """
    if not isinstance(rolespec.role_name, str) or not rolespec.role_name:
        raise ValueError("role_name must be a non-empty string")
    if not isinstance(rolespec.description, str) or not rolespec.description:
        raise ValueError("description must be a non-empty string")
    if not isinstance(rolespec.min_minutes, int) or rolespec.min_minutes <= 0:
        raise ValueError("min_minutes must be a non-negative integer")
    if (not isinstance(rolespec.positions, list) or not rolespec.positions or
            not all(isinstance(pos, str) and pos for pos in rolespec.positions)):
        raise ValueError("positions must be a non-empty list of non-empty strings")
    if (not isinstance(rolespec.required_columns, list) or not rolespec.required_columns or
            not all(isinstance(col, str) and col for col in rolespec.required_columns)):
        raise ValueError("required_columns must be a non-empty list of non-empty strings")
    if (not isinstance(rolespec.final_features, list) or not rolespec.final_features or
            not all(isinstance(feat, str) and feat for feat in rolespec.final_features)):
        raise ValueError("final_features must be a non-empty list of non-empty strings")

    if len(set(rolespec.positions)) != len(rolespec.positions):
        raise ValueError("positions contains duplicates")
    if len(set(rolespec.required_columns)) != len(rolespec.required_columns):
        raise ValueError("required_columns contains duplicates")
    if len(set(rolespec.final_features)) != len(rolespec.final_features):
        raise ValueError("final_features contains duplicates")

    for col in rolespec.required_columns:
        if col not in data_columns:
            raise ValueError(f"required_column {col} not in data_columns")

    for feat in rolespec.final_features:
        if feat not in feature_columns:
            raise ValueError(f"final_feature {feat} not in feature_columns")

    

    