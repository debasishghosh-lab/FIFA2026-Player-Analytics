import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils import (
    create_rating_columns,
    load_data,
    get_player_lookup,
    get_player_list
)

# ==========================================================
# Load Dataset
# ==========================================================

df = load_data()
df = create_rating_columns(df)

player_lookup = get_player_lookup(df)

players = get_player_list(df)

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

    /* ---------- Player Vs Card ---------- */
    .player-name-card {
        text-align: center;
        font-size: 26px;
        font-weight: 800;
        padding: 10px 0 16px 0;
        margin-bottom: 6px;
        border-radius: 14px;
    }

    .player-name-left {
        background: linear-gradient(90deg, rgba(0,191,255,0.18), transparent);
        color: #00BFFF;
        border-bottom: 3px solid #00BFFF;
    }

    .player-name-right {
        background: linear-gradient(270deg, rgba(255,127,80,0.18), transparent);
        color: #FF7F50;
        border-bottom: 3px solid #FF7F50;
    }

    .vs-badge {
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        color: #FFD700;
        margin: 6px 0 18px 0;
        letter-spacing: 2px;
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
        margin-bottom: 10px;
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

    /* ---------- Alerts ---------- */
    .stAlert {
        border-radius: 16px !important;
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
    <div class="hero-title">⚔️ Compare Players</div>
    <div class="hero-subtitle">
        Compare the tournament performances of any two players using
        Machine Learning based performance ratings and feature engineering.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# Player Selection
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    player_one = st.selectbox(
        "👤 Player 1",
        players,
        index=0,
        key="player_one"
    )

with col2:

    player_two = st.selectbox(
        "👤 Player 2",
        players,
        index=1,
        key="player_two"
    )

st.markdown('</div>', unsafe_allow_html=True)

p1 = player_lookup.loc[player_one]
p2 = player_lookup.loc[player_two]

# ==========================================================
# Prevent Goalkeeper Comparison
# ==========================================================

if p1["Position"] == "GK" or p2["Position"] == "GK":

    st.warning(
        "Goalkeeper comparison will be available in a future update."
    )

    st.stop()

# ==========================================================
# Player Cards
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">👥 Player Overview</div>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:

    st.markdown(f'<div class="player-name-card player-name-left">{player_one}</div>', unsafe_allow_html=True)

    st.metric(
        "Country",
        p1["Country"]
    )

    st.metric(
        "Position",
        p1["Position"]
    )

    st.metric(
        "Performance Rating",
        f"{p1['Performance Rating']:.1f}/100"
    )

with right:

    st.markdown(f'<div class="player-name-card player-name-right">{player_two}</div>', unsafe_allow_html=True)

    st.metric(
        "Country",
        p2["Country"]
    )

    st.metric(
        "Position",
        p2["Position"]
    )

    st.metric(
        "Performance Rating",
        f"{p2['Performance Rating']:.1f}/100"
    )

st.markdown('</div>', unsafe_allow_html=True)


# ==========================================================
# Radar Comparison
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">📊 Performance Radar Comparison</div>', unsafe_allow_html=True)

categories = [
    "Attack",
    "Passing",
    "Defense",
    "Movement"
]

p1_values = [
    p1["Attacking Rating"],
    p1["Passing Rating"],
    p1["Defensive Rating"],
    p1["Movement Rating"]
]

p2_values = [
    p2["Attacking Rating"],
    p2["Passing Rating"],
    p2["Defensive Rating"],
    p2["Movement Rating"]
]

# Close polygons
categories_closed = categories + [categories[0]]
p1_closed = p1_values + [p1_values[0]]
p2_closed = p2_values + [p2_values[0]]

fig = go.Figure()

# ----------------------------------------------------------
# Player 1
# ----------------------------------------------------------

fig.add_trace(

    go.Scatterpolar(

        r=p1_closed,

        theta=categories_closed,

        fill="toself",

        name=player_one,

        line=dict(
            color="#00BFFF",
            width=3
        ),

        fillcolor="rgba(0,191,255,0.35)"
    )

)

# ----------------------------------------------------------
# Player 2
# ----------------------------------------------------------

fig.add_trace(

    go.Scatterpolar(

        r=p2_closed,

        theta=categories_closed,

        fill="toself",

        name=player_two,

        line=dict(
            color="#FF7F50",
            width=3
        ),

        fillcolor="rgba(255,127,80,0.35)"
    )

)

fig.update_layout(

    polar=dict(

        bgcolor="rgba(0,0,0,0)",

        radialaxis=dict(

            visible=True,

            range=[0,100],

            tickvals=[20,40,60,80,100]

        )

    ),

    template="plotly_dark",

    legend=dict(
        orientation="h",
        y=1.08,
        x=0.25
    ),

    height=650,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Numerical Comparison
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">📈 Rating Comparison</div>', unsafe_allow_html=True)

comparison = pd.DataFrame({

    "Metric":[
        "Performance",
        "Attack",
        "Passing",
        "Defense",
        "Movement"
    ],

    player_one:[

        p1["Performance Rating"],
        p1["Attacking Rating"],
        p1["Passing Rating"],
        p1["Defensive Rating"],
        p1["Movement Rating"]

    ],

    player_two:[

        p2["Performance Rating"],
        p2["Attacking Rating"],
        p2["Passing Rating"],
        p2["Defensive Rating"],
        p2["Movement Rating"]

    ]

})

comparison[player_one] = comparison[player_one].round(1)
comparison[player_two] = comparison[player_two].round(1)

st.dataframe(
    comparison,
    hide_index=True,
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)