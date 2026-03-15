import pandas as pd
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
)

from src.utils.data_loader import load_master_dataset


def run_topic_sentiment_matrix():

    print("Running Topic Sentiment Matrix...")

    df = load_master_dataset()

    if df.empty:
        return {"error": "Master dataset empty"}

    # -----------------------------
    # Map sentiment to numeric
    # -----------------------------

    mapping = {
        "positive": 1,
        "neutral": 0,
        "negative": -1
    }

    df["sentiment_score"] = df["finbert_label"].map(mapping)

    # -----------------------------
    # Compute topic sentiment
    # -----------------------------

    topic_sentiment = (
        df.groupby("topic")["sentiment_score"]
        .mean()
        .sort_values(ascending=False)
    )

    topic_counts = df["topic"].value_counts()

    matrix = []

    for topic in topic_sentiment.index:

        matrix.append({
            "topic": topic,
            "article_volume": int(topic_counts[topic]),
            "avg_sentiment": round(float(topic_sentiment[topic]), 3)
        })

    result = {
        "topic_sentiment_matrix": matrix
    }

    print("\n--- Topic Sentiment Matrix ---")

    for row in matrix:
        print(
            f"{row['topic']:20} | "
            f"Volume: {row['article_volume']:3} | "
            f"Avg Sentiment: {row['avg_sentiment']}"
        )

    return result


if __name__ == "__main__":
    run_topic_sentiment_matrix()