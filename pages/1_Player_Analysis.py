import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

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
    load_data,
    create_rating_columns,
    get_player_lookup,
    get_player_list,
    get_similar_players
)

st.set_page_config(
    page_title="Player Scouting Dossier | APEX 26",
    page_icon="👤",
    layout="wide"
)

inject_apex_theme()

df = load_data()
df = create_rating_columns(df)

player_lookup = get_player_lookup(df)
players = get_player_list(df)

# Sidebar Branding
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 4px 14px 4px;">
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.2rem; font-weight: 900; color: #10B981;">
            MODULE // SCOUTING DOSSIER
        </div>
        <div style="font-size: 0.72rem; color: #94A3B8;">FIFA World Cup 2026 Telemetry</div>
    </div>
    """, unsafe_allow_html=True)

# Page Header
apex_hero(
    "Technical Dossier // Player Intelligence",
    "PLAYER ANALYTICS & SIMILARITY",
    "Individual performance breakdown, polar tactical radar comparison against archetype benchmarks, and high-dimensional similarity profile matching."
)

# Search Bar Card
apex_card_start()
selected_player = st.selectbox(
    "SEARCH PLAYER DOSSIER",
    options=players,
    index=None,
    placeholder="Type player name (e.g. Lionel Messi, Kylian Mbappe, Aaron Hickey)..."
)
apex_card_end()

if selected_player is None:
    apex_empty_state(
        "⚽",
        "No Player Selected",
        "Search and select a player above to load their complete scouting dossier with tactical radar and similarity matches."
    )
    st.stop()

player = player_lookup.loc[selected_player]

icons = {
    "Tournament Superstars": "⭐",
    "Elite All-Round Performers": "🏆",
    "Dynamic Attackers": "⚡",
    "Complete Midfielders": "🎯",
    "Balanced Contributors": "⚽",
    "Limited Tournament Impact": "📉"
}

# ──────────────────────────────────────────────
# PLAYER FUT CARD HUD
# ──────────────────────────────────────────────
st.markdown('<div class="fut-card">', unsafe_allow_html=True)
col_card_l, col_card_r = st.columns([1, 3])

with col_card_l:
    rating_val = player["Goalkeeping Rating"] if player["Position"] == "GK" else player["Performance Rating"]
    rating_label = "GK" if player["Position"] == "GK" else "OVR"
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
        <div class="fut-rating-shield">
            <div class="fut-rating-num">{rating_val:.0f}</div>
            <div class="fut-rating-lbl">{rating_label}</div>
        </div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.4rem; font-weight: 900; color: #F59E0B; margin-top: 12px; text-align: center;">
            {player['Position']}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_card_r:
    st.markdown(f"""
    <div style="font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 900; color: #F8FAFC; margin-bottom: 4px;">
        {selected_player}
    </div>
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; color: #10B981; font-weight: 700; margin-bottom: 20px;">
        🌍 {player['Country']} &nbsp;|&nbsp; ⚽ {player['Position']}
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("GOALS", int(player["Goals"]))
    with m2:
        st.metric("ASSISTS", int(player["Assists"]))
    with m3:
        mins = player["Minutes Played"]
        st.metric("MINUTES", int(mins) if pd.notna(mins) else "-")
    with m4:
        archetype_name = str(player.get("Player Archetype", "Goalkeeper"))
        archetype_icon = icons.get(archetype_name, "⚽")
        st.metric("ARCHETYPE", f"{archetype_icon} {archetype_name[:18]}")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TACTICAL RADAR CHART & RATINGS
