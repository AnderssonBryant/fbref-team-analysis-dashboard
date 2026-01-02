import streamlit as st
import pandas as pd
import numpy as np

from components.header import team_header
from modules.data_loader import load_team_data,load_standings,load_opponent_stats
from modules.preprocess import calculate_percentiles_all, calculated_metrics_radar, derived_opponent_metrics
from modules.visuals import  passing_types_bar, radar_chart, simple_scatter, summary_table
from utils.quadrant_labels import Labels
from data.team import TEAM_META
import plotly.express as px
import plotly.graph_objects as go


# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Premier League Team Dashboard",
    layout="wide"
)

# --------------------------------------------------
# DATAAAAA
# -------------------------------------------------

df = load_team_data()
standings = load_standings()
opp_df = load_opponent_stats()

#___________________________________________________
# STYLESS
#___________________________________________________


st.markdown("""
    <style>
    /* Base font */
    html, body, [class*="css"] {
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Page title */
    .title-h1 {
        font-size: 43px;
        font-weight: 700;
        margin: 0.5rem 0 1rem 0;
    }

    /* Section title */
    .title-h2 {
        font-size: 36px;
        font-weight: 600;
        margin: 1.25 rem 0 1rem 0;
    }

    /* Subsection title */
    .title-h3 {
        font-size: 24px;
        font-weight: 600;
        margin: 1.25rem 0 0.75rem 0;
        text-align: center;
    }

    /* Body text */
    .text-body {
        font-size: 18px;
        font-weight: 400;
        line-height: 1.6;
        opacity: 0.9;
    }

    /* Caption / helper */
    .text-caption {
        font-size: 15px;
        opacity: 0.65;
        margin-top: 0.25rem;
    }

    </style>            
    
""", unsafe_allow_html=True)


def h1(text):
    st.markdown(f"<div class='title-h1'>{text}</div>", unsafe_allow_html=True)

def h2(text):
    st.markdown(f"<div class='title-h2'>{text}</div>", unsafe_allow_html=True)

def h3(text):
    st.markdown(f"<div class='title-h3'>{text}</div>", unsafe_allow_html=True)

def body(text):
    st.markdown(f"<div class='text-body'>{text}</div>", unsafe_allow_html=True)

def caption(text):
    st.markdown(f"<div class='text-caption'>{text}</div>", unsafe_allow_html=True)


#--------------------------------------------------
# PREPROCESSING
#--------------------------------------------------

metrics_calculated_fulldf = calculated_metrics_radar(df)

metrics_general = ["Goals/Gm", "xG/Gm", "Conc/Gm", "xGA/Gm", "Shots/Gm", "Pass%", "Tck%", "SoT%"]
metrics_attack = ["Goals/Gm", "xG/Gm", "Shots/Gm", "SoT%", "Drb/Gm", "Crs/Gm", "Pass%", "Fld/Gm"]
metrics_defense = ["Conc/Gm", "xGA/Gm", "TcklA/Gm", "Tck%", "Int/Gm", "Blk/Gm", "Clr/Gm", "Fls/Gm"]

invert_metrics = ["Conc/Gm", "xGA/Gm", "Fls/Gm"]
metrics_all = ["Goals/Gm", "xG/Gm", "Conc/Gm", "xGA/Gm", "Shots/Gm", "Pass%", "Tck%", "SoT%","Drb/Gm",
            "Crs/Gm","Fld/Gm","TcklA/Gm","Int/Gm","Blk/Gm","Clr/Gm","Fls/Gm"]

percentile_metrics_df = calculate_percentiles_all(metrics_calculated_fulldf[metrics_all], invert_metrics)


# --------------------------------------------------
# SIDEBAR (GLOBAL CONTROLS)
# --------------------------------------------------
with st.sidebar:
    h1("Controls")

    selected_team = st.sidebar.selectbox(
    "Select Team",
    df['team']
    )


# --------------------------------------------------
# GET SELECTED TEAM DATA
# --------------------------------------------------

team_df = df[df["team"] == selected_team]
team_color = TEAM_META[selected_team]["color"]
row = df.index[df['team'] == selected_team][0]

# --------------------------------------------------
# HEADER
# --------------------------------------------------
h1("Premier League Team Analysis Dashboard")

team_header(selected_team, standings)

