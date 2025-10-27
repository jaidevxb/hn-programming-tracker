# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os

DATA_CSV = "data/hn_data.csv"

st.set_page_config(page_title="HN Programming Posts", layout="wide")

@st.cache_data(ttl=300)
def load_data():
    if not os.path.exists(DATA_CSV):
        return pd.DataFrame()
    df = pd.read_csv(DATA_CSV, parse_dates=["created_at"])
    # ensure language column exists
    if "language" not in df.columns:
        df["language"] = None
    return df

df = load_data()

st.title("Hacker News — Programming Post Tracker")
st.markdown("Fetches recent HN posts and classifies titles for programming languages (keyword matching).")

if df.empty:
    st.warning("No data found. Run `fetch_hn.py` first to populate `data/hn_data.csv`.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
min_date = df["created_at"].min().date()
max_date = df["created_at"].max().date()
date_range = st.sidebar.date_input("Date range", [min_date, max_date])
if len(date_range) != 2:
    # fallback
    date_range = [min_date, max_date]

# --- Timezone-aware date conversion ---
start_dt = pd.to_datetime(date_range[0]).tz_localize("UTC")
end_dt = (pd.to_datetime(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)).tz_localize("UTC")

# If your dataset timestamps are also in UTC, no conversion needed
filtered = df[(df["created_at"] >= start_dt) & (df["created_at"] <= end_dt)]

languages = sorted(filtered["language"].dropna().unique())
selected_langs = st.sidebar.multiselect("Languages", options=languages, default=languages)
if selected_langs:
    filtered = filtered[filtered["language"].isin(selected_langs)]

# Main KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total posts (filtered)", len(filtered))
col2.metric("Programming-labeled posts", filtered["language"].notna().sum())
col3.metric("Unique languages", filtered["language"].nunique())

# Top languages bar
st.subheader("Top languages (count)")
lang_counts = filtered["language"].value_counts().reset_index()
lang_counts.columns = ["language", "count"]
if not lang_counts.empty:
    fig1 = px.bar(lang_counts, x="language", y="count", text="count", labels={"count": "Posts"})
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No language-labeled posts in selection.")

# Time series: programming posts over time
st.subheader("Programming posts over time")
ts = filtered.copy()
ts["date"] = pd.to_datetime(ts["created_at"]).dt.date
ts_counts = ts[ts["language"].notna()].groupby("date").size().reset_index(name="count")
if not ts_counts.empty:
    fig2 = px.line(ts_counts, x="date", y="count", markers=True)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No programming-labeled posts to plot over time.")

# Table
st.subheader("Posts (table)")
show_cols = ["created_at", "title", "language", "author", "points", "num_comments", "url"]
st.dataframe(
    filtered[show_cols].sort_values("created_at", ascending=False).reset_index(drop=True),
    height=400
)

# Download filtered CSV
@st.cache_data
def convert_df(df_in):
    return df_in.to_csv(index=False).encode("utf-8")

csv_bytes = convert_df(filtered[show_cols])
st.download_button("Download filtered CSV", csv_bytes, file_name="hn_filtered.csv", mime="text/csv")

# At the bottom of your Streamlit layout
st.markdown("---")
st.markdown(
    f"🕒 Last updated: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}** (UTC)"
)

st.markdown(
    """
    <div style='text-align: center; font-size: 15px; margin-top: 20px;'>
        Built with ❤️ by <a href='https://www.linkedin.com/in/jaidevb/' target='_blank'>Jaidev B</a>
    </div>
    """,
    unsafe_allow_html=True
)