import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils import (
    load_data,
    get_player_lookup,
    get_player_list,
    get_similar_players
)


df = load_data()

# ==========================================================
# Create Ratings (0-100)
# ==========================================================

OUTFIELD_FEATURES = [
    "Attacking Impact Score",
    "Passing Impact Score",
    "Defensive Impact Score",
    "Movement Impact Score"
]

for feature in OUTFIELD_FEATURES:

    rating_name = feature.replace("Impact Score", "Rating")

    df[rating_name] = (
        (df[feature] - df[feature].min())
        /
        (df[feature].max() - df[feature].min())
        * 100
    ).round(1)

# ==========================================================
# Player Lookup
# ==========================================================

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
        font-size: 36px;
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

    .hero-caption {
        font-size: 13px;
        color: #9CA3AF;
        margin-top: 10px;
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

    /* ---------- Progress bars ---------- */
    .stProgress > div > div {
        background: linear-gradient(90deg, #006847, #00BFFF) !important;
        border-radius: 10px;
    }
    .stProgress {
        margin-bottom: 14px;
    }

    /* ---------- Containers (bordered) ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: rgba(31, 41, 55, 0.45) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateX(3px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    }

    /* ---------- Select box ---------- */
    div[data-baseweb="select"] {
        border-radius: 12px !important;
    }

    /* ---------- Success / Info boxes ---------- */
    .stAlert {
        border-radius: 16px !important;
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
    <div class="hero-title">⚽ FIFA World Cup 2026 Player Analytics</div>
    <div class="hero-subtitle">
        Analyze FIFA World Cup 2026 player performances using Machine Learning,
        PCA-based feature engineering, similarity analysis and player archetypes.
    </div>
    <div class="hero-caption">🗂️ Dataset: FIFA World Cup 2026 Player Statistics — Updated till 16 July 2026</div>
</div>
""", unsafe_allow_html=True)



# ==========================================================
# Player Search
# ==========================================================

selected_player = st.selectbox(
    "🔍 Search Player",
    options=players,
    index=None,
    placeholder="Start typing a player's name..."
)

if selected_player is None:
    st.info("👆 Search for a player to begin.")
    st.stop()

player = player_lookup.loc[selected_player]

# ==========================================================
# Archetype Icons
# ==========================================================

icons = {
    "Tournament Superstars": "⭐",
    "Elite All-Round Performers": "🏆",
    "Dynamic Attackers": "⚡",
    "Complete Midfielders": "🎯",
    "Balanced Contributors": "⚽",
    "Limited Tournament Impact": "📉"
}

# ==========================================================
# Player Profile
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

if player["Position"] == "GK":
    st.markdown('<div class="section-header">🧤 Goalkeeper Profile</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="section-header">👤 Player Profile</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Country", player["Country"])
    st.metric("Position", player["Position"])

with col2:
    st.metric("Goals", int(player["Goals"]))
    st.metric("Assists", int(player["Assists"]))

with col3:

    minutes = player["Minutes Played"]

    if pd.notna(minutes):
        st.metric("Minutes Played", int(minutes))
    else:
        st.metric("Minutes Played", "-")

    if player["Position"] == "GK":

        st.metric(
            "🧤 Goalkeeping Rating",
            f"{player['Goalkeeping Rating']:.1f}/100"
        )

    else:

        st.metric(
            "⭐ Performance Rating",
            f"{player['Performance Rating']:.1f}/100"
        )

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Archetype
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

if player["Position"] != "GK":

    st.markdown('<div class="section-header">🧬 Player Archetype</div>', unsafe_allow_html=True)

    icon = icons.get(player["Player Archetype"], "⚽")

    st.success(
        f"{icon} {player['Player Archetype']}"
    )

else:

    st.markdown('<div class="section-header">🧤 Goalkeeper</div>', unsafe_allow_html=True)

    st.info(
        "Goalkeepers are analyzed using dedicated goalkeeping metrics rather than outfield player archetypes."
    )

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Performance Radar
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">📊 Performance Radar</div>', unsafe_allow_html=True)

if player["Position"] != "GK":

    radar_features = [
        "Attacking Rating",
        "Passing Rating",
        "Defensive Rating",
        "Movement Rating"
    ]

    labels = [
        "Attack",
        "Passing",
        "Defense",
        "Movement"
    ]

    # Selected Player
    player_values = [
        player["Attacking Rating"],
        player["Passing Rating"],
        player["Defensive Rating"],
        player["Movement Rating"]
    ]

    # Archetype Average
    archetype_df = df[
        (df["Player Archetype"] == player["Player Archetype"])
        &
        (df["Position"] != "GK")
    ]

    average_values = [
        archetype_df["Attacking Rating"].mean(),
        archetype_df["Passing Rating"].mean(),
        archetype_df["Defensive Rating"].mean(),
        archetype_df["Movement Rating"].mean()
    ]

    # Close polygons
    labels_closed = labels + [labels[0]]
    player_closed = player_values + [player_values[0]]
    average_closed = average_values + [average_values[0]]

    fig = go.Figure()

    # ------------------------------------------------------
    # Archetype Average
    # ------------------------------------------------------

    fig.add_trace(

        go.Scatterpolar(

            r=average_closed,

            theta=labels_closed,

            fill="toself",

            name="Archetype Average",

            line=dict(
                color="lightgray",
                width=2
            ),

            fillcolor="rgba(180,180,180,0.35)"
        )
    )

    # ------------------------------------------------------
    # Selected Player
    # ------------------------------------------------------

    fig.add_trace(

        go.Scatterpolar(

            r=player_closed,

            theta=labels_closed,

            fill="toself",

            name=selected_player,

            line=dict(
                color="#00BFFF",
                width=3
            ),

            fillcolor="rgba(0,191,255,0.45)"
        )
    )

    fig.update_layout(

        title=f"{selected_player} vs Average {player['Player Archetype']}",

        polar=dict(

            bgcolor="rgba(0,0,0,0)",

            radialaxis=dict(

                visible=True,

                range=[0,100],

                tickvals=[20,40,60,80,100],

                gridcolor="gray",

                gridwidth=1

            ),

            angularaxis=dict(

                gridcolor="gray"

            )

        ),

        template="plotly_dark",

        showlegend=True,

        legend=dict(
            orientation="h",
            y=1.1,
            x=0.2
        ),

        height=600,

        margin=dict(
            l=50,
            r=50,
            t=80,
            b=40
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "🧤 Goalkeeper radar chart will be available in a future update."
    )

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Performance Ratings
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

if player["Position"] != "GK":

    st.markdown('<div class="section-header">📊 Football Ratings</div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:

        st.metric(
            "⚔️ Attacking",
            f"{player['Attacking Rating']:.0f}/100"
        )

        st.progress(player["Attacking Rating"] / 100)

        st.metric(
            "🎯 Passing",
            f"{player['Passing Rating']:.0f}/100"
        )

        st.progress(player["Passing Rating"] / 100)

    with right:

        st.metric(
            "🛡️ Defending",
            f"{player['Defensive Rating']:.0f}/100"
        )

        st.progress(player["Defensive Rating"] / 100)

        st.metric(
            "🏃 Movement",
            f"{player['Movement Rating']:.0f}/100"
        )

        st.progress(player["Movement Rating"] / 100)

else:

    st.markdown('<div class="section-header">🧤 Goalkeeping Statistics</div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:

        saves = player["Goalkeeper Saves"]

        st.metric(
            "Saves",
            "-" if pd.isna(saves) else int(saves)
        )

        inside = player["Goalkeeper Actions Inside the Penalty Area"]

        st.metric(
            "Actions Inside Area",
            "-" if pd.isna(inside) else int(inside)
        )

    with right:

        outside = player["Goalkeeper Actions Outside the Penalty Area"]

        st.metric(
            "Actions Outside Area",
            "-" if pd.isna(outside) else int(outside)
        )

        st.metric(
            "Goalkeeping Rating",
            f"{player['Goalkeeping Rating']:.0f}/100"
        )

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Similar Performance Profiles
# ==========================================================

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">🤝 Similar Performance Profiles</div>', unsafe_allow_html=True)

if player["Position"] != "GK":

    similar_players = get_similar_players(
        df,
        selected_player,
        top_n=5
    )

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    for i, (_, row) in enumerate(similar_players.iterrows()):

        with st.container(border=True):

            col1, col2, col3 = st.columns([4, 2, 2])

            with col1:

                st.markdown(
                    f"""
                ### {medals[i]} {row['Player']}

                🌍 **Country:** {row['Country']}

                ⚽ **Position:** {row['Position']}
                """
                                )

            with col2:

                st.metric(
                    "⭐ Performance",
                    f"{row['Performance Rating']:.1f}/100"
                )

            with col3:

                st.metric(
                    "🤝 Similarity",
                    f"{row['Similarity']:.1f}%"
                )

else:

    st.info(
        "🧤 Similar performance profiles for goalkeepers will be available in a future update."
    )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown(
    '<p class="footer-caption">Developed using FIFA World Cup 2026 player statistics • Machine Learning • PCA • Clustering • Similarity Search</p>',
    unsafe_allow_html=True
)