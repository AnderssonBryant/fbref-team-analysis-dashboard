import streamlit as st
from pathlib import Path
from data.team import TEAM_META
import base64

def ordinal(n):
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def team_header(team, standings):
    
    meta = TEAM_META[team]
    color = meta["color"]
    standingsdf = standings[standings["team"] == team]
    position = standingsdf["Pos"].values[0]
    points = standingsdf["Pts"].values[0]
    logo_path = f"assets/logos/{meta['logo']}"
    accent = meta["accent"]

    with open(logo_path, "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <div style="
            background: {color};
            padding: 18px 24px;
            border-radius: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 28px;
        ">
            <div style="display:flex; align-items:center; gap:16px;">
                <img src="data:image/png;base64,{logo_base64}"
                     style="height:65px;" />
                <div>
                    <h2 style="margin:0; color:{accent};">{team}</h2>
                    <p style="margin:0; color:{accent}; font-size:14px;">
                        Premier League · 2024/25
                    </p>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="
                    font-size:20px;
                    font-weight:600;
                    color:{accent};
                ">
                    {ordinal(position)}
                </div>
                <div style="
                    font-size:20px;
                    color:{accent};
                ">
                    {points} pts
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
