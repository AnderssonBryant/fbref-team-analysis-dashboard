import pandas as pd
import streamlit as st


@st.cache_data
def load_team_data():
    """Load cleaned team stats CSV."""
    return pd.read_csv("data/PL_24_25_master_stats.csv")

@st.cache_data
def load_standings():
    return pd.read_csv("data/PL_24_25_standings.csv")

@st.cache_data
def load_opponent_stats():
    return pd.read_csv("data/opponent_stats_24_25.csv")

'''
['team', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts',
       'Performance_SoTA', 'Performance_Saves', 'Performance_CS',
       'Penalty Kicks_PKatt', 'Penalty Kicks_PKA', 'Penalty Kicks_PKsv',
       'Pass Types_Live', 'Pass Types_Dead', 'Pass Types_FK', 'Pass Types_TB',
       'Pass Types_Sw', 'Pass Types_Crs', 'Pass Types_TI', 'Pass Types_CK',
       'Total_Cmp', 'Total_Att', 'Total_TotDist', 'Total_PrgDist', 'Short_Cmp',
       'Short_Att', 'Medium_Cmp', 'Medium_Att', 'Long_Cmp', 'Long_Att', 'KP',
       '1/3', 'PPA', 'CrsPA', 'Team Success_PPM', 'Team Success (xG)_onxGA',
       'Poss', 'Performance_Gls', 'Performance_Ast', 'Performance_CrdY',
       'Performance_CrdR', 'Expected_xG', 'Progression_PrgC',
       'Progression_PrgP', 'Touches_Touches', 'Touches_Def Pen',
       'Touches_Def 3rd', 'Touches_Mid 3rd', 'Touches_Att 3rd',
       'Touches_Att Pen', 'Touches_Live', 'Carries_Carries', 'Carries_TotDist',
       'Carries_PrgDist', 'Carries_PrgC', 'Carries_1/3', 'Carries_CPA',
       'Take-Ons_Att', 'Take-Ons_Succ', 'Performance_Fls', 'Performance_Fld',
       'Performance_Crs', 'Performance_PKwon', 'Performance_PKcon',
       'Performance_OG', 'Performance_Recov', 'Aerial Duels_Won',
       'Aerial Duels_Lost', 'SCA_SCA', 'GCA_GCA', 'Tackles_Tkl',
       'Tackles_TklW', 'Tackles_Def 3rd', 'Tackles_Mid 3rd', 'Tackles_Att 3rd',
       'Challenges_Tkl', 'Challenges_Att', 'Challenges_Lost', 'Blocks_Blocks',
       'Int', 'Clr', 'Err', 'Standard_Sh', 'Standard_SoT', 'Standard_Dist',
       'Standard_FK', 'Standard_PK', 'Standard_PKatt']

'''