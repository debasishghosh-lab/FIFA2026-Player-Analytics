import sys
import importlib.util
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) in sys.path:
    sys.path.remove(str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR))

utils_path = (BASE_DIR / "utils.py").resolve()
if "utils" in sys.modules:
    loaded_file = Path(getattr(sys.modules["utils"], "__file__", "")).resolve()
    if loaded_file != utils_path:
        del sys.modules["utils"]

if "utils" not in sys.modules:
    spec = importlib.util.spec_from_file_location("utils", utils_path)
    utils = importlib.util.module_from_spec(spec)
    sys.modules["utils"] = utils
    spec.loader.exec_module(utils)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils import (
    inject_apex_theme,
    apex_hero,
    apex_section_header,
    apex_card_start,
    apex_card_end,
    apex_empty_state,
    apex_divider,
    create_rating_columns,
    load_data,
    get_player_lookup,
    get_player_list
)

st.set_page_config(
    page_title="Compare Players | APEX 26",
    page_icon="⚔️",
    layout="wide"
)

inject_apex_theme()

df = load_data()
df = create_rating_columns(df)
player_lookup = get_player_lookup(df)
players = get_player_list(df)

# ──────────────────────────────────────────────
# PAGE HEADER
# ──────────────────────────────────────────────
apex_hero(
    "Head-to-Head Tactical Duel",
    "PLAYER COMPARISON",
    "Compare tournament performances of any two players using machine learning performance ratings and radar overlay analysis."
)

# ──────────────────────────────────────────────
# PLAYER SELECTION
# ──────────────────────────────────────────────
apex_card_start()

col1, col2 = st.columns(2)
with col1:
    player_one = st.selectbox("Player 1", players, index=0, key="player_one")
with col2:
    player_two = st.selectbox("Player 2", players, index=1 if len(players) > 1 else 0, key="player_two")

apex_card_end()

p1 = player_lookup.loc[player_one]
p2 = player_lookup.loc[player_two]

# ──────────────────────────────────────────────
# PREVENT GOALKEEPER COMPARISON
# ──────────────────────────────────────────────
if p1["Position"] == "GK" or p2["Position"] == "GK":
    apex_empty_state("🧤", "Goalkeeper Comparison", "Tactical radar comparison will be available in a future update. Goalkeeper analytics use a separate telemetry model.")
    st.stop()

# ──────────────────────────────────────────────
# PLAYER HEAD-TO-HEAD CARDS
# ──────────────────────────────────────────────
apex_card_start()
apex_section_header("PLAYER OVERVIEW")

left, right = st.columns(2)

with left:
    st.markdown(f"""
    <div class="compare-card" style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(15, 23, 42, 0.6) 100%); border: 1px solid rgba(6, 182, 212, 0.25); border-radius: 18px; padding: 24px; text-align: center;">
        <div class="compare-player-name" style="font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 900; color: #06B6D4; margin-bottom: 4px;">{player_one}</div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #94A3B8; margin-bottom: 16px;">{p1['Country']} · {p1['Position']}</div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; font-weight: 900; color: #FCD34D;">{p1['Performance Rating']:.1f}<span style="font-size: 0.9rem; color: #64748B;">/100</span></div>
        <div style="font-size: 0.72rem; color: #64748B; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;">Performance Rating</div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="compare-card" style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(15, 23, 42, 0.6) 100%); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 18px; padding: 24px; text-align: center;">
        <div class="compare-player-name" style="font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 900; color: #F59E0B; margin-bottom: 4px;">{player_two}</div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #94A3B8; margin-bottom: 16px;">{p2['Country']} · {p2['Position']}</div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; font-weight: 900; color: #FCD34D;">{p2['Performance Rating']:.1f}<span style="font-size: 0.9rem; color: #64748B;">/100</span></div>
        <div style="font-size: 0.72rem; color: #64748B; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;">Performance Rating</div>
    </div>
    """, unsafe_allow_html=True)

apex_card_end()

# ──────────────────────────────────────────────
# RADAR COMPARISON
# ──────────────────────────────────────────────
apex_card_start()
apex_section_header("PERFORMANCE RADAR COMPARISON")

categories = ["Attack", "Passing", "Defense", "Movement"]

p1_values = [p1["Attacking Rating"], p1["Passing Rating"], p1["Defensive Rating"], p1["Movement Rating"]]
p2_values = [p2["Attacking Rating"], p2["Passing Rating"], p2["Defensive Rating"], p2["Movement Rating"]]

categories_closed = categories + [categories[0]]
p1_closed = p1_values + [p1_values[0]]
p2_closed = p2_values + [p2_values[0]]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=p1_closed,
    theta=categories_closed,
    fill="toself",
    name=player_one,
    line=dict(color="#06B6D4", width=3),
    fillcolor="rgba(6, 182, 212, 0.35)"
))

fig.add_trace(go.Scatterpolar(
    r=p2_closed,
    theta=categories_closed,
    fill="toself",
    name=player_two,
    line=dict(color="#F59E0B", width=3),
    fillcolor="rgba(245, 158, 11, 0.35)"
))

fig.update_layout(
    polar=dict(
        bgcolor="rgba(0,0,0,0)",
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickvals=[20, 40, 60, 80, 100],
            gridcolor="rgba(255,255,255,0.08)"
        ),
        angularaxis=dict(
            gridcolor="rgba(255,255,255,0.08)",
            tickfont=dict(family="Outfit", size=13, color="#F8FAFC")
        )
    ),
    template="plotly_dark",
    legend=dict(
        orientation="h",
        y=1.08,
        x=0.25,
        font=dict(family="Inter", color="#94A3B8")
    ),
    height=580,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=40, r=40, t=60, b=40)
)

st.plotly_chart(fig, use_container_width=True)

apex_card_end()

# ──────────────────────────────────────────────
# NUMERICAL COMPARISON TABLE
# ──────────────────────────────────────────────
apex_card_start()
apex_section_header("RATING BREAKDOWN")

comparison = pd.DataFrame({
    "Metric": ["Performance", "Attack", "Passing", "Defense", "Movement"],
    player_one: [
        p1["Performance Rating"],
        p1["Attacking Rating"],
        p1["Passing Rating"],
        p1["Defensive Rating"],
        p1["Movement Rating"]
    ],
    player_two: [
        p2["Performance Rating"],
        p2["Attacking Rating"],
        p2["Passing Rating"],
        p2["Defensive Rating"],
        p2["Movement Rating"]
    ]
})

comparison[player_one] = comparison[player_one].round(1)
comparison[player_two] = comparison[player_two].round(1)

st.dataframe(comparison, hide_index=True, use_container_width=True)

apex_card_end()

apex_divider()
