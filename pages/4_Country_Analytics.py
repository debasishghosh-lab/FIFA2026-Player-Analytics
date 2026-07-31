import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
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
    page_title="Country Analytics | APEX 26",
    page_icon="🏆",
    layout="wide"
)

inject_apex_theme()

# ──────────────────────────────────────────────
# LOAD DATA
# ──────────────────────────────────────────────
df = load_data()

# ──────────────────────────────────────────────
# COUNTRY SUMMARY
# ──────────────────────────────────────────────
country_stats = (
    df.groupby("Country")
      .agg({
          "Performance Rating": "mean",
          "Goals": "sum",
          "Assists": "sum",
          "Player": "count"
      })
      .reset_index()
)

country_stats.rename(
    columns={"Performance Rating": "Average Rating", "Player": "Players"},
    inplace=True
)

country_stats["Average Rating"] = country_stats["Average Rating"].round(1)
country_stats = country_stats.sort_values("Average Rating", ascending=False)

# ──────────────────────────────────────────────
# PAGE HEADER
# ──────────────────────────────────────────────
apex_hero(
    "FIFA World Cup 2026 · National Squad Analytics",
    "COUNTRY ANALYTICS",
    "Team performances based on aggregated player statistics from every competing nation at the 2026 World Cup."
)

# ──────────────────────────────────────────────
# TOURNAMENT OVERVIEW KPI CARDS
# ──────────────────────────────────────────────
apex_section_header("TOURNAMENT OVERVIEW")

top_country = country_stats.iloc[0]["Country"]
num_countries = country_stats.shape[0]
num_players = len(df)
avg_rating = country_stats["Average Rating"].mean()

apex_kpi_grid([
    ("COUNTRIES", str(num_countries), "Competing nations", "green"),
    ("PLAYERS", f"{num_players:,}", "Total registered", "cyan"),
    ("AVG RATING", f"{avg_rating:.1f}", "Across all squads", "amber"),
    ("TOP NATION", top_country[:14], "Highest avg rating", "rose"),
])

# ──────────────────────────────────────────────
# COUNTRY RANKINGS TABLE
# ──────────────────────────────────────────────
apex_section_header("COUNTRY RANKINGS")

display_stats = country_stats.copy()
display_stats.index = range(1, len(display_stats) + 1)

apex_card_start()
st.dataframe(display_stats, use_container_width=True)
apex_card_end()

# ──────────────────────────────────────────────
# AVERAGE RATING BAR CHART
# ──────────────────────────────────────────────
apex_section_header("AVERAGE PERFORMANCE RATING BY COUNTRY")

fig = px.bar(
    country_stats,
    x="Country",
    y="Average Rating",
    color="Average Rating",
    text="Average Rating",
    color_continuous_scale=[
        [0.0, "#059669"],
        [0.5, "#10B981"],
        [1.0, "#FCD34D"],
    ],
)

fig.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside",
    marker_line_width=0,
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#F8FAFC"),
    xaxis=dict(
        title="",
        tickfont=dict(size=10, family="Outfit"),
        gridcolor="rgba(255,255,255,0.05)",
        showline=False,
    ),
    yaxis=dict(
        title="Average Rating",
        title_font=dict(size=12, color="#94A3B8"),
        tickfont=dict(size=10),
        gridcolor="rgba(255,255,255,0.05)",
        showline=False,
    ),
    coloraxis_showscale=False,
    margin=dict(l=20, r=20, t=30, b=60),
    height=420,
)

apex_card_start()
st.plotly_chart(fig, use_container_width=True)
apex_card_end()

# ──────────────────────────────────────────────
# BEST PLAYER PER COUNTRY
# ──────────────────────────────────────────────
apex_section_header("BEST PLAYER FROM EVERY COUNTRY")

best = (
    df.sort_values("Performance Rating", ascending=False)
    .groupby("Country")
    .first()
    .reset_index()
)

best = best[["Country", "Player", "Position", "Performance Rating", "Player Archetype"]]
best["Performance Rating"] = best["Performance Rating"].round(1)

apex_card_start()
st.dataframe(best, use_container_width=True, hide_index=True)
apex_card_end()

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
apex_divider()

st.markdown("""
<div style="text-align: center; padding: 1.5rem;">
    <div style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1rem;">
        <span style="background: linear-gradient(135deg, #10B981, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">APEX 26</span>
        <span style="color: #64748B; font-size: 0.8rem; margin-left: 8px;">Country Analytics Module</span>
    </div>
    <div style="color: #475569; font-size: 0.75rem; margin-top: 6px; font-family: 'JetBrains Mono', monospace;">Data for illustrative purposes only</div>
</div>
""", unsafe_allow_html=True)
