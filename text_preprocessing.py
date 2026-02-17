import pandas as pd
import os
import re
from nltk.corpus import stopwords


# Load stopwords
stop_words = set(stopwords.words("english"))


def clean_text(text):
    """
    Clean text by:
    - Lowercasing
    - Removing URLs
    - Removing special characters
    - Removing stopwords
    """

    if pd.isna(text):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()
    words = [word for word in words if word not in stop_words]

    return " ".join(words)


def preprocess_news_data():
    """
    Process raw news data and save cleaned dataset.
    """

    # Get project root directory
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )

    raw_path = os.path.join(
        project_root,
        "data",
        "raw",
        "news_data.csv"
    )

    processed_path = os.path.join(
        project_root,
        "data",
        "processed"
    )

    os.makedirs(processed_path, exist_ok=True)

    # Load raw dataset
    df = pd.read_csv(raw_path)

    # Combine title and description
    df["combined_text"] = df["title"].fillna("") + " " + df["description"].fillna("")

    # Clean text
    df["cleaned_text"] = df["combined_text"].apply(clean_text)

    # Remove empty rows
    df = df[df["cleaned_text"].str.strip() != ""]

    # Select required columns
    df_final = df[
        ["brand",
         "source",
         "published_at",
         "combined_text",
         "cleaned_text"]
    ]

    # Rename columns for clarity
    df_final.columns = [
        "Brand",
        "Source",
        "Published_Date",
        "Combined_Text",
        "Cleaned_Text"
    ]

    # Save processed file
    save_path = os.path.join(
        processed_path,
        "cleaned_news.csv"
    )

    df_final.to_csv(save_path, index=False)

    print("\nCleaned data saved successfully!")
    print(f"Location: {save_path}")
    print("\nSample Preview:\n")
    print(df_final.head())


if __name__ == "__main__":
    print("\nStarting preprocessing...\n")
    preprocess_news_data()
    print("\nPreprocessing completed successfully.\n")




