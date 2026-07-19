import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data

df = load_data()

st.title("📊 Dataset Insights")

st.markdown("""
Explore the FIFA World Cup 2026 dataset and understand the machine learning
pipeline used to analyze player performances.
""")

st.divider()

st.subheader("📌 Dataset Overview")

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

st.divider()

st.subheader("⚽ Player Position Distribution")

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
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("🧬 Player Archetypes")

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
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("⭐ Performance Rating Distribution")

fig = px.histogram(

    df[df["Position"] != "GK"],

    x="Performance Rating",

    nbins=20,

    color_discrete_sequence=["royalblue"]

)

fig.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("🏆 Top Tournament Performers")

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

