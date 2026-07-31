import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) in sys.path:
    sys.path.remove(str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR))

import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    inject_apex_theme,
    apex_hero,
    apex_section_header,
    apex_card_start,
    apex_card_end,
    apex_kpi_grid,
    apex_divider,
    load_data
)

st.set_page_config(
    page_title="Dataset Insights | APEX 26",
    page_icon="📊",
    layout="wide"
)

inject_apex_theme()

df = load_data()

# ──────────────────────────────────────────────
# PAGE HEADER
# ──────────────────────────────────────────────
apex_hero(
    "Tournament Telemetry & ML Pipeline Analytics",
    "DATASET INSIGHTS",
    "Explore the FIFA World Cup 2026 dataset and the machine learning pipeline used to engineer player performance dimensions."
)

# ──────────────────────────────────────────────
# DATASET OVERVIEW KPI CARDS
# ──────────────────────────────────────────────
apex_kpi_grid([
    ("PLAYERS", f"{len(df):,}", "Scouted profiles", "green"),
    ("COUNTRIES", str(df["Country"].nunique()), "Global coverage", "cyan"),
    ("POSITIONS", str(df["Position"].nunique()), "Role classifications", "amber"),
    ("AVG PERFORMANCE", f"{df['Performance Rating'].mean():.1f}", "Outfield benchmark", "rose"),
])

# ──────────────────────────────────────────────
# PLAYER POSITION DISTRIBUTION
# ──────────────────────────────────────────────
apex_section_header("PLAYER POSITION DISTRIBUTION")

position_counts = df["Position"].value_counts().reset_index()
position_counts.columns = ["Position", "Players"]

fig = px.bar(
    position_counts,
    x="Position",
    y="Players",
    color="Position",
    text="Players",
    color_discrete_sequence=["#10B981", "#06B6D4", "#F59E0B", "#8B5CF6", "#EF4444"]
)

fig.update_traces(
    textposition="outside",
    marker_line_width=0,
)

fig.update_layout(
    template="plotly_dark",
    showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#F8FAFC"),
    xaxis=dict(
        title="",
        tickfont=dict(size=11, family="Outfit"),
        gridcolor="rgba(255,255,255,0.05)",
    ),
    yaxis=dict(
        title="Player Count",
        title_font=dict(size=12, color="#94A3B8"),
        tickfont=dict(size=10),
        gridcolor="rgba(255,255,255,0.05)",
    ),
    margin=dict(l=20, r=20, t=20, b=40),
    height=380,
)

apex_card_start()
st.plotly_chart(fig, use_container_width=True)
apex_card_end()

# ──────────────────────────────────────────────
# PLAYER ARCHETYPES DONUT
# ──────────────────────────────────────────────
apex_section_header("PLAYER ARCHETYPE DISTRIBUTION")

cluster_counts = (
    df[df["Position"] != "GK"]["Player Archetype"]
    .value_counts()
    .reset_index()
)
cluster_counts.columns = ["Archetype", "Players"]

fig = px.pie(
    cluster_counts,
    values="Players",
    names="Archetype",
    hole=0.45,
    color_discrete_sequence=[
        "#10B981", "#06B6D4", "#F59E0B", "#8B5CF6",
        "#EF4444", "#EC4899"
    ]
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#F8FAFC"),
    legend=dict(
        font=dict(family="Outfit", size=11),
        bgcolor="rgba(0,0,0,0)"
    ),
    margin=dict(l=20, r=20, t=20, b=20),
    height=420,
)

apex_card_start()
st.plotly_chart(fig, use_container_width=True)
apex_card_end()

# ──────────────────────────────────────────────
# PERFORMANCE RATING HISTOGRAM
# ──────────────────────────────────────────────
apex_section_header("PERFORMANCE RATING DISTRIBUTION")

fig = px.histogram(
    df[df["Position"] != "GK"],
    x="Performance Rating",
    nbins=20,
    color_discrete_sequence=["#06B6D4"]
)

fig.update_traces(
    marker_line_width=0,
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#F8FAFC"),
    xaxis=dict(
        title="Performance Rating",
        title_font=dict(size=12, color="#94A3B8"),
        tickfont=dict(size=10),
        gridcolor="rgba(255,255,255,0.05)",
    ),
    yaxis=dict(
        title="Frequency",
        title_font=dict(size=12, color="#94A3B8"),
        tickfont=dict(size=10),
        gridcolor="rgba(255,255,255,0.05)",
    ),
    margin=dict(l=20, r=20, t=20, b=40),
    height=380,
)

apex_card_start()
st.plotly_chart(fig, use_container_width=True)
apex_card_end()

# ──────────────────────────────────────────────
# TOP 10 TOURNAMENT PERFORMERS
# ──────────────────────────────────────────────
apex_section_header("TOP 10 TOURNAMENT PERFORMERS")

top = (
    df[df["Position"] != "GK"]
    .sort_values("Performance Rating", ascending=False)
    .head(10)
)

apex_card_start()
st.dataframe(
    top[["Player", "Country", "Position", "Performance Rating", "Player Archetype"]],
    hide_index=True,
    use_container_width=True
)
apex_card_end()

apex_divider()
