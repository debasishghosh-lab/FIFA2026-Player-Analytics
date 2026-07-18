import pandas as pd

# Load merged dataset
df = pd.read_csv("data/processed/master_dataset.csv")

# 1. Drop duplicate assists column
df = df.drop(columns=["Assists_x"])

# 2. Rename Attacking assists column
df = df.rename(columns={
    "Assists_y": "Assists"
})

# 3. Fill missing goals with 0
df["Goals"] = df["Goals"].fillna(0)

# 4. Convert xG Efficiency to numeric
df["xG Efficiency"] = (
    df["xG Efficiency"]
    .str.replace("x", "", regex=False)
    .astype(float)
)

# Save cleaned dataset
df.to_csv(
    "data/processed/cleaned_dataset.csv",
    index=False
)

print("=" * 60)
print("Cleaning Complete")
print("=" * 60)
print(df.info())
print("\nSaved as cleaned_dataset.csv")