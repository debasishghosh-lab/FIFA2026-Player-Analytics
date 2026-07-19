import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data

# ==========================================================
# Load Data
# ==========================================================

df = load_data()

# ==========================================================
# Title
# ==========================================================

st.title("🌍 Player Space")

st.markdown("""
Visualize every player in a 2D football performance space generated using
Principal Component Analysis (PCA).

Players positioned closer together produced more similar tournament performances.
""")

st.divider()

# ==========================================================
# Filters
# ==========================================================

positions = ["All"] + sorted(df["Position"].unique())

selected_position = st.selectbox(
    "Filter by Position",
    positions
)

if selected_position != "All":
    plot_df = df[df["Position"] == selected_position]
else:
    plot_df = df.copy()

# ==========================================================
# Scatter Plot
# ==========================================================

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

    yaxis_title="Principal Component 2"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# Statistics
# ==========================================================

st.subheader("📈 Dataset Overview")

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

st.divider()

st.caption(
    "Player positions are obtained using PCA on the four engineered performance dimensions."
)