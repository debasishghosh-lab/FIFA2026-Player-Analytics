from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")

files = [
    "adidas_golden_boot.csv",
    "attacking.csv",
    "distribution.csv",
    "defending.csv",
    "discipline.csv",
    "goalkeeping.csv",
    "movement.csv",
    "physical.csv"
]

master = None

for file in files:

    print(f"Loading {file}")

    df = pd.read_csv(DATA_DIR / file)

    # Remove Rank because every CSV has its own ranking
    if "Rank" in df.columns:
        df = df.drop(columns=["Rank"])

    if master is None:
        master = df
    else:
        master = master.merge(
            df,
            on=["Player", "Country", "Position"],
            how="outer"
        )

print("\nFinal Shape:", master.shape)

master.to_csv(
    DATA_DIR / "master_dataset.csv",
    index=False
)

print("master_dataset.csv created successfully!")