import pandas as pd
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


def detect_market_drivers(top_n=3):

    file_path = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "news_with_topics.csv"
    )

    df = pd.read_csv(file_path)

    if df.empty:
        return {"drivers": []}

    df["date"] = pd.to_datetime(df["Published_Date"])

    df = df.sort_values("date")

    latest_date = df["date"].max()

    prev_date = df[df["date"] < latest_date]["date"].max()

    if pd.isna(prev_date):
        return {"drivers": []}

    today_df = df[df["date"] == latest_date]
    prev_df = df[df["date"] == prev_date]

    today_counts = today_df["topic_group"].value_counts()
    prev_counts = prev_df["topic_group"].value_counts()

    topics = set(today_counts.index).union(prev_counts.index)

    drivers = []

    for topic in topics:

        today = today_counts.get(topic, 0)
        prev = prev_counts.get(topic, 0)

        change = today - prev

        if prev == 0:
            pct_change = 100
        else:
            pct_change = (change / prev) * 100

        drivers.append({
            "topic_group": topic,
            "change": change,
            "pct_change": round(pct_change, 2)
        })

    drivers = sorted(
        drivers,
        key=lambda x: x["pct_change"],
        reverse=True
    )

    return {
        "drivers": drivers[:top_n]
    }