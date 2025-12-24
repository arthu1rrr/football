**GRAIN**: one row per player-season-competition (league only)
Current season only for now.
Identifiers Required:
    player_id (internal)
    player_name 
    team
    competition (prem/champ)
    season (all current so irrelevant at the moment)
player_id generation:
    TODO
include:
    minutes (p90s computed later during processing)
    pos_primary 
    pos_others (optional)
    team_pos_pct (average team posession for that comp+season)
raw stats to maintain (keep adding as new analyses produced):
    shooting:
        npxg
        shots
        touches_box (touches in box)
    chance creation:
        xa
        key_passes
    carries:
        prog_carries
        carries_final_third
        carries_box
    pressing/defensive actions:
        pressures_final_third
        def_actions_final_third
    location on pitch:
        touches_halfspace
        touches_central
        touches_wide


Conventions:
    Missing stats are NaN
    position defined by sources/me, not by heuristics
    naming convention: snake_case
    add data as required
    all stats are total unless otherwise described in the name
    specific data quality rules are clear to me but can be added later

columns_to_keep =
    identifiers
  + feature_cols
  + [f"{c}_z" for c in feature_cols]
Record Future Changes: