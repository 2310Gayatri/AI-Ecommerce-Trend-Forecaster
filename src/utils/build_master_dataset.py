import pandas as pd
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

def build_master_dataset():

    cleaned_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_news.csv")
    finbert_path = os.path.join(BASE_DIR, "data", "processed", "finbert_output.csv")
    topic_path = os.path.join(BASE_DIR, "data", "processed", "news_with_topics.csv")

    cleaned_df = pd.read_csv(cleaned_path)
    finbert_df = pd.read_csv(finbert_path)
    topic_df = pd.read_csv(topic_path)

    master_df = cleaned_df.copy()

    master_df["finbert_label"] = finbert_df["finbert_label"]
    master_df["finbert_confidence"] = finbert_df["finbert_confidence"]

    master_df["topic"] = topic_df["topic"]
    master_df["topic_confidence"] = topic_df["topic_confidence"]

    output_path = os.path.join(BASE_DIR, "data", "processed", "news_master_dataset.csv")

    master_df.to_csv(output_path, index=False)

    print("Master dataset created")
    print(output_path)