# ──────────────────────────────────────────────
if player["Position"] != "GK":
    col_rad, col_rat = st.columns([3, 2])

    with col_rad:
        apex_card_start()
        apex_section_header("TACTICAL POLAR RADAR")

        labels = ["Attack", "Passing", "Defense", "Movement"]
        player_values = [
            player["Attacking Rating"],
            player["Passing Rating"],
            player["Defensive Rating"],
            player["Movement Rating"]
        ]

        archetype_df = df[(df["Player Archetype"] == player["Player Archetype"]) & (df["Position"] != "GK")]
        average_values = [
            archetype_df["Attacking Rating"].mean(),
            archetype_df["Passing Rating"].mean(),
            archetype_df["Defensive Rating"].mean(),
            archetype_df["Movement Rating"].mean()
        ]

        labels_closed = labels + [labels[0]]
        player_closed = player_values + [player_values[0]]
        average_closed = average_values + [average_values[0]]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=average_closed,
            theta=labels_closed,
            fill="toself",
            name=f"Avg {player['Player Archetype']}",
            line=dict(color="#94A3B8", width=2, dash="dash"),
            fillcolor="rgba(148, 163, 184, 0.2)"
        ))

        fig.add_trace(go.Scatterpolar(
            r=player_closed,
            theta=labels_closed,
            fill="toself",
            name=selected_player,
            line=dict(color="#06B6D4", width=3),
            fillcolor="rgba(6, 182, 212, 0.4)"
        ))

        fig.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 100], tickvals=[20, 40, 60, 80, 100], gridcolor="rgba(255,255,255,0.1)"),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", font=dict(family="Outfit", size=13, color="#F8FAFC"))
            ),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(orientation="h", y=1.1, x=0.1, font=dict(family="Inter", color="#94A3B8")),
            height=480,
            margin=dict(l=40, r=40, t=60, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)
        apex_card_end()

    with col_rat:
        apex_card_start()
        apex_section_header("ATTRIBUTE METRICS")

        st.markdown(f"**Attacking Rating** `{player['Attacking Rating']:.0f} / 100`")
        st.progress(player["Attacking Rating"] / 100)

        st.markdown(f"**Passing Rating** `{player['Passing Rating']:.0f} / 100`")
        st.progress(player["Passing Rating"] / 100)

        st.markdown(f"**Defending Rating** `{player['Defensive Rating']:.0f} / 100`")
        st.progress(player["Defensive Rating"] / 100)

        st.markdown(f"**Movement Rating** `{player['Movement Rating']:.0f} / 100`")
        st.progress(player["Movement Rating"] / 100)

        apex_card_end()

else:
    apex_card_start()
    apex_section_header("GOALKEEPER TELEMETRY")

    gk_col1, gk_col2, gk_col3 = st.columns(3)
    with gk_col1:
        saves = player["Goalkeeper Saves"]
        st.metric("SAVES", "-" if pd.isna(saves) else int(saves))
    with gk_col2:
        inside = player["Goalkeeper Actions Inside the Penalty Area"]
        st.metric("INSIDE AREA ACTIONS", "-" if pd.isna(inside) else int(inside))
    with gk_col3:
        outside = player["Goalkeeper Actions Outside the Penalty Area"]
        st.metric("OUTSIDE AREA ACTIONS", "-" if pd.isna(outside) else int(outside))

    apex_card_end()

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 5 NEAREST SIMILAR PLAYER PROFILES
# ──────────────────────────────────────────────
apex_card_start()
apex_section_header("NEAREST PERFORMANCE SIMILARITY MATCHES")

if player["Position"] != "GK":
    similar_players = get_similar_players(df, selected_player, top_n=5)
    medals = ["#1", "#2", "#3", "#4", "#5"]

    for i, (_, row) in enumerate(similar_players.iterrows()):
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 18px 24px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(6,182,212,0.2)); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 800; color: #10B981;">{medals[i]}</div>
                <div>
                    <div style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 800; color: #F8FAFC;">{row['Player']}</div>
                    <div style="font-size: 0.82rem; color: #94A3B8;">{row['Country']} · {row['Position']}</div>
                </div>
            </div>
            <div style="display: flex; gap: 28px; text-align: right;">
                <div>
                    <div style="font-size: 0.7rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Rating</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 800; color: #FCD34D;">{row['Performance Rating']:.1f}</div>
                </div>
                <div>
                    <div style="font-size: 0.7rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Similarity</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 800; color: #10B981;">{row['Similarity']:.1f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    apex_empty_state("🧤", "Goalkeeper Mode", "Similarity engine is active for outfield player positions only.")

apex_card_end()
