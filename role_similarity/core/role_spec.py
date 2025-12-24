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