import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv("data/processed/cleaned_dataset.csv")

print("=" * 60)
print("Football Feature Engineering")
print("=" * 60)

# ==========================================================
# Football Categories
# ==========================================================

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

PASSING = [
    "Passes",
    "Passes Completed",
    "Passing Accuracy (%)",
    "Crosses",
    "Crossing Accuracy (%)",
    "Take-Ons Completed",
    "Defensive Linebreaks Attempted",
    "Defensive Linebreaks Acc (%)",
    "Switches of Play Attempted",
    "Switches of Play Acc (%)"
]

DEFENDING = [
    "Forced Turnovers",
    "Defensive Pressures Applied",
    "Defensive Pressures Directly Applied",
    "Fouls For"
]

MOVEMENT = [
    "Offers To Receive",
    "Offers In Behind",
    "Offers In Between",
    "Offers In Front",
    "Offers Inside Team Shape",
    "Offers Outside Team Shape",
    "Receptions In Behind",
    "Receptions Between Midfield And Defensive Line",
    "Receptions Under Pressure",
    "Player Involvements",
    "Average Speed (km/h)",
    "High Speed Running",
    "Sprints",
    "Total Distance (m)"
]

GOALKEEPING = [
    "Goalkeeper Saves",
    "Goalkeeper Actions Inside the Penalty Area",
    "Goalkeeper Actions Outside the Penalty Area"
]

# ==========================================================
# Generic PCA Function
# ==========================================================

def create_pca_score(df, columns, score_name):

    X = df[columns].fillna(0)

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    pca = PCA()

    X_pca = pca.fit_transform(X_scaled)

    score = X_pca[:, 0]

    # -------------------------------------------------
# Flip sign so higher score always means better
# -------------------------------------------------

    temp = df.copy()
    temp["_score"] = score

    best_mean = temp.nlargest(10, columns[0])["_score"].mean()
    worst_mean = temp.nsmallest(10, columns[0])["_score"].mean()

    if best_mean < worst_mean:
        score *= -1
        pca.components_[0] *= -1

    print("\n")
    print("=" * 60)
    print(score_name)
    print("=" * 60)

    print(
        f"PC1 Explained Variance : "
        f"{pca.explained_variance_ratio_[0]*100:.2f}%"
    )

    loadings = pd.DataFrame({
        "Feature": columns,
        "Weight": pca.components_[0]
    })

    print(loadings.sort_values(
        "Weight",
        ascending=False
    ))

    return score

# ==========================================================
# Generate Scores
# ==========================================================

df["Attacking Impact Score"] = create_pca_score(
    df,
    ATTACKING,
    "Attacking"
)

df["Passing Impact Score"] = create_pca_score(
    df,
    PASSING,
    "Passing"
)

df["Defensive Impact Score"] = create_pca_score(
    df,
    DEFENDING,
    "Defending"
)

df["Movement Impact Score"] = create_pca_score(
    df,
    MOVEMENT,
    "Movement"
)

# Goalkeepers only

gk = df["Position"] == "GK"

gk_scores = create_pca_score(
    df[gk].copy(),
    GOALKEEPING,
    "Goalkeeping"
)

df["Goalkeeping Impact Score"] = pd.NA

df.loc[gk, "Goalkeeping Impact Score"] = gk_scores

# ==========================================================
# Save Dataset
# ==========================================================

df.to_csv(
    "data/processed/engineered_dataset.csv",
    index=False
)

print("\n")
print("=" * 60)
print("Feature Engineering Complete")
print("=" * 60)

print(df[[
    "Player",
    "Attacking Impact Score",
    "Passing Impact Score",
    "Defensive Impact Score",
    "Movement Impact Score",
    "Goalkeeping Impact Score"
]].head())