# --------------------------------------------------
# TABS
# --------------------------------------------------
tabs = st.tabs([
    "Overview",
    "Attacking",
    "Possession",
    "Defensive",
    "Standings"
])

st.markdown("""
<style>
div[data-baseweb="tab-list"] button {
    font-size: 15px;
    padding: 10px 16px;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# OVERVIEW TAB (FULL IMPLEMENTATION)
# ==================================================
with tabs[0]:
    
    h1("Team Overview")
    caption("A high level snapshot of attacking, possession, and defensive performance")
    st.divider()
    h2("Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Goals", team_df["GF"].values[0],delta = int(team_df['GF'])-df['GF'].mean(),delta_color="normal")
    col2.metric("xG", round(team_df["Expected_xG"].values[0], 2),delta = round(float(team_df['Expected_xG'])-float(df['Expected_xG'].mean()),2),delta_color="normal")
    col3.metric("Conceded", team_df["GA"].values[0],delta = int(team_df['GA'])-df['GA'].mean(),delta_color="inverse")
    col4.metric("Possession (%)", round(team_df["Poss"].values[0], 2),delta = round(float(team_df['Poss'])-float(df['Poss'].mean()),2),delta_color="normal")
    st.divider()

    col1, col2, col3 = st.columns(3)


    with col1:
        with st.container(border= True):
            h3("General Performance")

            percentile_teamdf = percentile_metrics_df[metrics_general].iloc[[row]]
            raw_values = metrics_calculated_fulldf[metrics_general].iloc[[row]]

            fig = radar_chart(percentile_teamdf, raw_values, selected_team, metrics_general,team_color)
            
            st.plotly_chart(fig,use_container_width=True,theme = None)

    with col2:
        with st.container(border= True):
            h3("Team Attacking")

            percentile_teamdf = percentile_metrics_df[metrics_attack].iloc[[row]]
            raw_values = metrics_calculated_fulldf[metrics_attack].iloc[[row]]

            fig = radar_chart(percentile_teamdf, raw_values, selected_team, metrics_attack,team_color)

            st.plotly_chart(fig,use_container_width=True,theme = None)

    with col3:
        with st.container(border= True):
            h3("Team Defending")

            percentile_teamdf = percentile_metrics_df[metrics_defense].iloc[[row]]
            raw_values = metrics_calculated_fulldf[metrics_defense].iloc[[row]]

            fig = radar_chart(percentile_teamdf, raw_values, selected_team, metrics_defense,team_color)

            st.plotly_chart(fig,use_container_width=True,theme = None)

# ==================================================
# OTHER TABS (PLACEHOLDERS)
# ==================================================
with tabs[1]:
    h1("Attacking Analysis")
    caption("How team create chances, reach dangerous areas, and turn attacks into goals")
    st.divider()

    h2("Key Metrics")

    metrics_teamdf = metrics_calculated_fulldf[metrics_calculated_fulldf['team'] == selected_team] 

    col1, col2, col3, col4,col5 = st.columns(5)

    col1.metric("Goals / Game", round(metrics_teamdf["Goals/Gm"].values[0],2),delta = round((metrics_teamdf["Goals/Gm"].values[0]-metrics_calculated_fulldf["Goals/Gm"].mean()),2),delta_color="normal")
    col2.metric("xG / Game", round(metrics_teamdf["xG/Gm"].values[0], 2),delta = round((metrics_teamdf["xG/Gm"].values[0]-metrics_calculated_fulldf["xG/Gm"].mean()),2),delta_color="normal")
    col3.metric("Shots / Game", round(metrics_teamdf["Shots/Gm"].values[0],2),delta = round((metrics_teamdf["Shots/Gm"].values[0]-metrics_calculated_fulldf["Shots/Gm"].mean()),2),delta_color="normal")
    col4.metric("Shot on Target (%)", round(metrics_teamdf["SoT%"].values[0], 2),delta = round((metrics_teamdf["SoT%"].values[0]-metrics_calculated_fulldf["SoT%"].mean()),2),delta_color="normal")
    col5.metric("Conversion (%)", round(metrics_teamdf["Conversion%"].values[0], 2),delta = round((metrics_teamdf["Conversion%"].values[0]-metrics_calculated_fulldf["Conversion%"].mean()),2),delta_color="normal")

    st.divider()

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        with st.container(border = True):
            h3("Decisive Creation to Goal")

            fig = simple_scatter(
                df=metrics_calculated_fulldf,
                x_col="GCA/Gm",
                y_col="Goals/Gm",
                team_color=team_color,
                highlight_team=selected_team,
                title="Goal Creation Action vs Goals",
                labels= Labels["A1"]
            )
            st.plotly_chart(fig, use_container_width=True)

    with row1_col2:
        with st.container(border = True):
            h3("Chance Quality vs Goal Output")

            fig = simple_scatter(
                df=metrics_calculated_fulldf,
                x_col="xG/Gm",
                y_col="Goals/Gm",
                team_color=team_color,
                highlight_team=selected_team,
                title="Expected Goals vs Goals",
                labels= Labels["A2"]
            )
            st.plotly_chart(fig, use_container_width=True)

    with row2_col1:
        with st.container(border= True):
            h3("Box Presence vs  Goal Output")

            fig = simple_scatter(
                df=metrics_calculated_fulldf,
                x_col="Touch_AttPen/Gm",
                y_col="Goals/Gm",
                team_color=team_color,
                highlight_team=selected_team,
                title="Touch at Penalty Area vs Goals",
                labels= Labels["A3"]
            )

            st.plotly_chart(fig, use_container_width=True)

    with row2_col2:
        with st.container(border= True):
            h3("Shot Volume vs Goal Output")

            fig = simple_scatter(
                df=metrics_calculated_fulldf,
                x_col="Shots/Gm",
                y_col="Goals/Gm",
                team_color=team_color,
                highlight_team=selected_team,
                title="Shot Volume vs Goals",
                labels= Labels["A4"]
            )

            st.plotly_chart(fig, use_container_width=True)

    with st.container(border= True):
        h3("Attacking Summary Table")
        ATTACKING_SUMMARY = {
            "xG / Gm": "xG/Gm",
            "Goals / Gm": "Goals/Gm",
            "SCA / Gm": "SCA/Gm",
            "GCA / Gm": "GCA/Gm",
            "Shots / Gm": "Shots/Gm",
            "Conversion %": "Conversion%"
        }

        rank_dir = {
            "Conversion%": False  # higher is better
        }

        table = summary_table(  
                df=metrics_calculated_fulldf,
                entity_col="team",
                entity_name=selected_team,
                metrics=ATTACKING_SUMMARY,
                decimals=2,
                rank_ascending=rank_dir
            )

        st.dataframe(table, hide_index=True, use_container_width=True)

with tabs[2]:
    h1("Possession Analysis")
    caption("How team use possesion to progress the ball")
    st.divider()
    
    h2("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Possession %", round(metrics_teamdf["Poss"].values[0], 2),delta = round(float(metrics_teamdf['Poss'])-float(df['Poss'].mean()),2),delta_color="normal")
    col2.metric("Pass %",round(metrics_teamdf["Pass%"].values[0], 2),delta = round((metrics_teamdf["Pass%"].values[0]-metrics_calculated_fulldf["Pass%"].mean()),2),delta_color="normal")
    col3.metric("Territory %", round(metrics_teamdf["Territory%"].values[0], 2),delta = round((metrics_teamdf["Territory%"].values[0]-metrics_calculated_fulldf["Territory%"].mean()),2),delta_color="normal")
    col4.metric("Progressive Pass %", round(metrics_teamdf["ProgPass%"].values[0], 2),delta = round((metrics_teamdf["ProgPass%"].values[0]-metrics_calculated_fulldf["ProgPass%"].mean()),2),delta_color="normal")
    st.divider()
    col_1, col_2 = st.columns(2)

    with col_1:
        with st.container(border= True):
            h3("Possession Control vs Territorial Presence")

            fig = simple_scatter(
                df=metrics_calculated_fulldf,
                x_col="Poss",
                y_col="Touch_Att3rd/Gm",
                team_color=team_color,
                highlight_team=selected_team,
                title="Possession % vs Touches Att 3rd / Gm",
                labels= Labels["P1"]
            )

            st.plotly_chart(fig, use_container_width=True)
    with col_2:
        with st.container(border= True):
            h3("Ball Progression vs Passing Security")

            fig = simple_scatter(
                df=metrics_calculated_fulldf,
                x_col="Pass%",
                y_col="ProgPass/Gm",
                team_color=team_color,
                highlight_team=selected_team,
                title="Pass % vs Progressive Pass/Gm",
                labels= Labels["P2"]
            )

            st.plotly_chart(fig, use_container_width=True)

    with st.container(border = True):
        h3("Passing Types Distribution")
        fig = passing_types_bar(
            df=metrics_calculated_fulldf,
            entity_col="team",
            entity_name=selected_team
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.container(border= True):
        h3("Possession Summary Table")
        POSSESSION_SUMMARY = {
            "Possession %": "Poss",
            "Pass %": "Pass%",
            "Territory %": "Territory%",
            "Progressive Pass %": "ProgPass%",
            "Pass into Final Third/Gm" : "Pass_F3rd/Gm",
            "Key Passes/Gm" : "KeyPasses/Gm"
        }

        rank_dir = {
            "Possession %": False,  # higher is better
            "Pass %": False,
            "Territory %": False,
            "Progressive Pass %": False,

        }

        table = summary_table(
            df=metrics_calculated_fulldf,
            entity_col="team",
            entity_name=selected_team,
            metrics=POSSESSION_SUMMARY,
            decimals=2,
            rank_ascending=rank_dir
        )

        st.dataframe(table, hide_index=True, use_container_width=True)


with tabs[3]:
    h1("Defensive Analysis")
    caption("How team manage defensive exposure and prevent high quality chances")
    st.divider()


    opp_df = derived_opponent_metrics(opp_df)
    metrics_calculated_fulldf = pd.concat([metrics_calculated_fulldf, opp_df[["Opp_Shots/Gm","Opp_SoT/Gm","Opp_TouchAtt3rd/Gm","Opp_TouchAttPen/Gm"]]], axis=1)

    metrics_calculated_fulldf["OppxG/ShA/Gm"] = metrics_calculated_fulldf["OppxG/Gm"] / metrics_calculated_fulldf["Opp_Shots/Gm"]

    metrics_teamdf = metrics_calculated_fulldf[metrics_calculated_fulldf['team'] == selected_team] 

    h2("Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Conceded / Game", round(metrics_teamdf["Conc/Gm"].values[0],2),delta = round((metrics_teamdf["Conc/Gm"].values[0]-metrics_calculated_fulldf["Conc/Gm"].mean()),2),delta_color="inverse")
    col2.metric("Shot Faced / Game",round(metrics_teamdf["Opp_Shots/Gm"].values[0],2), delta =round((metrics_teamdf["Opp_Shots/Gm"].values[0]-metrics_calculated_fulldf["Opp_Shots/Gm"].mean()),2),delta_color="inverse" )
    col3.metric("xGA / Game", round(metrics_teamdf["xGA/Gm"].values[0], 2),delta = round((metrics_teamdf["xGA/Gm"].values[0]-metrics_calculated_fulldf["xGA/Gm"].mean()),2),delta_color="inverse")
    col4.metric("Tackles Won %", round(metrics_teamdf["Tck%"].values[0],2),delta = round((metrics_teamdf["Tck%"].values[0]-metrics_calculated_fulldf["Tck%"].mean()),2),delta_color="normal")
    col5.metric("Defensive Conversion %", round(metrics_teamdf["DefConv%"].values[0], 2),delta = round((metrics_teamdf["DefConv%"].values[0]-metrics_calculated_fulldf["DefConv%"].mean()),2),delta_color="normal")
    st.divider()

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        with st.container(border=True):
            h3("Defensive workload vs Defensive output")

            fig = simple_scatter(
                df=metrics_calculated_fulldf,
                x_col="OppxG/Gm",
                y_col="Tckl+int/Gm",
                team_color=team_color,
                highlight_team=selected_team,
                title="Opponent xG./Gm vs Tackles + Int/Gm",
                labels= Labels["D1"]
            )
            st.plotly_chart(fig, use_container_width=True)

    with row1_col2:
         with st.container(border=True):
            h3("Territorial Resistance")

            fig = simple_scatter(
                df=metrics_calculated_fulldf,
                x_col="Opp_TouchAtt3rd/Gm",
                y_col="Opp_TouchAttPen/Gm",
                team_color=team_color,
                highlight_team=selected_team,
                title="Opponent Touches in Final Third vs Touches in Penalty Area",
                labels= Labels["D2"]
            )
            st.plotly_chart(fig, use_container_width=True)
    with row2_col1:
        with st.container(border= True):
            h3("Shot Quality Prevention")

            fig = simple_scatter(
                df=metrics_calculated_fulldf,
                x_col="Opp_Shots/Gm",
                y_col="OppxG/Gm",
                team_color=team_color,
                highlight_team=selected_team,
                title="Opponent Shot Volume vs xG Conceded",
                labels= Labels["D3"]
            )
            st.plotly_chart(fig, use_container_width=True)
    with row2_col2:
        with st.container(border= True):
            h3("Activity vs Efficiency")

            fig = simple_scatter(
                df=metrics_calculated_fulldf,
                x_col="DefAct/Gm",
                y_col="Tck%",
                team_color=team_color,
                highlight_team=selected_team,
                title="Defensive Actions vs Tackle Success%",
                labels= Labels["D4"]
            )
            st.plotly_chart(fig, use_container_width=True)

    with st.container(border = True):
        h3("Defensive Summary Table")
        Defensive_SUMMARY = {
            "Opposition xG/Gm": "OppxG/Gm",
            "xG per Shot Faced": "OppxG/ShA/Gm",
            "Tackle + Interception / Gm": "Tckl+int/Gm",
            "Aerial Win%": "Aerial_won%"
        }

        rank_dir = {
            "OppxG/Gm": True,  # higher is better
            "OppxG/ShA/Gm": True,
            "Tckl+int/Gm": False,
            "Aerial_won%": False,

        }

        table = summary_table(
            df=metrics_calculated_fulldf,
            entity_col="team",
            entity_name=selected_team,
            metrics=Defensive_SUMMARY,
            decimals=2,
            rank_ascending=rank_dir
        )

        st.dataframe(table, hide_index=True, use_container_width=True)


with tabs[4]:
    h2("Premier League Standings")
    caption("Season 2024/25 • Contextual league table")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Teams", standings.shape[0])
    c2.metric("Matches Played", 38)
    c3.metric("Top Team Points", standings.iloc[0]["Pts"])
    c4.metric("Relegation Safety", standings.iloc[16]["Pts"])

    st.divider()

    # --------------------------------
    # Styling functions
    # --------------------------------
    def style_zones(row):
        if row["Pos"] <= 4:
            color = "#2BD67B"      # Champions League
        elif row["Pos"] == 5:
            color = "#60A5FA"      # Europa League
        elif row["Pos"] == 6:
            color = "#A78BFA"      # Conference League
        elif row["Pos"] >= 18:
            color = "#DC2626"      # Relegation
        else:
            color = "#9CA3AF"      # Neutral
        return [f"color: {color}"] * len(row)


    def highlight_team(row):
        if row["team"] == selected_team:
            return [
                "background-color: #3D195B; color: #E6E6E6"
            ] * len(row)
        return [""] * len(row)


    # --------------------------------
    # Apply styles
    # --------------------------------
    styled_df = (
        standings
        .style
        .apply(style_zones, axis=1)
        .apply(highlight_team, axis=1)
        .format({
            "GD": "{:+d}",
            "Pts": "{:.0f}"
        })
    )

    # --------------------------------
    # Display table
    # --------------------------------
    h2("League Table")

    st.dataframe(
        styled_df,
        use_container_width=True,
        height = 738,
        hide_index=True
    )

    # --------------------------------
    # Context note
    # --------------------------------
    caption(
        "Qualification zones and relegation places are highlighted for context. "
        "This table is intended for situational awareness, not tactical analysis."
    )

# -----------------------------
# CONTEXT NOTE
# -----------------------------
caption(
    "Note: All metrics are team-level aggregates from FBref. "
    "Derived metrics are calculated manually for analytical clarity."
)

st.divider()

st.markdown(
    """
    <div style="text-align:center; font-size:0.85rem; color:#9CA3AF;">
        Premier League Team Analysis Dashboard<br>
        Data: FBref | Season: 2024/25<br>
        Built by <b>Bryant Andersson</b><br>
        <a href="https://github.com/anderssonbryant" target="_blank">GitHub</a> |
        <a href="https://www.linkedin.com/in/bryant-andersson-tantra-73a5291b2/" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True
)
