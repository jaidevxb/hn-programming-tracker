# 🚀 Hacker News Programming Tracker

Track the most recent programming-related posts from [Hacker News](https://news.ycombinator.com/) using **Python**, **Streamlit**, and a scheduled **GitHub Action**.

🔗 **Live App:** [https://hn-programming-tracker.streamlit.app/](https://hn-programming-tracker.streamlit.app/)

---

## 📘 Overview

This project automatically fetches the latest Hacker News stories tagged with `story` from the **Algolia API** and displays the programming-related ones on a **Streamlit dashboard**.

Every day, the dataset refreshes automatically via **GitHub Actions**, so the Streamlit app always shows the latest programming and tech discussions.

---

## 🧠 Features

* Fetches the **latest 1000 Hacker News stories** daily.
* Classifies whether each post is **programming-related** using keyword & semantic matching.
* Performs **sentiment analysis** on each title using **TextBlob**.
* Interactive Streamlit dashboard with:

  * Search bar to find posts by keyword
  * Bar chart showing post counts by date
  * Sentiment breakdown visualization
  * Links to the original Hacker News articles
* **Daily automatic data refresh** using GitHub Actions.

---

## 🛠️ Tech Stack

| Component      | Technology                                            |
| -------------- | ----------------------------------------------------- |
| Data Source    | [Hacker News Algolia API](https://hn.algolia.com/api) |
| Backend Script | Python (`requests`, `pandas`, `sqlite3`, `textblob`)  |
| Dashboard      | [Streamlit](https://streamlit.io/)                    |
| Automation     | [GitHub Actions](https://github.com/features/actions) |

---

## 🗂️ Project Structure

```
HN-Programming-Tracker/
│
├── data/
│   ├── hn_data.csv        # Latest fetched stories
│   └── hn_data.sqlite     # SQLite database for backup
│
├── fetch_hn.py            # Fetches data + sentiment analysis
├── app.py                 # Streamlit dashboard
├── requirements.txt       # Python dependencies
├── .gitignore             # Ignore unnecessary files (like data/)
└── .github/workflows/
    └── fetch_daily.yml    # GitHub Action for daily auto-fetch
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/jaidevxb/hn-programming-tracker.git
cd hn-programming-tracker
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Fetch Script (Optional Manual Update)

```bash
python fetch_hn.py
```

This creates/updates `data/hn_data.csv` and `data/hn_data.sqlite`.

### 4️⃣ Run Streamlit Locally

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal.

---

## 🤖 Automated Daily Fetch

The file `.github/workflows/fetch_daily.yml` is configured to:

* Run every day at **04:00 UTC (9:30 AM IST)**.
* Execute `fetch_hn.py` to fetch & analyze the latest posts.
* Commit and push updated data automatically.

You can view the workflow in **GitHub → Actions tab**.

---

## 🌐 Deployment

This project is hosted on **Streamlit Cloud**. Streamlit automatically redeploys the app whenever new commits are pushed to the main branch.

---

## 👨‍💻 Author

**Jaidev B**
Aspiring Data Scientist | Electrical & Electronics Engineering
[LinkedIn Profile](https://www.linkedin.com/in/jaidevxb/)

---

## 💡 Future Enhancements

* Add topic/language filters (Python, AI, Web Dev, etc.)
* Compare daily sentiment trends in programming discussions.
* Highlight top-voted posts per language.
* Integrate Transformer-based sentiment model for higher accuracy.

---

## 🟪 License

This project is open source under the [MIT License](LICENSE).

---

⭐ **If you like this project, give it a star on GitHub!**
