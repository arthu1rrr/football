from role_similarity.core.role_spec import RoleSpec, validate_rolespec

CHANNEL_FORWARD_ROLESPEC_V1 = RoleSpec(
    role_name="channel_forward_v1",
    description="""A channel forward is a mobile attacker who opereates in half-spaces between full backs and centre backs. 
Instead of holding a central position, channel forwards tend to roam wider to find gaps.
Channel forwards attack space with their runs and destabilise the defensive structures.
Value comes from: Movement, strong pressing, contribution in transitions, combining goal threat with chance creation along with providing defensive support through a press.""",
min_minutes=900,
positions=['ST'],
required_columns=[
    "player_id","player_name","season","league",
    "team","team_pos_pct",
    "minutes",
    "primary_position",
    "npxG","shots","touches_in_box",
    "central_touches","wide_touches",
    "progressive_carries","carries_into_final_third",
    "xA","key_passes",
    "pressures_in_final_third","defensive_actions_final_third",
],
final_features=[
    "npxG_p90",
    "shots_p90",
    "touches_in_box_p90_padj",
    "central_touches_p90_padj_to_wide_touches_p90_padj",
    "progressive_carries_p90_padj",
    "carries_into_final_third_p90_padj",
    "xA_p90",
    "key_passes_p90",
    "pressures_in_final_third_p90_padj",
    "defensive_actions_final_third_p90_padj",
]
)