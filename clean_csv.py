import pandas as pd

csv_path = "data/hn_data.csv"
df = pd.read_csv(csv_path)

# Drop exact duplicates of objectID
df = df.drop_duplicates(subset=["objectID"], keep="last")

# Sort chronologically
df = df.sort_values(by="created_at")

df.to_csv(csv_path, index=False)
print(f"Cleaned CSV saved — total {len(df)} unique posts.")
