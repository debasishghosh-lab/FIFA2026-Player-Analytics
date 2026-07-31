import sys
import importlib.util
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) in sys.path:
    sys.path.remove(str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR))

utils_path = (BASE_DIR / "utils.py").resolve()
if "utils" in sys.modules:
    loaded_file = Path(getattr(sys.modules["utils"], "__file__", "")).resolve()
    if loaded_file != utils_path:
        del sys.modules["utils"]

if "utils" not in sys.modules:
    spec = importlib.util.spec_from_file_location("utils", utils_path)
    utils = importlib.util.module_from_spec(spec)
    sys.modules["utils"] = utils
    spec.loader.exec_module(utils)

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
    page_title="Player Space | APEX 26",
    page_icon="🌍",
    layout="wide"
)

inject_apex_theme()

df = load_data()

# ──────────────────────────────────────────────
# PAGE HEADER
# ──────────────────────────────────────────────
apex_hero(
    "PCA Performance Spatial Map",
    "PLAYER SPACE",
    "Visualize every player in a 2D football performance space generated using Principal Component Analysis. Players positioned closer together produced more similar tournament performances."
)

# ──────────────────────────────────────────────
# FILTERS
# ──────────────────────────────────────────────
apex_card_start()

positions = ["All"] + sorted(df["Position"].unique())
selected_position = st.selectbox("Filter by Position", positions)

if selected_position != "All":
    plot_df = df[df["Position"] == selected_position]
else:
    plot_df = df.copy()

apex_card_end()

# ──────────────────────────────────────────────
# SCATTER PLOT
# ──────────────────────────────────────────────
apex_card_start()

fig = px.scatter(
    plot_df,
    x="PC1",
    y="PC2",
    color="Player Archetype",
    hover_name="Player",
    hover_data={
        "Country": True,
        "Position": True,
        "Performance Rating": ":.1f",
        "Goals": True,
        "Assists": True,
        "PC1": False,
        "PC2": False
    },
    title="Football Performance Space",
    height=700,
    color_discrete_sequence=[
        "#10B981", "#06B6D4", "#F59E0B", "#8B5CF6",
        "#EF4444", "#EC4899", "#14B8A6", "#F97316"
    ]
)

fig.update_traces(
    marker=dict(size=10, line=dict(width=1, color="rgba(255,255,255,0.3)"))
)

fig.update_layout(
    template="plotly_dark",
    legend_title="Player Archetype",
    xaxis_title="Principal Component 1 (Attack + Passing)",
    yaxis_title="Principal Component 2 (Defense + Movement)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94A3B8"),
    legend=dict(
        font=dict(family="Outfit", size=12),
        bgcolor="rgba(0,0,0,0)"
    ),
    margin=dict(l=40, r=40, t=60, b=40)
)

st.plotly_chart(fig, use_container_width=True)

apex_card_end()

# ──────────────────────────────────────────────
# DATASET OVERVIEW KPI CARDS
# ──────────────────────────────────────────────
apex_kpi_grid([
    ("PLAYERS", f"{len(plot_df):,}", "In current view", "green"),
    ("COUNTRIES", str(plot_df["Country"].nunique()), "Represented", "cyan"),
    ("ARCHETYPES", str(plot_df["Player Archetype"].nunique()), "Detected clusters", "amber"),
    ("AVG RATING", f"{plot_df['Performance Rating'].mean():.1f}", "Across filtered set", "rose"),
])

apex_divider()

st.markdown(
    '<p style="text-align: center; color: #64748B; font-size: 0.82rem; font-family: \'JetBrains Mono\', monospace;">Player positions are obtained using PCA on the four engineered performance dimensions.</p>',
    unsafe_allow_html=True
)
