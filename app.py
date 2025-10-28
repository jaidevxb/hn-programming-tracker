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
    if "language" not in df.columns:
        df["language"] = None
    if "sentiment" not in df.columns:
        df["sentiment"] = None
    return df

df = load_data()

st.title("🧠 Hacker News — Programming Post Tracker")
st.markdown("Fetches recent HN posts and classifies titles by programming language **and sentiment**.")

if df.empty:
    st.warning("No data found. Run `fetch_hn.py` first to populate `data/hn_data.csv`.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
min_date = df["created_at"].min().date()
max_date = df["created_at"].max().date()
date_range = st.sidebar.date_input("Date range", [min_date, max_date])
if len(date_range) != 2:
    date_range = [min_date, max_date]

start_dt = pd.to_datetime(date_range[0]).tz_localize("UTC")
end_dt = (pd.to_datetime(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)).tz_localize("UTC")

filtered = df[(df["created_at"] >= start_dt) & (df["created_at"] <= end_dt)]

languages = sorted(filtered["language"].dropna().unique())
selected_langs = st.sidebar.multiselect("Languages", options=languages, default=languages)
if selected_langs:
    filtered = filtered[filtered["language"].isin(selected_langs)]

# Sentiment filter
sentiments = ["positive", "neutral", "negative"]
selected_sents = st.sidebar.multiselect("Sentiment", options=sentiments, default=sentiments)
filtered = filtered[filtered["sentiment"].isin(selected_sents)]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total posts", len(filtered))
col2.metric("Programming-labeled posts", filtered["language"].notna().sum())
col3.metric("Unique languages", filtered["language"].nunique())

# Top languages bar
st.subheader("Top Languages")
lang_counts = filtered["language"].value_counts().reset_index()
lang_counts.columns = ["language", "count"]
if not lang_counts.empty:
    fig1 = px.bar(lang_counts, x="language", y="count", text="count")
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No language-labeled posts in selection.")

# Sentiment pie
st.subheader("Sentiment Distribution")
sent_counts = filtered["sentiment"].value_counts().reset_index()
sent_counts.columns = ["sentiment", "count"]
if not sent_counts.empty:
    fig2 = px.pie(sent_counts, names="sentiment", values="count", title="Post Sentiment Distribution")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No sentiment data to display.")

# Time series
st.subheader("Programming Posts Over Time")
ts = filtered.copy()
ts["date"] = pd.to_datetime(ts["created_at"]).dt.date
ts_counts = ts[ts["language"].notna()].groupby("date").size().reset_index(name="count")
if not ts_counts.empty:
    fig3 = px.line(ts_counts, x="date", y="count", markers=True)
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No posts to plot over time.")

# Table
st.subheader("Posts Table")
show_cols = ["created_at", "title", "language", "sentiment", "author", "points", "num_comments", "url"]
st.dataframe(filtered[show_cols].sort_values("created_at", ascending=False).reset_index(drop=True), height=400)

# Download
@st.cache_data
def convert_df(df_in):
    return df_in.to_csv(index=False).encode("utf-8")

csv_bytes = convert_df(filtered[show_cols])
st.download_button("Download Filtered CSV", csv_bytes, file_name="hn_filtered.csv", mime="text/csv")

st.markdown("---")
st.markdown(f"🕒 Last updated: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC**")

st.markdown(
    """
    <div style='text-align: center; font-size: 15px; margin-top: 20px;'>
        Built with ❤️ by <a href='https://www.linkedin.com/in/jaidevb/' target='_blank'>Jaidev B</a>
    </div>
    """,
    unsafe_allow_html=True
)
