import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# ======================================================
# Load Engineered Dataset
# ======================================================

df = pd.read_csv("data/processed/engineered_dataset.csv")

# ======================================================
# Feature Space
# ======================================================

FEATURES = [
    "Attacking Impact Score",
    "Passing Impact Score",
    "Defensive Impact Score",
    "Movement Impact Score"
]

# Ignore Goalkeeping for now

players = df[df["Position"] != "GK"].copy()

# ======================================================
# Standardize
# ======================================================

scaler = StandardScaler()

X = scaler.fit_transform(players[FEATURES])

# ======================================================
# Train Similarity Model
# ======================================================

model = NearestNeighbors(
    n_neighbors=6,
    metric="euclidean"
)

model.fit(X)

# ======================================================
# Player Search
# ======================================================

player_name = input("\nEnter Player Name: ").strip()

matches = players[
    players["Player"].str.lower() == player_name.lower()
]

if matches.empty:

    print("\nPlayer not found.")

    exit()

player_index = matches.index[0]

vector_index = players.index.get_loc(player_index)

distances, indices = model.kneighbors(
    [X[vector_index]]
)

print("\n")

print("=" * 70)
print(f"Closest Performance Profiles to {player_name.title()}")
print("=" * 70)
print("(Based on FIFA World Cup 2026 tournament statistics)")
print()

for distance, idx in zip(
    distances[0][1:],
    indices[0][1:]
):

    row = players.iloc[idx]

    print(
        f"{row['Player']:<25}"
        f"{row['Country']:<6}"
        f"{row['Position']:<4}"
        f"Distance : {distance:.3f}"
    )