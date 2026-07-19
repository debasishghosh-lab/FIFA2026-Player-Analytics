import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ==========================================================
# Load Clustered Dataset
# ==========================================================

df = pd.read_csv("data/processed/clustered_dataset.csv")

# ==========================================================
# Features
# ==========================================================

FEATURES = [
    "Attacking Impact Score",
    "Passing Impact Score",
    "Defensive Impact Score",
    "Movement Impact Score"
]

# Ignore Goalkeeping Impact because it only exists for GKs

# ==========================================================
# Standardize Features
# ==========================================================

scaler = StandardScaler()

X = scaler.fit_transform(df[FEATURES])

# ==========================================================
# PCA
# ==========================================================

pca = PCA(n_components=2)

player_space = pca.fit_transform(X)

# ==========================================================
# Save Coordinates
# ==========================================================

df["PC1"] = player_space[:, 0]
df["PC2"] = player_space[:, 1]

# ==========================================================
# Explained Variance
# ==========================================================

print("=" * 60)
print("Player Space PCA")
print("=" * 60)

print(
    f"PC1 : {pca.explained_variance_ratio_[0] * 100:.2f}%"
)

print(
    f"PC2 : {pca.explained_variance_ratio_[1] * 100:.2f}%"
)

print(
    f"Total : {pca.explained_variance_ratio_.sum() * 100:.2f}%"
)

# ==========================================================
# PCA Loadings
# ==========================================================

print("\n")
print("=" * 60)
print("Feature Loadings")
print("=" * 60)

loadings = pd.DataFrame(
    pca.components_.T,
    columns=["PC1", "PC2"],
    index=FEATURES
)

print(loadings)

# ==========================================================
# Player Space Plot
# ==========================================================

colors = {
    "FW": "red",
    "MF": "blue",
    "DF": "green",
    "GK": "black"
}

plt.figure(figsize=(12, 9))

for position in df["Position"].unique():

    subset = df[df["Position"] == position]

    plt.scatter(
        subset["PC1"],
        subset["PC2"],
        color=colors.get(position, "gray"),
        alpha=0.7,
        label=position
    )

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.title("Football Player Space")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()

# ==========================================================
# Top Overall Performers
# ==========================================================

top = (
    df
    .sort_values(
        "Performance Rating",
        ascending=False
    )
    .head(20)
)

plt.figure(figsize=(12, 10))

for position in df["Position"].unique():

    subset = df[df["Position"] == position]

    plt.scatter(
        subset["PC1"],
        subset["PC2"],
        color=colors.get(position, "gray"),
        alpha=0.15
    )

plt.scatter(
    top["PC1"],
    top["PC2"],
    color="gold",
    s=80,
    edgecolors="black"
)

for _, row in top.iterrows():

    plt.text(
        row["PC1"],
        row["PC2"],
        row["Player"],
        fontsize=8
    )

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.title("Top Tournament Performers in Player Space")

plt.grid(True)

plt.tight_layout()

plt.show()

# ==========================================================
# Save Updated Dataset
# ==========================================================

df.to_csv(
    "data/processed/clustered_dataset.csv",
    index=False
)

print("\n")
print("=" * 60)
print("Dataset Updated")
print("=" * 60)

print("Saved -> data/processed/clustered_dataset.csv")