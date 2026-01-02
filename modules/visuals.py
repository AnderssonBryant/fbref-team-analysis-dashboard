import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from modules.preprocess import ordinal

def simple_scatter(df, x_col, y_col, highlight_team, team_color, title, labels):
    
    x_mid = df[x_col].median()
    y_mid = df[y_col].median()

    x_min = df[x_col].min()
    x_max = df[x_col].max()

    y_min = df[y_col].min()
    y_max = df[y_col].max()
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        hover_name="team",
    )

    # Base styling (league-wide)
    fig.update_traces(
        marker=dict(
            size=10,
            color="rgba(200,200,200,0.45)",
        )
    )

    # Highlight selected team
    highlight_df = df[df["team"] == highlight_team]

    fig.add_scatter(
        x=highlight_df[x_col],
        y=highlight_df[y_col],
        mode="markers+text",
        text=highlight_team,
        textposition="top center",
        marker=dict(
            size=16,
            color=team_color,
            line=dict(width=2, color="white"),
        ),
        showlegend=False,
    )

    fig.add_vline(
        x=x_mid,
        line_dash="dash",
        line_color="rgba(255,255,255,0.35)",
    )

    fig.add_hline(
        y=y_mid,
        line_dash="dash",
        line_color="rgba(255,255,255,0.35)",
    )

    fig.update_layout(
        annotations=[
            dict(x=(x_mid + x_max)/2, y=(y_mid + y_max)/2,
                 text=labels["top_right"], showarrow=False,
                 font=dict(color="rgba(255,255,255,0.6)", size=12)),

            dict(x=(x_mid + x_min)/2, y=(y_mid + y_max)/2,
                 text=labels["top_left"], showarrow=False,
                 font=dict(color="rgba(255,255,255,0.6)", size=12)),

            dict(x=(x_mid + x_max)/2, y=(y_mid + y_min)/2,
                 text=labels["bottom_right"], showarrow=False,
                 font=dict(color="rgba(255,255,255,0.6)", size=12)),

            dict(x=(x_mid + x_min)/2, y=(y_mid + y_min)/2,
                 text=labels["bottom_left"], showarrow=False,
                 font=dict(color="rgba(255,255,255,0.6)", size=12)),
        ]
    )

    # Layout – keep same theme as overview
    fig.update_layout(
        title=title,
        height=430,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E6E6E6"),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
        ),
    )
    return fig


def radar_chart(percentile_df, raw_df, team_name, metrics, team_color):
    """Create a radar chart for the selected team based on given metrics."""
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r = percentile_df[metrics].values.flatten().tolist(),
        theta=metrics,
        fill='toself',
        name=team_name,
        customdata=raw_df.values.flatten().tolist(),
        line=dict(color=team_color, width=3),
        fillcolor=f"rgba{tuple(int(team_color[i:i+2],16) for i in (1,3,5)) + (0.25,)}",
        hovertemplate=(
            "<b>%{theta}</b><br>"
            "Value: %{customdata:.2f}<br>"
            "Percentile: %{r:.0f}"
            "<extra></extra>"
        )
    ))

    fig.update_layout(
        template="plotly_dark",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                range=[0, 100],
                ticksuffix="%",
                showline=False,
                gridcolor="rgba(255,255,255,0.15)",
                tickfont=dict(size=10, color="#E5E7EB")
           ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#E5E7EB"),
                gridcolor="rgba(255,255,255,0.08)"
            ),
        ),
        hoverlabel=dict(
            bgcolor="#111827",
            font_size=12,
            bordercolor="#E5E7EB"
        ),
        margin=dict(l=30, r=30, t=30, b=30),
        height=340,
        showlegend=False
    )
    return fig

def summary_table(
    df: pd.DataFrame,
    entity_col: str,
    entity_name: str,
    metrics: dict,
    decimals: int = 2,
    rank_ascending: dict | None = None
):
    """
    Generic summary table with value and league rank

    Parameters
    ----------
    df : pd.DataFrame
        Source dataframe
    entity_col : str
        Entity column name (e.g. 'Team')
    entity_name : str
        Selected entity (e.g. 'Arsenal')
    metrics : dict
        {Display Name: column_name}
    decimals : int
        Decimal rounding
    rank_ascending : dict
        {column_name: True/False} if lower is better
    """

    if rank_ascending is None:
        rank_ascending = {}

    row = df[df[entity_col] == entity_name]

    records = []

    for label, col in metrics.items():
        value = row[col].values[0]

        ascending = rank_ascending.get(col, False)
        rank = (
            df[col]
            .rank(ascending=ascending, method="min")
            .loc[row.index]
            .values[0]
        )

        records.append({
            "Metric": label,
            "Value": round(value, decimals),
            "Rank": ordinal(int(rank))
        })

    return pd.DataFrame(records)


def passing_types_bar(
    df,
    entity_col,
    entity_name,
    colors=None,
    template="plotly_dark",
    height=220
):
    """
    Horizontal bar chart for passing types distribution
    """

    if colors is None:
        colors = {
            "Short": "#2ecc71",
            "Medium": "#f1c40f",
            "Long": "#e74c3c"
        }

    row = df[df[entity_col] == entity_name]

    labels = ["Short", "Medium", "Long"]
    values = [
        row["Short%"].values[0],
        row["Medium%"].values[0],
        row["Long%"].values[0]
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=labels,
        x=values,
        orientation="h",
        marker_color=[colors[l] for l in labels],
        text=[f"{v:.2f}%" for v in values],
        textposition="outside"
    ))

    fig.update_layout(
        title="Passing Types Distribution",
        xaxis_title="Percentage of Passes",
        yaxis_title="",
        template=template,
        height=height,
        margin=dict(l=80, r=40, t=40, b=30),
        showlegend=False
    )

    fig.update_xaxes(range=[0, 100])

    return fig