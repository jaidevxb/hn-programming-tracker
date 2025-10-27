# fetch_hn.py
import requests
import pandas as pd
import sqlite3
from datetime import datetime, timezone
from dateutil import parser
import os
import re
import time

API_URL = "https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=100"
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "hn_data.csv")
DB_PATH = os.path.join(DATA_DIR, "hn_data.sqlite")

# languages list and common aliases (lowercase)
LANG_KEYWORDS = {
    "python": ["python"],
    "javascript": ["javascript", "js", "node", "nodejs"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],
    "c": [r"\bc\b"],  # regex for single-letter c as whole word
    "go": ["golang", "go "],
    "rust": ["rust"],
    "typescript": ["typescript", "ts "],
    "ruby": ["ruby"],
    "php": ["php"],
    "swift": ["swift"],
    "kotlin": ["kotlin"],
    "scala": ["scala"],
    "r": [r"\br\b"],
    "dart": ["dart"],
    "haskell": ["haskell"],
    "perl": ["perl"],
    "shell": ["bash", "shell", "sh", "zsh"],
    "sql": ["sql"],
}

def normalize_title(t):
    return t.strip()

def classify_title(title):
    t = title.lower()
    for lang, tokens in LANG_KEYWORDS.items():
        for token in tokens:
            if token.startswith("\\b") or token.endswith(" "):
                if re.search(token, t):
                    return lang
            else:
                if token in t:
                    return lang
    return None

def fetch_hn():
    """Fetch multiple pages (~1000 recent posts)"""
    all_hits = []
    for page in range(10):  # fetch ~2000 posts
        url = f"{API_URL}&page={page}"
        res = requests.get(url, timeout=15)
        res.raise_for_status()
        hits = res.json().get("hits", [])
        if not hits:
            break
        all_hits.extend(hits)
        time.sleep(1)
    return all_hits

def hits_to_df(hits):
    rows = []
    for h in hits:
        title = h.get("title") or h.get("story_title") or ""
        title = normalize_title(title)
        if not title:
            continue
        created_at = h.get("created_at")
        try:
            created_ts = parser.isoparse(created_at) if created_at else datetime.now(timezone.utc)
        except Exception:
            created_ts = datetime.now(timezone.utc)
        row = {
            "objectID": h.get("objectID"),
            "title": title,
            "url": h.get("url"),
            "author": h.get("author"),
            "points": h.get("points", 0),
            "num_comments": h.get("num_comments", 0),
            "created_at": created_ts.isoformat(),
        }
        row["language"] = classify_title(title)
        rows.append(row)
    df = pd.DataFrame(rows)
    if not df.empty:
        df["points"] = df["points"].astype(int)
        df["num_comments"] = df["num_comments"].astype(int)
        df["created_at"] = pd.to_datetime(df["created_at"])
    return df

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_to_sqlite(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("posts_tmp", conn, if_exists="replace", index=False)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        objectID TEXT PRIMARY KEY,
        title TEXT,
        url TEXT,
        author TEXT,
        points INTEGER,
        num_comments INTEGER,
        created_at TEXT,
        language TEXT
    );
    """)
    cur.execute("""
    INSERT OR REPLACE INTO posts (objectID, title, url, author, points, num_comments, created_at, language)
    SELECT objectID, title, url, author, points, num_comments, created_at, language FROM posts_tmp;
    """)
    conn.commit()
    cur.execute("DROP TABLE IF EXISTS posts_tmp;")
    conn.commit()
    conn.close()

def append_to_csv(df):
    if os.path.exists(CSV_PATH):
        existing = pd.read_csv(CSV_PATH, parse_dates=["created_at"])
        combined = pd.concat([existing, df], ignore_index=True)
        combined = combined.drop_duplicates(subset=["objectID"], keep="last")
        combined.to_csv(CSV_PATH, index=False)
    else:
        df.to_csv(CSV_PATH, index=False)

def main():
    ensure_data_dir()
    hits = fetch_hn()
    df = hits_to_df(hits)
    if df.empty:
        print("No posts fetched.")
        return
    save_to_sqlite(df)
    append_to_csv(df)
    print(f"Fetched {len(df)} posts; saved to {CSV_PATH} and {DB_PATH}")

if __name__ == "__main__":
    main()
