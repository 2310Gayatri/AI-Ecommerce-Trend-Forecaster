import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Download lexicon (only runs first time)
nltk.download('vader_lexicon')

print("Starting VADER analysis...")

# Load dataset
file_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_news.csv")

df = pd.read_csv(file_path)

# Initialize analyzer
sia = SentimentIntensityAnalyzer()

scores = []
labels = []

for text in df["Cleaned_Text"]:
    sentiment = sia.polarity_scores(str(text))
    compound = sentiment["compound"]

    scores.append(compound)

    if compound >= 0.05:
        labels.append("Positive")
    elif compound <= -0.05:
        labels.append("Negative")
    else:
        labels.append("Neutral")

# Add new columns
df["vader_score"] = scores
df["vader_label"] = labels

# Save output CSV
output_path = os.path.join(BASE_DIR, "data", "processed", "vader_output.csv")
df.to_csv(output_path, index=False)

# Create summary
summary = {
    "total_articles": len(df),
    "average_score": float(df["vader_score"].mean()),
    "positive_count": labels.count("Positive"),
    "negative_count": labels.count("Negative"),
    "neutral_count": labels.count("Neutral")
}

# Save summary JSON
summary_path = os.path.join(BASE_DIR, "data", "processed", "vader_summary.json")

with open(summary_path, "w") as f:
    json.dump(summary, f, indent=4)

print("VADER analysis complete.")