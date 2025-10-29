import sqlite3
import pandas as pd

csv_path = "data/hn_data.csv"
db_path = "data/hn_data.sqlite"

df = pd.read_csv(csv_path)
conn = sqlite3.connect(db_path)

df.to_sql("posts", conn, if_exists="replace", index=False)
conn.close()

print(f"Synced SQLite DB from CSV — {len(df)} rows written.")
