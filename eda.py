import pandas as pd

# Load dataset
df = pd.read_csv("data/processed/master_dataset.csv")

print("=" * 60)
print("Dataset Shape")
print("=" * 60)
print(df.shape)

print("\n" + "=" * 60)
print("Columns")
print("=" * 60)
print(df.columns.tolist())

print("\n" + "=" * 60)
print("Data Types")
print("=" * 60)
print(df.dtypes)

print("\n" + "=" * 60)
print("Missing Values")
print("=" * 60)
print(df.isnull().sum())

print("\n" + "=" * 60)
print("Duplicate Players")
print("=" * 60)
print(df.duplicated(subset=["Player", "Country", "Position"]).sum())

print("\n" + "=" * 60)
print("First Five Rows")
print("=" * 60)
print(df.head())