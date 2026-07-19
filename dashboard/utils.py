import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# ==========================================================
# Load Dataset
# ==========================================================

def load_data(path="data/processed/clustered_dataset.csv"):
    return pd.read_csv(path)


# ==========================================================
# Player Lookup
# ==========================================================

def get_player_lookup(df):
    return df.set_index("Player")


# ==========================================================
# Player List
# ==========================================================

def get_player_list(df):
    return sorted(df["Player"].unique())


# ==========================================================
# Get Player
# ==========================================================

def get_player(player_lookup, player_name):
    return player_lookup.loc[player_name]


# ==========================================================
# Goalkeeper Check
# ==========================================================

def is_goalkeeper(player):
    return player["Position"] == "GK"


# ==========================================================
# Archetype Average
# ==========================================================

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

        rating = feature.replace(
            "Impact Score",
            "Rating"
        )

        df[rating] = (
            (
                df[feature] - df[feature].min()
            )
            /
            (
                df[feature].max() - df[feature].min()
            )
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
    """
    Returns players with the most similar tournament performances.
    """

    # Only compare outfield players
    players = df[df["Position"] != "GK"].copy()

    scaler = StandardScaler()

    X = scaler.fit_transform(players[SIMILARITY_FEATURES])

    model = NearestNeighbors(
        n_neighbors=top_n + 1,
        metric="euclidean"
    )

    model.fit(X)

    # Find selected player
    idx = players.index[
        players["Player"] == player_name
    ][0]

    pos = players.index.get_loc(idx)

    distances, indices = model.kneighbors(
        X[pos].reshape(1, -1)
    )

    # Normalize only among returned neighbours
    nearest_distances = distances[0][1:]

    min_dist = nearest_distances.min()
    max_dist = nearest_distances.max()

    results = []

    for d, i in zip(
        nearest_distances,
        indices[0][1:]
    ):

        row = players.iloc[i]

        if max_dist == min_dist:
            similarity = 100.0
        else:
            similarity = 100 - (
                (d - min_dist)
                /
                (max_dist - min_dist)
            ) * 20

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