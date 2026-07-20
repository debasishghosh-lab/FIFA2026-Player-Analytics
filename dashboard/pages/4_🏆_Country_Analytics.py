import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import load_data

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="FIFA WC 2026 | Country Analytics",
    page_icon="🌍",
    layout="wide",
)

# ==========================================================
# Global CSS
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0B1220 0%, #0d1a2d 50%, #0B1220 100%);
    min-height: 100vh;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.5rem 2rem 3rem 2rem;
    max-width: 1400px;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #003d28 0%, #006847 45%, #004d35 100%);
    border: 1px solid rgba(0, 191, 255, 0.15);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(0, 104, 71, 0.35);
    animation: fadeSlideDown 0.6s ease both;
}
.hero-banner::before {
    content: "🌍";
    position: absolute;
    right: 3rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 7rem;
    opacity: 0.12;
    pointer-events: none;
}
.hero-banner::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 80% 50%, rgba(0, 191, 255, 0.07), transparent 60%);
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #FFD700;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1.15;
    margin: 0 0 0.6rem 0;
}
.hero-sub {
    font-size: 1rem;
    color: rgba(255,255,255,0.65);
    max-width: 500px;
    line-height: 1.6;
    margin: 0;
}

/* ── Section header ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 1rem 0;
}
.section-header .icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #006847, #00a86b);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.section-header h2 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0;
}
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(0,104,71,0.6), rgba(0,191,255,0.2), transparent);
    margin-bottom: 1.5rem;
    border: none;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 0.5rem;
}
.kpi-card {
    background: linear-gradient(145deg, #1a2535, #141d2e);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    animation: fadeSlideUp 0.5s ease both;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.kpi-card.green::before  { background: linear-gradient(90deg, #006847, #22C55E); }
.kpi-card.blue::before   { background: linear-gradient(90deg, #0066cc, #00BFFF); }
.kpi-card.gold::before   { background: linear-gradient(90deg, #b8860b, #FFD700); }
.kpi-card.red::before    { background: linear-gradient(90deg, #991b1b, #EF4444); }

.kpi-icon {
    font-size: 1.5rem;
    margin-bottom: 0.7rem;
    display: block;
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.45);
    margin-bottom: 0.35rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1;
}
.kpi-sub {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.4);
    margin-top: 0.35rem;
}

/* ── Data card wrapper ── */
.data-card {
    background: linear-gradient(145deg, #151e2e, #111827);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
    animation: fadeSlideUp 0.55s ease both;
}

/* ── Plotly chart container ── */
.stPlotlyChart > div {
    border-radius: 14px;
    overflow: hidden;
}

/* ── Dataframe styling ── */
.stDataFrame {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stDataFrame"] table {
    background: transparent !important;
}

/* ── Keyframe animations ── */
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# Load Dataset
# ==========================================================

df = load_data()

# ==========================================================
# Country Summary (unchanged logic)
# ==========================================================

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
    columns={
        "Performance Rating": "Average Rating",
        "Player": "Players"
    },
    inplace=True
)

country_stats["Average Rating"] = (
    country_stats["Average Rating"]
    .round(1)
)

country_stats = country_stats.sort_values(
    "Average Rating",
    ascending=False
)

# ==========================================================
# Hero Banner
# ==========================================================

