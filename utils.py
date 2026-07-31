from pathlib import Path
import pandas as pd
import streamlit as st

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# ==========================================================
# Resolve Base Directory & Data Path
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "processed" / "clustered_dataset.csv"

# ==========================================================
# Load Dataset
# ==========================================================

def load_data(path=None):
    if path is None:
        file_path = DEFAULT_DATA_PATH
    else:
        file_path = Path(path)
        if not file_path.is_absolute():
            file_path = BASE_DIR / file_path
    return pd.read_csv(file_path)


# ==========================================================
# APEX 26 Design System & CSS Theme Injection
# ==========================================================

def inject_apex_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');

        /* ---------- Global Theme & Pitch Atmosphere ---------- */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #F8FAFC;
        }

        .stApp {
            background: 
                radial-gradient(circle at 15% 15%, rgba(16, 185, 129, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(6, 182, 212, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(245, 158, 11, 0.04) 0%, transparent 60%),
                linear-gradient(180deg, #050811 0%, #0B1120 50%, #050811 100%);
            background-attachment: fixed;
        }

        /* ---------- Hide Default Streamlit Chrome ---------- */
        #MainMenu, footer, header, [data-testid="stHeader"] {
            visibility: hidden;
            display: none !important;
        }

        .block-container {
            padding: 2rem 2.5rem 4rem 2.5rem !important;
            max-width: 1440px !important;
        }

        /* ---------- Sidebar Styling ---------- */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #080D1A 0%, #050811 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 12px;
            margin: 4px 12px;
            padding: 10px 14px;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            color: #94A3B8 !important;
            transition: all 0.25s ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: rgba(16, 185, 129, 0.12) !important;
            color: #10B981 !important;
            transform: translateX(4px);
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 182, 212, 0.15)) !important;
            color: #F8FAFC !important;
            border-left: 4px solid #10B981;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.25);
        }

        /* ---------- Broadcast Hero Header ---------- */
        .apex-hero {
            background: linear-gradient(135deg, rgba(5, 46, 22, 0.9) 0%, rgba(11, 17, 32, 0.95) 50%, rgba(8, 13, 26, 0.95) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 24px;
            padding: 38px 42px;
            margin-bottom: 32px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }

        .apex-hero::before {
            content: "";
            position: absolute;
            top: 0; right: 0; bottom: 0; left: 0;
            background: radial-gradient(circle at 80% 20%, rgba(245, 158, 11, 0.15), transparent 50%);
            pointer-events: none;
        }

        .apex-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #34D399;
            padding: 6px 16px;
            border-radius: 9999px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 14px;
        }

        .apex-badge-pulse {
            width: 8px;
            height: 8px;
            background-color: #10B981;
            border-radius: 50%;
            box-shadow: 0 0 10px #10B981;
        }

        .apex-title {
            font-family: 'Outfit', sans-serif;
            font-size: 2.8rem;
            font-weight: 900;
            letter-spacing: -0.5px;
            line-height: 1.1;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #FFFFFF 30%, #F59E0B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .apex-subtitle {
            font-size: 1.05rem;
            color: #94A3B8;
            max-width: 820px;
            line-height: 1.65;
            margin: 0;
        }

        /* ---------- Glassmorphism Card Wrapper ---------- */
        .apex-card {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 28px 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .apex-card:hover {
            border-color: rgba(16, 185, 129, 0.3);
            box-shadow: 0 14px 36px rgba(16, 185, 129, 0.1);
        }

        /* ---------- Section Header ---------- */
        .apex-section-header {
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 800;
            color: #F8FAFC;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .apex-section-header-accent {
            width: 4px;
            height: 24px;
            background: linear-gradient(180deg, #F59E0B, #10B981);
            border-radius: 4px;
        }

        /* ---------- Custom Telemetry KPI Cards ---------- */
        [data-testid="stMetric"] {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.8), rgba(8, 13, 26, 0.9));
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 20px 22px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
            transition: transform 0.25s ease, border-color 0.25s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            border-color: rgba(6, 182, 212, 0.4);
        }

        [data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
            font-family: 'Outfit', sans-serif;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        [data-testid="stMetricValue"] {
            color: #FCD34D !important;
            font-family: 'JetBrains Mono', monospace;
            font-size: 2rem !important;
            font-weight: 800 !important;
        }

        /* ---------- FUT Player Card Component ---------- */
        .fut-card {
            background: linear-gradient(145deg, #0F172A 0%, #070B14 100%);
            border: 2px solid #F59E0B;
            border-radius: 24px;
            padding: 28px;
            position: relative;
            box-shadow: 0 15px 35px rgba(245, 158, 11, 0.15);
            overflow: hidden;
        }

        .fut-card::before {
            content: "APEX 26";
            position: absolute;
            right: -20px;
            top: 20px;
            font-family: 'Outfit', sans-serif;
            font-size: 4.5rem;
            font-weight: 900;
            color: rgba(255, 255, 255, 0.03);
            pointer-events: none;
            letter-spacing: 4px;
        }

        .fut-rating-shield {
            width: 72px;
            height: 84px;
            background: linear-gradient(135deg, #F59E0B 0%, #B45309 100%);
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
        }

        .fut-rating-num {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.8rem;
            font-weight: 900;
            color: #050811;
            line-height: 1;
        }

        .fut-rating-lbl {
            font-size: 0.65rem;
            font-weight: 800;
            color: #050811;
            letter-spacing: 1px;
        }

        /* ---------- Custom Dataframe ---------- */
        [data-testid="stDataFrame"] {
            border-radius: 16px !important;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        /* ---------- Custom Inputs & Selectboxes ---------- */
        div[data-baseweb="select"] {
            border-radius: 14px !important;
            background-color: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
        }

        /* ---------- Text & Number Inputs ---------- */
        div[data-baseweb="input"] {
            border-radius: 14px !important;
        }
        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea {
            background-color: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 14px !important;
            color: #F8FAFC !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* ---------- Slider ---------- */
        div[data-baseweb="slider"] {
            padding-top: 4px !important;
        }
        div[data-baseweb="slider"] [data-testid="stThumbValue"] {
            background: #10B981 !important;
            color: #050811 !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
        }

        /* ---------- Radio & Checkbox ---------- */
        div[data-baseweb="radio"] label,
        div[data-baseweb="checkbox"] label {
            color: #CBD5E1 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
        }
        div[data-baseweb="radio"] label:hover,
        div[data-baseweb="checkbox"] label:hover {
            color: #F8FAFC !important;
        }

        /* ---------- Tabs ---------- */
        button[data-baseweb="tab"] {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            color: #94A3B8 !important;
            border-radius: 12px 12px 0 0 !important;
            padding: 10px 20px !important;
            transition: all 0.2s ease !important;
        }
        button[data-baseweb="tab"]:hover {
            color: #F8FAFC !important;
            background: rgba(255, 255, 255, 0.04) !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #10B981 !important;
            background: rgba(16, 185, 129, 0.08) !important;
            border-bottom: 3px solid #10B981 !important;
        }
        div[data-baseweb="tab-border"] {
            border-color: rgba(255, 255, 255, 0.08) !important;
        }

        /* ---------- Progress bar ---------- */
        .stProgress > div > div {
            background: linear-gradient(90deg, #10B981, #06B6D4) !important;
            border-radius: 9999px;
        }

        /* ---------- Tooltips ---------- */
        div[data-testid="stTooltip"] {
            background: rgba(15, 23, 42, 0.95) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
        }

        /* ---------- Alerts & Info Boxes ---------- */
        .stAlert {
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        /* ---------- Expander ---------- */
        details[data-testid="stExpander"] {
            background: rgba(15, 23, 42, 0.5) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
        }
        details[data-testid="stExpander"] summary {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            color: #F8FAFC !important;
        }

        /* ---------- Spinner ---------- */
        .stSpinner > div {
            border-color: #10B981 transparent transparent transparent !important;
        }

        /* ---------- Divider ---------- */
        .apex-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.3), transparent);
            margin: 2rem 0;
            border: none;
        }

        /* ---------- Keyframe Animations ---------- */
        @keyframes apexFadeIn {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes apexSlideUp {
            from { opacity: 0; transform: translateY(24px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes apexPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        .apex-fade-in { animation: apexFadeIn 0.6s ease-out both; }
        .apex-slide-up { animation: apexSlideUp 0.7s ease-out both; }

        /* ---------- Empty State ---------- */
        .apex-empty {
            text-align: center;
            padding: 3rem 2rem;
            color: #64748B;
        }
        .apex-empty-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }
        .apex-empty-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: #94A3B8;
            margin-bottom: 0.5rem;
        }
        .apex-empty-desc {
            font-size: 0.9rem;
            color: #64748B;
            max-width: 400px;
            margin: 0 auto;
            line-height: 1.5;
        }

        /* ---------- Pitch Geometry Subtle Background ---------- */
        .apex-pitch-lines {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            pointer-events: none;
            z-index: 0;
            opacity: 0.015;
            background-image:
                repeating-linear-gradient(0deg, transparent, transparent 99px, rgba(255,255,255,0.5) 99px, rgba(255,255,255,0.5) 100px),
                repeating-linear-gradient(90deg, transparent, transparent 99px, rgba(255,255,255,0.5) 99px, rgba(255,255,255,0.5) 100px);
        }

        /* ---------- KPI Card Grid ---------- */
        .apex-kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        .apex-kpi-card {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.8), rgba(8, 13, 26, 0.9));
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.3rem 1.4rem;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .apex-kpi-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
        }
        .apex-kpi-card::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            border-radius: 16px 16px 0 0;
        }
        .apex-kpi-card.accent-green::before  { background: linear-gradient(90deg, #059669, #10B981); }
        .apex-kpi-card.accent-cyan::before   { background: linear-gradient(90deg, #0891B2, #06B6D4); }
        .apex-kpi-card.accent-amber::before  { background: linear-gradient(90deg, #D97706, #F59E0B); }
        .apex-kpi-card.accent-rose::before   { background: linear-gradient(90deg, #E11D48, #FB7185); }
        .apex-kpi-label {
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: rgba(255, 255, 255, 0.45);
            margin-bottom: 0.35rem;
        }
        .apex-kpi-value {
            font-size: 1.9rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            color: #F8FAFC;
            line-height: 1;
        }
        .apex-kpi-sub {
            font-size: 0.72rem;
            color: rgba(255, 255, 255, 0.4);
            margin-top: 0.35rem;
        }

        /* ---------- Data Card Wrapper ---------- */
        .apex-data-card {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.7), rgba(8, 13, 26, 0.85));
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 18px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25);
        }

        /* ---------- Plotly Container ---------- */
        .stPlotlyChart > div {
            border-radius: 14px;
            overflow: hidden;
        }

    </style>
    """, unsafe_allow_html=True)


def get_apex_plotly_layout(title=""):
    return dict(
        title=dict(
            text=title,
            font=dict(family="Outfit", size=18, color="#F8FAFC"),
            x=0.02
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#94A3B8"),
        margin=dict(l=40, r=40, t=60, b=40)
    )


# ==========================================================
# Reusable UI Component Helpers
# ==========================================================

def apex_hero(badge_text, title, subtitle):
    """Render a broadcast-style hero banner."""
    st.markdown(f"""
    <div class="apex-hero">
        <div class="apex-badge">
            <span class="apex-badge-pulse"></span>
            {badge_text}
        </div>
        <div class="apex-title">{title}</div>
        <div class="apex-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def apex_section_header(title):
    """Render a consistent section header with accent bar."""
    st.markdown(f"""
    <div class="apex-section-header">
        <div class="apex-section-header-accent"></div>
        <span>{title}</span>
    </div>
    """, unsafe_allow_html=True)


def apex_card_start():
    """Open a glassmorphism card wrapper."""
    st.markdown('<div class="apex-card">', unsafe_allow_html=True)


def apex_card_end():
    """Close a glassmorphism card wrapper."""
    st.markdown('</div>', unsafe_allow_html=True)


def apex_kpi_grid(items):
    """Render a grid of KPI cards. items: list of (label, value, sub_text, accent) tuples.
    accent: 'green', 'cyan', 'amber', 'rose'
    """
    cols_html = ""
    for label, value, sub, accent in items:
        cols_html += f"""
        <div class="apex-kpi-card accent-{accent}">
            <div class="apex-kpi-label">{label}</div>
            <div class="apex-kpi-value">{value}</div>
            <div class="apex-kpi-sub">{sub}</div>
        </div>"""
    st.markdown(f'<div class="apex-kpi-grid">{cols_html}</div>', unsafe_allow_html=True)


def apex_empty_state(icon, title, description):
    """Render an empty state placeholder."""
    st.markdown(f"""
    <div class="apex-empty">
        <div class="apex-empty-icon">{icon}</div>
        <div class="apex-empty-title">{title}</div>
        <div class="apex-empty-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def apex_divider():
    """Render a subtle gradient divider."""
    st.markdown('<div class="apex-divider"></div>', unsafe_allow_html=True)


# ==========================================================
# Player Lookup & Helper Logic
# ==========================================================

def get_player_lookup(df):
    return df.set_index("Player")


def get_player_list(df):
    return sorted(df["Player"].unique())


def get_player(player_lookup, player_name):
    return player_lookup.loc[player_name]


def is_goalkeeper(player):
    return player["Position"] == "GK"


def get_archetype_average(df, archetype):
    return df[
        (df["Player Archetype"] == archetype)
        &
        (df["Position"] != "GK")
    ]


def create_rating_columns(df):
    features = [
        "Attacking Impact Score",
        "Passing Impact Score",
        "Defensive Impact Score",
        "Movement Impact Score"
    ]

    for feature in features:
        rating = feature.replace("Impact Score", "Rating")
        df[rating] = (
            (df[feature] - df[feature].min())
            /
            (df[feature].max() - df[feature].min())
            * 100
        ).round(1)

    return df


# ==========================================================
# Similar Performance Engine
# ==========================================================

SIMILARITY_FEATURES = [
    "Attacking Impact Score",
    "Passing Impact Score",
    "Defensive Impact Score",
    "Movement Impact Score"
]


def get_similar_players(df, player_name, top_n=5):
    players = df[df["Position"] != "GK"].copy()
    scaler = StandardScaler()
    X = scaler.fit_transform(players[SIMILARITY_FEATURES])

    model = NearestNeighbors(
        n_neighbors=top_n + 1,
        metric="euclidean"
    )
    model.fit(X)

    idx = players.index[players["Player"] == player_name][0]
    pos = players.index.get_loc(idx)

    distances, indices = model.kneighbors(X[pos].reshape(1, -1))
    nearest_distances = distances[0][1:]

    min_dist = nearest_distances.min()
    max_dist = nearest_distances.max()

    results = []

    for d, i in zip(nearest_distances, indices[0][1:]):
        row = players.iloc[i]
        if max_dist == min_dist:
            similarity = 100.0
        else:
            similarity = 100 - ((d - min_dist) / (max_dist - min_dist)) * 20

        similarity = round(similarity, 1)

        results.append({
            "Player": row["Player"],
            "Country": row["Country"],
            "Position": row["Position"],
            "Performance Rating": row["Performance Rating"],
            "Distance": round(float(d), 3),
            "Similarity": similarity
        })

    return pd.DataFrame(results)
