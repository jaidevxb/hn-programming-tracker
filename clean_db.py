# clean_sqlite.py
import sqlite3
import pandas as pd
import os
import sys

DB_PATH = "data/hn_data.sqlite"
TABLE_NAME = "posts"

if not os.path.exists(DB_PATH):
    print(f"DB not found at {DB_PATH}")
    sys.exit(1)

conn = sqlite3.connect(DB_PATH)

# check table exists
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (TABLE_NAME,))
if cur.fetchone() is None:
    print(f"Table '{TABLE_NAME}' not found in {DB_PATH}. Available tables:")
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print([r[0] for r in cur.fetchall()])
    conn.close()
    sys.exit(1)

# Read table
df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME};", conn)

if df.empty:
    print("Table is empty — nothing to clean.")
    conn.close()
    sys.exit(0)

# Ensure objectID is string
if "objectID" in df.columns:
    df["objectID"] = df["objectID"].astype(str)
else:
    print("No 'objectID' column found — can't deduplicate. Exiting.")
    conn.close()
    sys.exit(1)

# Parse created_at to datetime if present
if "created_at" in df.columns:
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
else:
    print("No 'created_at' column found — rows will not be sorted by date.")

# Drop duplicates (keep the last, i.e. newest)
df = df.drop_duplicates(subset=["objectID"], keep="last")

# Sort by created_at if available, else by objectID
if "created_at" in df.columns:
    df = df.sort_values(by="created_at", ascending=True)
else:
    df = df.sort_values(by="objectID", ascending=True)

# Write cleaned table back (replace)
df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

print(f"SQL table cleaned — total {len(df)} unique posts written to '{TABLE_NAME}' in {DB_PATH}")

conn.close()