st.markdown("""
<div class="hero-banner">
    <p class="hero-eyebrow">⚽ FIFA World Cup 2026 · Player Analytics</p>
    <h1 class="hero-title">🌍 Country Analytics</h1>
    <p class="hero-sub">Team performances based on aggregated player statistics from every nation at the 2026 World Cup.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# Tournament Overview — KPI Cards
# ==========================================================

st.markdown("""
<div class="section-header">
    <div class="icon">🌐</div>
    <h2>Tournament Overview</h2>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

top_country = country_stats.iloc[0]["Country"]
num_countries = country_stats.shape[0]
num_players = len(df)
avg_rating = country_stats["Average Rating"].mean()

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card green">
        <span class="kpi-icon">🌍</span>
        <div class="kpi-label">Countries</div>
        <div class="kpi-value">{num_countries}</div>
        <div class="kpi-sub">Competing nations</div>
    </div>
    <div class="kpi-card blue">
        <span class="kpi-icon">👥</span>
        <div class="kpi-label">Players</div>
        <div class="kpi-value">{num_players}</div>
        <div class="kpi-sub">Total registered</div>
    </div>
    <div class="kpi-card gold">
        <span class="kpi-icon">📊</span>
        <div class="kpi-label">Average Rating</div>
        <div class="kpi-value">{avg_rating:.1f}</div>
        <div class="kpi-sub">Across all squads</div>
    </div>
    <div class="kpi-card red">
        <span class="kpi-icon">🏆</span>
        <div class="kpi-label">Top Country</div>
        <div class="kpi-value" style="font-size:1.3rem;">{top_country}</div>
        <div class="kpi-sub">Highest avg rating</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# Country Rankings Table
# ==========================================================

st.markdown("""
<div class="section-header">
    <div class="icon">🏅</div>
    <h2>Country Rankings</h2>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

display_stats = country_stats.copy()
display_stats.index = range(1, len(display_stats) + 1)

with st.container():
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.dataframe(
        display_stats,
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Average Rating Bar Chart
# ==========================================================

st.markdown("""
<div class="section-header">
    <div class="icon">📊</div>
    <h2>Average Performance Rating by Country</h2>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

fig = px.bar(
    country_stats,
    x="Country",
    y="Average Rating",
    color="Average Rating",
    text="Average Rating",
    color_continuous_scale=[
        [0.0, "#006847"],
        [0.5, "#00a86b"],
        [1.0, "#FFD700"],
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
    font=dict(family="Inter", color="#FFFFFF"),
    xaxis=dict(
        title="Country",
        title_font=dict(size=12, color="rgba(255,255,255,0.5)"),
        tickfont=dict(size=10),
        gridcolor="rgba(255,255,255,0.05)",
        showline=False,
    ),
    yaxis=dict(
        title="Average Rating",
        title_font=dict(size=12, color="rgba(255,255,255,0.5)"),
        tickfont=dict(size=10),
        gridcolor="rgba(255,255,255,0.05)",
        showline=False,
    ),
    coloraxis_showscale=False,
    margin=dict(l=20, r=20, t=30, b=60),
    height=420,
)

with st.container():
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Best Player Per Country
# ==========================================================

st.markdown("""
<div class="section-header">
    <div class="icon">🥇</div>
    <h2>Best Player From Every Country</h2>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

best = (
    df.sort_values(
        "Performance Rating",
        ascending=False
    )
    .groupby("Country")
    .first()
    .reset_index()
)

best = best[[
    "Country",
    "Player",
    "Position",
    "Performance Rating",
    "Player Archetype"
]]

best["Performance Rating"] = (
    best["Performance Rating"]
    .round(1)
)

with st.container():
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.dataframe(
        best,
        use_container_width=True,
        hide_index=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Footer
# ==========================================================

st.markdown("""
<div style="
    margin-top: 3rem;
    padding: 1.5rem 2rem;
    background: linear-gradient(135deg, #0d1a2d, #111827);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.75rem;
">
    <div>
        <span style="font-size:1.1rem;">⚽</span>
        <span style="color:#006847; font-weight:700; margin-left:0.4rem;">FIFA World Cup 2026</span>
        <span style="color:rgba(255,255,255,0.35); font-size:0.8rem; margin-left:0.75rem;">Player Analytics Dashboard</span>
    </div>
    <div style="color:rgba(255,255,255,0.25); font-size:0.75rem;">
        Country Analytics · Data for illustrative purposes
    </div>
</div>
""", unsafe_allow_html=True)