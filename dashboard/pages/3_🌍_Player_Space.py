import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data

# ==========================================================
# Load Data
# ==========================================================

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

    /* ---------- Select box ---------- */
    div[data-baseweb="select"] {
        border-radius: 12px !important;
    }

    /* ---------- Divider ---------- */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 30px 0;
        border: none;
        opacity: 0.55;
    }

    /* ---------- Caption ---------- */
    .footer-caption {
        text-align: center;
        color: #9CA3AF;
        font-size: 13px;
        margin-top: 10px;
    }

</style>
""", unsafe_allow_html=True)

# ==========================================================
# Title
# ==========================================================

st.markdown("""
<div class="hero-container">
    <div class="hero-title">🌍 Player Space</div>
    <div class="hero-subtitle">
        Visualize every player in a 2D football performance space generated using
        Principal Component Analysis (PCA).<br>
        Players positioned closer together produced more similar tournament performances.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# Filters
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

positions = ["All"] + sorted(df["Position"].unique())

selected_position = st.selectbox(
    "Filter by Position",
    positions
)

if selected_position != "All":
    plot_df = df[df["Position"] == selected_position]
else:
    plot_df = df.copy()

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Scatter Plot
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

fig = px.scatter(

    plot_df,

    x="PC1",

    y="PC2",

    color="Player Archetype",

    hover_name="Player",

    hover_data={

        "Country":True,

        "Position":True,

        "Performance Rating":":.1f",

        "Goals":True,

        "Assists":True,

        "PC1":False,

        "PC2":False

    },

    title="Football Player Space",

    height=700
)

fig.update_traces(

    marker=dict(

        size=10,

        line=dict(
            width=1,
            color="white"
        )

    )

)

fig.update_layout(

    template="plotly_dark",

    legend_title="Player Archetype",

    xaxis_title="Principal Component 1",

    yaxis_title="Principal Component 2",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Statistics
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">📈 Dataset Overview</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Players",
        len(plot_df)
    )

with c2:
    st.metric(
        "Countries",
        plot_df["Country"].nunique()
    )

with c3:
    st.metric(
        "Archetypes",
        plot_df["Player Archetype"].nunique()
    )

with c4:
    st.metric(
        "Average Rating",
        f"{plot_df['Performance Rating'].mean():.1f}"
    )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown(
    '<p class="footer-caption">Player positions are obtained using PCA on the four engineered performance dimensions.</p>',
    unsafe_allow_html=True
)