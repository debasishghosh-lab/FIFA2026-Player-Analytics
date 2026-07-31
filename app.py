import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st
import pandas as pd
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
    page_title="APEX 26 // FIFA World Cup Scouting Suite",
    page_icon="⚽",
    layout="wide"
)

inject_apex_theme()

# ──────────────────────────────────────────────
# SIDEBAR BRANDING
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 4px 20px 4px;">
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.5rem; font-weight: 900; background: linear-gradient(135deg, #10B981, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px;">
            APEX 26
        </div>
        <div style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; letter-spacing: 1px; text-transform: uppercase;">
            FIFA World Cup Telemetry
        </div>
        <div style="margin-top: 12px; display: inline-flex; align-items: center; gap: 6px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); padding: 4px 10px; border-radius: 9999px; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #34D399;">
            <span style="width: 6px; height: 6px; background: #10B981; border-radius: 50%; box-shadow: 0 0 8px #10B981;"></span>
            LIVE ENGINE v2.6
        </div>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# BROADCAST HERO BANNER
# ──────────────────────────────────────────────
apex_hero(
    "FIFA World Cup 2026 // Technical Scouting Suite",
    "APEX 26 ANALYTICS",
    "Advanced player telemetry, PCA-engineered tactical performance dimensions, and machine learning archetype clustering for the 2026 FIFA World Cup."
)

# ──────────────────────────────────────────────
# TELEMETRY OVERVIEW METRICS
# ──────────────────────────────────────────────
df = load_data()

apex_kpi_grid([
    ("SCOUTED PLAYERS", f"{len(df):,}", "Complete profiles", "green"),
    ("NATIONS", str(df["Country"].nunique()), "Global coverage", "cyan"),
    ("ARCHETYPES", "6 Clusters", "K-Means classification", "amber"),
    ("PEAK RATING", f"{df['Performance Rating'].max():.1f}", "Outfield benchmark", "rose"),
])

# ──────────────────────────────────────────────
# SCOUTING MODULES GRID
# ──────────────────────────────────────────────
apex_card_start()
apex_section_header("TECHNICAL SCOUTING MODULES")

modules = [
    ("Player Analysis", "Deep-dive scouting dossier, radar rating comparison, and 5 nearest similarity matches."),
    ("Compare Players", "Head-to-head tactical duel comparing attribute ratings and overlay radar charts."),
    ("Player Space", "Interactive 2D PCA performance spatial map categorizing players into archetypes."),
    ("Country Analytics", "National squad power rankings, team averages, and country MVP leaderboards."),
    ("Dataset Insights", "Tournament-wide analytical telemetry, positional distributions, and performance histograms.")
]

module_cols = st.columns(2)

for i, (name, desc) in enumerate(modules):
    target_col = module_cols[i % 2]
    with target_col:
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 18px 20px; margin-bottom: 14px; transition: border-color 0.2s ease;">
            <div style="font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 4px;">{name}</div>
            <div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; color: #64748B; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; margin-top: 8px;">
        SELECT A MODULE FROM THE SIDEBAR TO BEGIN ANALYZING
    </div>
""", unsafe_allow_html=True)

apex_card_end()

# ──────────────────────────────────────────────
# ML PIPELINE TELEMETRY BOARD
# ──────────────────────────────────────────────
apex_card_start()
apex_section_header("ANALYTICAL PIPELINE ARCHITECTURE")

pipeline_steps = [
    ("01", "Automated Scraper", "Playwright sync scraping 8 FIFA statistical categories"),
    ("02", "Data Sanitation", "Pandas cleaning, duplicate removal, and missing value interpolation"),
    ("03", "PCA Dimensionality", "Principal Component Analysis on Attack, Pass, Defend, Movement & GK"),
    ("04", "K-Means Clustering", "Unsupervised machine learning identifying 6 core player archetypes"),
    ("05", "Euclidean Similarity", "NearestNeighbors engine computing tournament performance similarity %")
]

p_cols = st.columns(len(pipeline_steps))

for idx, (step_num, step_name, step_desc) in enumerate(pipeline_steps):
    with p_cols[idx]:
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.04); border: 1px solid rgba(16, 185, 129, 0.15); border-radius: 14px; padding: 18px 14px; text-align: center; height: 100%;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; color: #10B981; margin-bottom: 6px;">{step_num}</div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 0.9rem; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;">{step_name}</div>
            <div style="font-size: 0.75rem; color: #94A3B8; line-height: 1.4;">{step_desc}</div>
        </div>
        """, unsafe_allow_html=True)

apex_card_end()

apex_divider()

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 1rem 2rem 2rem 2rem;">
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #475569;">
        APEX 26 ANALYTICS · FIFA World Cup 2026 Technical Scouting Suite
    </div>
</div>
""", unsafe_allow_html=True)
