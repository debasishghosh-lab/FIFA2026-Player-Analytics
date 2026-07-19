import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ============================================================
# Load Dataset
# ============================================================

df = pd.read_csv("data/processed/cleaned_dataset.csv")

# ============================================================
# Attacking Features
# ============================================================

ATTACKING = [
    "Goals",
    "Assists",
    "Attempts On Target",
    "Attempts At Goal",
    "Attempts At Goal Conv. Rate (%)",
    "Attempts Inside the Penalty Area",
    "Attempts Outside the Penalty Area",
    "Headed Attempts at Goal",
    "xG",
    "xG Efficiency",
    "Corners"
]

# ============================================================
# Standardize Features
# ============================================================

scaler = StandardScaler()

X = scaler.fit_transform(df[ATTACKING])

# ============================================================
# PCA
# ============================================================

pca = PCA()

X_pca = pca.fit_transform(X)

# ============================================================
# Store Principal Components
# ============================================================

df["PC1"] = X_pca[:, 0]
df["PC2"] = X_pca[:, 1]

# ------------------------------------------------------------
# Flip PC1 if necessary
# (Higher score should represent stronger attackers)
# ------------------------------------------------------------

top_goals = df.nlargest(10, "Goals")["PC1"].mean()
bottom_goals = df.nsmallest(10, "Goals")["PC1"].mean()

if top_goals < bottom_goals:
    df["PC1"] *= -1
    pca.components_[0] *= -1

# ============================================================
# Explained Variance
# ============================================================

print("=" * 60)
print("Explained Variance")
print("=" * 60)

explained = pd.DataFrame({
    "Principal Component":
        [f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))],

    "Variance Explained":
        pca.explained_variance_ratio_,

    "Cumulative Variance":
        pca.explained_variance_ratio_.cumsum()
})

print(explained)

# ============================================================
# Feature Loadings
# ============================================================

print("\n")

print("=" * 60)
print("Feature Loadings")
print("=" * 60)

loadings = pd.DataFrame(
    pca.components_.T,
    columns=[f"PC{i+1}" for i in range(len(ATTACKING))],
    index=ATTACKING
)

print(loadings)

# ============================================================
# Top Players by PC1
# ============================================================

print("\n")

print("=" * 60)
print("Top 20 Attacking Players")
print("=" * 60)

top_attack = (
    df.sort_values(
        "PC1",
        ascending=False
    )[
        [
            "Player",
            "Country",
            "Position",
            "Goals",
            "PC1"
        ]
    ]
    .head(20)
)

print(top_attack)

# ============================================================
# Scree Plot
# ============================================================

plt.figure(figsize=(10,5))

plt.plot(
    range(1, len(pca.explained_variance_ratio_) + 1),
    pca.explained_variance_ratio_,
    marker="o",
    linewidth=2
)

plt.title("Attacking PCA Scree Plot")

plt.xlabel("Principal Component")

plt.ylabel("Explained Variance")

plt.grid(True)

plt.tight_layout()

plt.show()

# ============================================================
# PCA Scatter Plot
# ============================================================

plt.figure(figsize=(10,8))

plt.scatter(
    df["PC1"],
    df["PC2"],
    alpha=0.30
)

plt.xlabel("PC1")

plt.ylabel("PC2")

plt.title("Players in Attacking PCA Space")

plt.grid(True)

plt.tight_layout()

plt.show()

# ============================================================
# Top 20 Players in PCA Space
# ============================================================

top20 = (
    df.sort_values(
        "PC1",
        ascending=False
    )
    .head(20)
)

plt.figure(figsize=(12,10))

plt.scatter(
    df["PC1"],
    df["PC2"],
    alpha=0.15
)

plt.scatter(
    top20["PC1"],
    top20["PC2"],
    s=70
)

for _, row in top20.iterrows():
    plt.text(
        row["PC1"],
        row["PC2"],
        row["Player"],
        fontsize=8
    )

plt.xlabel("PC1")

plt.ylabel("PC2")

plt.title("Top 20 Attackers in PCA Space")

plt.grid(True)

plt.tight_layout()

plt.show()

# ============================================================
# PCA Loading Heatmap
# ============================================================

plt.figure(figsize=(8,6))

plt.imshow(
    loadings.iloc[:, :5],
    aspect="auto"
)

plt.colorbar(label="Loading")

plt.xticks(
    range(5),
    loadings.columns[:5]
)

plt.yticks(
    range(len(loadings.index)),
    loadings.index
)

plt.title("Feature Loadings (First Five Principal Components)")

plt.tight_layout()

plt.show()

# ============================================================
# Save Results
# ============================================================

df.to_csv(
    "data/processed/pca_attack_dataset.csv",
    index=False
)

print("\nSaved: data/processed/pca_attack_dataset.csv")