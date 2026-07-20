import streamlit as st

st.set_page_config(
    page_title="FIFA World Cup 2026 Analytics",
    page_icon="⚽",
    layout="wide"
)

# ──────────────────────────────────────────────
# CUSTOM CSS — Premium Dark Football Dashboard Theme
# ──────────────────────────────────────────────
st.markdown("""
<style>

    /* ---------- Global ---------- */
    .stApp {
        background: radial-gradient(circle at top left, #0B1220 0%, #111827 45%, #0B1220 100%);
        color: #FFFFFF;
    }

    #MainMenu, footer {visibility: hidden;}

    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
    }

    /* ---------- Animations ---------- */
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(12px);}
        to {opacity: 1; transform: translateY(0);}
    }
    @keyframes slideUp {
        from {opacity: 0; transform: translateY(30px);}
        to {opacity: 1; transform: translateY(0);}
    }

    .fade-in { animation: fadeIn 0.8s ease-out; }
    .slide-up { animation: slideUp 0.9s ease-out; }

    /* ---------- Hero Section ---------- */
    .hero-container {
        background: linear-gradient(135deg, #006847 0%, #0B1220 60%, #111827 100%);
        border-radius: 20px;
        padding: 48px 40px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0, 104, 71, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
        animation: fadeIn 1s ease-out;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 6px;
        background: linear-gradient(90deg, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #D1D5DB;
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto;
    }

    .hero-icons {
        font-size: 28px;
        margin-bottom: 14px;
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
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        animation: slideUp 0.8s ease-out;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 28px rgba(0, 191, 255, 0.15);
    }

    /* ---------- Section Header ---------- */
    .section-header {
        font-size: 24px;
        font-weight: 700;
        margin: 10px 0 18px 0;
        padding-left: 14px;
        border-left: 5px solid #FFD700;
        background: linear-gradient(90deg, #FFFFFF, #9CA3AF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ---------- Feature List Items ---------- */
    .feature-item {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 10px;
        font-size: 16px;
        transition: background 0.2s ease, transform 0.2s ease;
    }

    .feature-item:hover {
        background: rgba(0, 104, 71, 0.18);
        transform: translateX(4px);
    }

    /* ---------- Pipeline Steps ---------- */
    .pipeline-item {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(34, 197, 94, 0.08);
        border: 1px solid rgba(34, 197, 94, 0.25);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
        font-size: 15px;
        color: #E5E7EB;
        transition: background 0.2s ease;
    }

    .pipeline-item:hover {
        background: rgba(34, 197, 94, 0.16);
    }

    /* ---------- Divider ---------- */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 34px 0;
        border: none;
        opacity: 0.6;
    }

    /* ---------- Info Box ---------- */
    .stAlert {
        border-radius: 16px !important;
        border: 1px solid rgba(0, 191, 255, 0.25) !important;
    }

    /* ---------- Sidebar hint text ---------- */
    .sidebar-hint {
        text-align: center;
        color: #9CA3AF;
        font-size: 14px;
        margin-top: 8px;
    }

</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# HERO SECTION
# ──────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-icons">⚽ 🏆 🌎</div>
    <div class="hero-title">FIFA World Cup 2026</div>
    <div class="hero-title" style="font-size:30px;">Player Analytics Dashboard</div>
    <div class="hero-subtitle">
        Explore comprehensive player statistics across every performance category.
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# WELCOME / OVERVIEW CARD
# ──────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown("""
Welcome to the **FIFA World Cup 2026 Analytics Dashboard**.

This project uses Machine Learning techniques to analyze player performances
from the FIFA World Cup 2026.(Based On Data  till 16th june 2026)
""")

st.markdown('<div class="section-header">✨ Features</div>', unsafe_allow_html=True)

features = [
    ("👤", "Player Analysis"),
    ("⚔️", "Compare Players"),
    ("🌍", "Player Space"),
    ("🏆", "Country Analytics"),
    ("📊", "Dataset Insights"),
]

col1, col2 = st.columns(2)
for i, (icon, label) in enumerate(features):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.markdown(f"""
        <div class="feature-item">
            <span style="font-size:22px;">{icon}</span>
            <span>{label}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown(
    '<p class="sidebar-hint">👈 Select a page from the left sidebar to begin.</p>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DIVIDER
# ──────────────────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# ML PIPELINE CARD
# ──────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown('<div class="section-header">🧠 Machine Learning Pipeline</div>', unsafe_allow_html=True)

pipeline_steps = [
    "Data Scraping",
    "Data Cleaning",
    "Exploratory Data Analysis",
    "PCA Feature Engineering",
    "Player Performance Rating",
    "Similar Tournament Performance Engine",
    "K-Means Player Archetypes",
]

p_col1, p_col2 = st.columns(2)
for i, step in enumerate(pipeline_steps):
    target_col = p_col1 if i % 2 == 0 else p_col2
    with target_col:
        st.markdown(f"""
        <div class="pipeline-item">
            <span style="color:#22C55E; font-size:18px;">✅</span>
            <span>{step}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DIVIDER
# ──────────────────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TECH STACK INFO
# ──────────────────────────────────────────────
st.info(
    "🛠️ Developed using **Python**, **Pandas**, **Scikit-Learn**, **Plotly** and **Streamlit**."
)