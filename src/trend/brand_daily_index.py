import pandas as pd
import os


def run_brand_daily_index():

    print("Calculating Brand-Level Daily Sentiment Index...")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    input_path = os.path.join(BASE_DIR, "data", "processed", "finbert_output.csv")
    output_path = os.path.join(BASE_DIR, "data", "processed", "brand_daily_sentiment_index.csv")

    df = pd.read_csv(input_path)

    df["Published_Date"] = pd.to_datetime(df["Published_Date"])
    df["date"] = df["Published_Date"].dt.date

    mapping = {
        "positive": 1,
        "neutral": 0,
        "negative": -1
    }

    df["sentiment_score"] = df["finbert_label"].map(mapping)

    brand_daily_index = (
        df.groupby(["date", "Brand"])["sentiment_score"]
        .mean()
        .reset_index()
    )

    brand_daily_index.to_csv(output_path, index=False)

    print("Brand-Level Daily Sentiment Index saved.")

    return output_path


if __name__ == "__main__":
    run_brand_daily_index()