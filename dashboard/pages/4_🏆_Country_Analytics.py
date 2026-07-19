import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data

# ==========================================================
# Load Dataset
# ==========================================================

df = load_data()

# ==========================================================
# Title
# ==========================================================

st.title("🏆 Country Analytics")

st.markdown("""
Analyze team performances based on aggregated player statistics
from the FIFA World Cup 2026.
""")

st.divider()

# ==========================================================
# Country Summary
# ==========================================================

country_stats = (
    df.groupby("Country")
      .agg({
          "Performance Rating":"mean",
          "Goals":"sum",
          "Assists":"sum",
          "Player":"count"
      })
      .reset_index()
)

country_stats.rename(
    columns={
        "Performance Rating":"Average Rating",
        "Player":"Players"
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
# Tournament Overview
# ==========================================================

st.subheader("🌍 Tournament Overview")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "Countries",
        country_stats.shape[0]
    )

with c2:
    st.metric(
        "Players",
        len(df)
    )

with c3:
    st.metric(
        "Average Rating",
        f"{country_stats['Average Rating'].mean():.1f}"
    )

with c4:
    st.metric(
        "Top Country",
        country_stats.iloc[0]["Country"]
    )

st.divider()

# ==========================================================
# Rankings
# ==========================================================

st.subheader("🏅 Country Rankings")

country_stats.index = country_stats.index + 1

st.dataframe(
    country_stats,
    use_container_width=True
)

st.divider()

# ==========================================================
# Average Rating Chart
# ==========================================================

st.subheader("📊 Average Performance Rating")

fig = px.bar(

    country_stats,

    x="Country",

    y="Average Rating",

    color="Average Rating",

    text="Average Rating"

)

fig.update_layout(

    template="plotly_dark",

    xaxis_title="Country",

    yaxis_title="Average Rating"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# Best Player Per Country
# ==========================================================

st.subheader("🥇 Best Player From Every Country")

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

st.dataframe(
    best,
    use_container_width=True,
    hide_index=True
)