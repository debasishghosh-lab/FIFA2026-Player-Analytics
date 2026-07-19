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
# Title
# ==========================================================

st.title("⚽ FIFA World Cup 2026 Player Analytics")

st.markdown("""
Analyze FIFA World Cup 2026 player performances using Machine Learning,
PCA-based feature engineering, similarity analysis and player archetypes.

**Dataset:** FIFA World Cup 2026 Player Statistics *(Updated till 16 July 2026)*
""")

st.divider()



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

if player["Position"] == "GK":
    st.subheader("🧤 Goalkeeper Profile")
else:
    st.subheader("👤 Player Profile")

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

st.divider()

# ==========================================================
# Archetype
# ==========================================================

if player["Position"] != "GK":

    st.subheader("🧬 Player Archetype")

    icon = icons.get(player["Player Archetype"], "⚽")

    st.success(
        f"{icon} {player['Player Archetype']}"
    )

else:

    st.subheader("🧤 Goalkeeper")

    st.info(
        "Goalkeepers are analyzed using dedicated goalkeeping metrics rather than outfield player archetypes."
    )

st.divider()

# ==========================================================
# Performance Radar
# ==========================================================

st.subheader("📊 Performance Radar")

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
        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "🧤 Goalkeeper radar chart will be available in a future update."
    )

st.divider()

# ==========================================================
# Performance Ratings
# ==========================================================

if player["Position"] != "GK":

    st.subheader("📊 Football Ratings")

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

    st.subheader("🧤 Goalkeeping Statistics")

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

# ==========================================================
# Similar Performance Profiles
# ==========================================================

st.divider()

st.subheader("🤝 Similar Performance Profiles")

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

st.divider()

st.caption(
    "Developed using FIFA World Cup 2026 player statistics • Machine Learning • PCA • Clustering • Similarity Search"
)