import plotly.graph_objects as go

def simple_radar_withavg(df, team, metrics, labels, team_color,invert_metrics):
    """
    Renders a simple radar chart comparing a team's metrics against the average.

    Parameters:
    - df: DataFrame containing the metrics data.
    - team: The team to highlight.
    - metrics: List of metric column names.
    - labels: List of labels for the radar chart axes.
    - team_color: Color to use for the team's trace.
    - scale: Scale mode for the radar chart ('linear' or 'log').

    Returns:
    - fig: Plotly Figure object representing the radar chart.
    """
    work = df.copy()

    team_row = work[work['team'] == team]

    pct_vals = team_row[metrics].rank(pct=True)
    raw_vals = team_row[metrics].values

    print(pct_vals)
    print(raw_vals)

    fig = go.Figure()

    fig.add_trace(go.line_polar(
        r=pct_vals,
        theta=labels,
        fill='toself',
        name=team,
        line=dict(color=team_color, width = 3),
        customdata=raw_vals,
        hovertemplate='%{theta}: %{customdata[0]:.2f}<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0,100],
                ticksuffix = '%'
            )
        ),
        showlegend=True
    )

    return fig