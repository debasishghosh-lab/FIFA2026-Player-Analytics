import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv("data/processed/engineered_dataset.csv")

# ==========================================================
# Features
# ==========================================================

FEATURES = [
    "Attacking Impact Score",
    "Passing Impact Score",
    "Defensive Impact Score",
    "Movement Impact Score"
]

# Ignore goalkeepers for clustering
players = df[df["Position"] != "GK"].copy()

# ==========================================================
# Standardize Features
# ==========================================================

scaler = StandardScaler()

X = scaler.fit_transform(players[FEATURES])

# ==========================================================
# Elbow Method + Silhouette Score
# ==========================================================

k_values = range(2, 11)

inertia = []
silhouette = []

for k in k_values:

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X)

    inertia.append(model.inertia_)

    silhouette.append(
        silhouette_score(X, labels)
    )

results = pd.DataFrame({
    "K": list(k_values),
    "Inertia": inertia,
    "Silhouette Score": silhouette
})

print("=" * 60)
print("Choosing Number of Clusters")
print("=" * 60)

print(results)

# ==========================================================
# Elbow Plot
# ==========================================================

plt.figure(figsize=(8,5))

plt.plot(
    k_values,
    inertia,
    marker="o",
    linewidth=2
)

plt.title("Elbow Method")

plt.xlabel("Number of Clusters")

plt.ylabel("Inertia")

plt.grid(True)

plt.tight_layout()

plt.show()

# ==========================================================
# Silhouette Plot
# ==========================================================

plt.figure(figsize=(8,5))

plt.plot(
    k_values,
    silhouette,
    marker="o",
    linewidth=2
)

plt.title("Silhouette Score")

plt.xlabel("Number of Clusters")

plt.ylabel("Silhouette Score")

plt.grid(True)

plt.tight_layout()

plt.show()

# ==========================================================
# Final Model
# ==========================================================

print("\n")
print("=" * 60)
print("Training Final Model (K = 6)")
print("=" * 60)

kmeans = KMeans(
    n_clusters=6,
    random_state=42,
    n_init=10
)

players["Cluster"] = kmeans.fit_predict(X)

cluster_names = {
    0: "Balanced Contributors",
    1: "Dynamic Attackers",
    2: "Limited Tournament Impact",
    3: "Complete Midfielders",
    4: "Tournament Superstars",
    5: "Elite All-Round Performers"
}

players["Player Archetype"] = players["Cluster"].map(cluster_names)

# ==========================================================
# Merge Back
# ==========================================================

df["Cluster"] = -1
df["Player Archetype"] = "Goalkeeper"

df.loc[players.index, "Cluster"] = players["Cluster"]
df.loc[players.index, "Player Archetype"] = players["Player Archetype"]

# ==========================================================
# Cluster Sizes
# ==========================================================

print("\n")
print("=" * 60)
print("Cluster Sizes")
print("=" * 60)

print(
    players["Cluster"]
    .value_counts()
    .sort_index()
)

# ==========================================================
# Cluster Summary
# ==========================================================

print("\n")
print("=" * 60)
print("Cluster Summary")
print("=" * 60)

cluster_summary = (
    players
    .groupby("Cluster")[FEATURES]
    .mean()
)

print(cluster_summary)

# ==========================================================
# Player Space Visualization
# ==========================================================

pca = PCA(n_components=2)

player_space = pca.fit_transform(X)

players["PC1"] = player_space[:, 0]
players["PC2"] = player_space[:, 1]

plt.figure(figsize=(12,8))

scatter = plt.scatter(
    players["PC1"],
    players["PC2"],
    c=players["Cluster"],
    cmap="tab10",
    alpha=0.75
)

plt.xlabel("Player Space Dimension 1")
plt.ylabel("Player Space Dimension 2")

plt.title("Player Archetypes (K-Means Clustering)")

plt.colorbar(scatter, label="Cluster")

plt.grid(True)

plt.tight_layout()

plt.show()

# ==========================================================
# Overall Performance Score
# ==========================================================

from sklearn.preprocessing import MinMaxScaler

score_scaler = MinMaxScaler()

scaled_scores = df[FEATURES].copy()

scaled_scores = pd.DataFrame(
    score_scaler.fit_transform(scaled_scores),
    columns=FEATURES,
    index=df.index
)

df["Overall Performance Score"] = (
    scaled_scores.sum(axis=1)
)

df["Performance Rating"] = (
    df["Overall Performance Score"]
    / df["Overall Performance Score"].max()
    * 100
).round(1)

# ==========================================================
# Goalkeeping Rating (Goalkeepers Only)
# ==========================================================

from sklearn.preprocessing import MinMaxScaler

gk_mask = df["Position"] == "GK"

gk_scaler = MinMaxScaler()

df["Goalkeeping Rating"] = pd.NA

df.loc[gk_mask, "Goalkeeping Rating"] = (
    gk_scaler.fit_transform(
        df.loc[gk_mask, ["Goalkeeping Impact Score"]]
    ).flatten() * 100
).round(1)

# ==========================================================
# Save Dataset
# ==========================================================

df.to_csv(
    "data/processed/clustered_dataset.csv",
    index=False
)

print("\n")
print("=" * 60)
print("Dataset Saved")
print("=" * 60)
print("Saved -> data/processed/clustered_dataset.csv")