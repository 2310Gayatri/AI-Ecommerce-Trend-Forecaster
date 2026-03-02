import pandas as pd
import os


def run_daily_sentiment_index():

    print("Calculating Daily Sentiment Index...")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    input_path = os.path.join(BASE_DIR, "data", "processed", "finbert_output.csv")
    output_path = os.path.join(BASE_DIR, "data", "processed", "daily_sentiment_index.csv")

    df = pd.read_csv(input_path)

    df["Published_Date"] = pd.to_datetime(df["Published_Date"])
    df["date"] = df["Published_Date"].dt.date

    mapping = {
        "positive": 1,
        "neutral": 0,
        "negative": -1
    }

    df["sentiment_score"] = df["finbert_label"].map(mapping)

    daily_index = df.groupby("date")["sentiment_score"].mean().reset_index()

    daily_index.to_csv(output_path, index=False)

    print("Daily Sentiment Index saved.")

    return output_path


if __name__ == "__main__":
    run_daily_sentiment_index()