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
# Title
# ==========================================================

st.title("⚔️ Compare Players")

st.markdown("""
Compare the tournament performances of any two players using
Machine Learning based performance ratings and feature engineering.
""")

st.divider()

# ==========================================================
# Player Selection
# ==========================================================

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

st.subheader("👥 Player Overview")

left, right = st.columns(2)

with left:

    st.markdown(f"## {player_one}")

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

    st.markdown(f"## {player_two}")

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

st.divider()


# ==========================================================
# Radar Comparison
# ==========================================================

st.subheader("📊 Performance Radar Comparison")

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

    height=650

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# Numerical Comparison
# ==========================================================

st.subheader("📈 Rating Comparison")

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

st.divider()