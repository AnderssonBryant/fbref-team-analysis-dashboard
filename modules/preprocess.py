def per90 (value):
    return value / 38

def calculate_percentiles(series):
    """Convert columns into percentile ranking 0-100."""
    return series.rank(pct=True) * 100

def inverse_percentiles(series):
    """Convert columns into inverse percentile ranking 0-100."""
    return (1 - series.rank(pct=True)) * 100

def ordinal(n):
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def calculate_percentiles_all(df, invert_metrics):
    """Calculate percentiles for all metrics in the dataframe."""
    percentile_df = df.copy()
    for column in percentile_df.columns:
        if column in invert_metrics:
            percentile_df[column] = inverse_percentiles(df[column])
        else:
            percentile_df[column] = calculate_percentiles(df[column])
    return percentile_df

def calculated_metrics_radar(df):
    """Add calculated metrics to the dataframe."""
    df_display = df.copy()
    #shot quality
    df_display["Goals/Gm"] = df["GF"] / 38
    df_display["xG/Gm"] = df["Expected_xG"] / 38
    df_display["Conc/Gm"] = df["GA"] / 38
    df_display["xGA/Gm"] = df["Team Success (xG)_onxGA"] / 38
    df_display["Shots/Gm"] = df["Standard_Sh"] / 38
    df_display["Pass%"] = df["Total_Cmp"] / df["Total_Att"] * 100
    df_display["Tck%"] = df["Tackles_TklW"] / df["Tackles_Tkl"] * 100
    df_display["SoT%"] = df["Standard_SoT"] / df["Standard_Sh"] * 100
    df_display["Drb/Gm"] = df["Take-Ons_Succ"] / 38
    df_display['Crs/Gm'] = df['CrsPA'] / 38
    df_display["Fld/Gm"] = df["Performance_Fld"] / 38
    df_display["TcklA/Gm"] = df["Tackles_Tkl"] / 38
    df_display["Int/Gm"] = df["Int"] / 38
    df_display['Blk/Gm'] = df['Blocks_Blocks'] / 38
    df_display["Clr/Gm"] = df["Clr"] / 38
    df_display["Fls/Gm"] = df["Performance_Fls"] / 38
    df_display["xG/Shot"] = df["Expected_xG"] / df["Standard_Sh"]
    df_display["PrgC/Gm"] = df["Progression_PrgC"] / 38
    df_display["SCA/Gm"] = df["SCA_SCA"] / 38
    df_display["Touch_Att3rd/Gm"] = df["Touches_Att 3rd"] / 38
    df_display["Touch_AttPen/Gm"] = df["Touches_Att Pen"] / 38
    df_display["GCA/Gm"] = df["GCA_GCA"] / 38
    df_display["Conversion%"] = df_display["GF"] / df_display["Standard_Sh"] * 100
    df_display["Territory%"] = df_display["Touches_Att 3rd"] / df_display["Touches_Touches"]
    df_display["ProgPass%"] = df_display["Progression_PrgP"] / df_display["Total_Att"] * 100
    df_display["ProgPass/Gm"] = df_display["Progression_PrgP"] / 38
    df_display["Passing/Gm"] = df_display["Total_Att"] / 38
    df_display["Pass%"] = df_display["Total_Cmp"] / df_display["Total_Att"] * 100
    df_display["Short%"] = df_display["Short_Att"] / df_display["Total_Att"] * 100
    df_display["Medium%"] = df_display["Medium_Att"] / df_display["Total_Att"] * 100
    df_display["Long%"] = df_display["Long_Att"] / df_display["Total_Att"] * 100
    df_display["DefConv%"] = df_display["GA"] / df_display["Performance_SoTA"] * 100
    df_display["Pass_F3rd/Gm"] = df_display["1/3"] / 38
    df_display["KeyPasses/Gm"] = df_display["KP"] / 38
    df_display["Clearances/Gm"] = df_display["Clr"] / 38
    df_display["Blocks/Gm"] = df_display["Blocks_Blocks"] / 38
    df_display["Tckl+int/Gm"] = (df_display["Tackles_TklW"] + df_display["Int"])/38
    df_display["OppxG/Gm"] = df_display["Team Success (xG)_onxGA"] / 38
    df_display["DefAct/Gm"] = (df_display["Tackles_Tkl"] + df_display["Int"] + df_display["Blocks_Blocks"] + df_display["Clr"])/38
    df_display["Aerial_won%"] = df_display["Aerial Duels_Won"] / (df_display["Aerial Duels_Won"]+df_display["Aerial Duels_Lost"])

    return df_display

metrics = ["Goals/Gm", "xG/Gm", "Conc/Gm", "xGA/Gm", "Shots/Gm", "Pass%", "Tck%", "SoT%","Drb/Gm",
           "Crs/Gm","Fld/Gm","TcklA/Gm","Int/Gm","Blk/Gm","Clr/Gm","Fls/Gm"]


def derived_opponent_metrics(df):
    df_derived = df.copy()
    df_derived["Opp_Shots/Gm"] = df_derived["Standard_Sh"] / 38
    df_derived["Opp_SoT/Gm"] = df_derived["Standard_SoT"] / 38
    df_derived["Opp_TouchAtt3rd/Gm"] = df_derived["Touches_Att 3rd"] / 38
    df_derived["Opp_TouchAttPen/Gm"] = df_derived["Touches_Att Pen"] / 38
    return df_derived


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