import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data

df = load_data()

# ==========================================================
# CUSTOM CSS — Premium Dark Football Dashboard Theme
# ==========================================================

st.markdown("""
<style>

    .stApp {
        background: radial-gradient(circle at top left, #0B1220 0%, #111827 45%, #0B1220 100%);
        color: #FFFFFF;
    }

    #MainMenu, footer {visibility: hidden;}

    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(12px);}
        to {opacity: 1; transform: translateY(0);}
    }
    @keyframes slideUp {
        from {opacity: 0; transform: translateY(30px);}
        to {opacity: 1; transform: translateY(0);}
    }

    /* ---------- Hero ---------- */
    .hero-container {
        background: linear-gradient(135deg, #006847 0%, #0B1220 60%, #111827 100%);
        border-radius: 20px;
        padding: 40px 36px;
        margin-bottom: 26px;
        box-shadow: 0 8px 32px rgba(0, 104, 71, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.08);
        animation: fadeIn 0.9s ease-out;
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 6px;
        background: linear-gradient(90deg, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #D1D5DB;
        max-width: 780px;
        line-height: 1.6;
    }

    /* ---------- Glass Card ---------- */
    .glass-card {
        background: rgba(31, 41, 55, 0.55);
        backdrop-filter: blur(10px);
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 26px 28px;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        animation: slideUp 0.7s ease-out;
    }

    /* ---------- Section Header ---------- */
    .section-header {
        font-size: 22px;
        font-weight: 700;
        margin: 4px 0 18px 0;
        padding-left: 14px;
        border-left: 5px solid #FFD700;
        background: linear-gradient(90deg, #FFFFFF, #9CA3AF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ---------- Metric Cards ---------- */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(0,104,71,0.25), rgba(31,41,55,0.55));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0, 191, 255, 0.18);
    }

    [data-testid="stMetricLabel"] {
        color: #D1D5DB !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-weight: 800 !important;
    }

    /* ---------- Dataframe ---------- */
    [data-testid="stDataFrame"] {
        border-radius: 14px !important;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
    }

    /* ---------- Divider ---------- */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 30px 0;
        border: none;
        opacity: 0.55;
    }

</style>
""", unsafe_allow_html=True)

# ==========================================================
# Title
# ==========================================================

st.markdown("""
<div class="hero-container">
    <div class="hero-title">📊 Dataset Insights</div>
    <div class="hero-subtitle">
        Explore the FIFA World Cup 2026 dataset and understand the machine learning
        pipeline used to analyze player performances.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# Dataset Overview
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">📌 Dataset Overview</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Players", len(df))

with c2:
    st.metric("Countries", df["Country"].nunique())

with c3:
    st.metric("Positions", df["Position"].nunique())

with c4:
    st.metric(
        "Average Performance",
        f"{df['Performance Rating'].mean():.1f}/100"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Player Position Distribution
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">⚽ Player Position Distribution</div>', unsafe_allow_html=True)

position_counts = (
    df["Position"]
    .value_counts()
    .reset_index()
)

position_counts.columns = [
    "Position",
    "Players"
]

fig = px.bar(

    position_counts,

    x="Position",

    y="Players",

    color="Position",

    text="Players"

)

fig.update_layout(
    template="plotly_dark",
    showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Player Archetypes
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">🧬 Player Archetypes</div>', unsafe_allow_html=True)

cluster_counts = (
    df[df["Position"] != "GK"]
    ["Player Archetype"]
    .value_counts()
    .reset_index()
)

cluster_counts.columns = [
    "Archetype",
    "Players"
]

fig = px.pie(

    cluster_counts,

    values="Players",

    names="Archetype",

    hole=0.45

)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Performance Rating Distribution
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">⭐ Performance Rating Distribution</div>', unsafe_allow_html=True)

fig = px.histogram(

    df[df["Position"] != "GK"],

    x="Performance Rating",

    nbins=20,

    color_discrete_sequence=["#00BFFF"]

)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Top Tournament Performers
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">🏆 Top Tournament Performers</div>', unsafe_allow_html=True)

top = (
    df[df["Position"] != "GK"]
    .sort_values(
        "Performance Rating",
        ascending=False
    )
    .head(10)
)

st.dataframe(

    top[[
        "Player",
        "Country",
        "Position",
        "Performance Rating",
        "Player Archetype"
    ]],

    hide_index=True,

    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)