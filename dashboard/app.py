import streamlit as st

st.set_page_config(
    page_title="FIFA World Cup 2026 Analytics",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FIFA World Cup 2026 Analytics")

st.markdown("""
Welcome to the **FIFA World Cup 2026 Analytics Dashboard**.

This project uses Machine Learning techniques to analyze player performances
from the FIFA World Cup 2026.

### Features

- 👤 Player Analysis
- ⚔️ Compare Players
- 🌍 Player Space
- 🏆 Country Analytics
- 📊 Dataset Insights

Select a page from the **left sidebar** to begin.
""")

st.divider()

st.subheader("Machine Learning Pipeline")

st.markdown("""
- ✅ Data Scraping
- ✅ Data Cleaning
- ✅ Exploratory Data Analysis
- ✅ PCA Feature Engineering
- ✅ Player Performance Rating
- ✅ Similar Tournament Performance Engine
- ✅ K-Means Player Archetypes
""")

st.divider()

st.info(
    "Developed using Python, Pandas, Scikit-Learn, Plotly and Streamlit."
)