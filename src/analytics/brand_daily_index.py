import pandas as pd
import os


def run_brand_daily_index():

    print("Calculating Brand-Level Daily Metrics...")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    input_path = os.path.join(BASE_DIR, "data", "processed", "news_master_dataset.csv")
    output_path = os.path.join(BASE_DIR, "data", "processed", "brand_daily_metrics.csv")

    df = pd.read_csv(input_path)

    df["Published_Date"] = pd.to_datetime(df["Published_Date"])
    df["date"] = df["Published_Date"].dt.date

    sentiment_mapping = {
        "positive": 1,
        "neutral": 0,
        "negative": -1
    }

    df["sentiment_score"] = df["finbert_label"].map(sentiment_mapping)

    # -----------------------------
    # 1️⃣ Sentiment Index
    # -----------------------------
    sentiment_index = (
        df.groupby(["date", "Brand"])["sentiment_score"]
        .mean()
        .reset_index(name="sentiment_index")
    )

    # -----------------------------
    # 2️⃣ Topic Counts
    # -----------------------------
    topic_counts = (
        df.groupby(["date", "Brand", "topic"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # -----------------------------
    # 3️⃣ Merge Sentiment + Topics
    # -----------------------------
    brand_metrics = pd.merge(
        sentiment_index,
        topic_counts,
        on=["date", "Brand"],
        how="left"
    )

    brand_metrics.to_csv(output_path, index=False)

    print("Brand Daily Metrics saved.")

    return output_path


if __name__ == "__main__":
    run_brand_daily_index()