import pandas as pd
from textblob import TextBlob
import os
import json

print("Starting TextBlob analysis...")

# Project root path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# File paths
input_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_news.csv")
output_path = os.path.join(BASE_DIR, "data", "processed", "textblob_output.csv")
summary_path = os.path.join(BASE_DIR, "data", "processed", "textblob_summary.json")

# Load dataset
df = pd.read_csv(input_path)

scores = []
labels = []

for text in df["Cleaned_Text"]:
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity

    scores.append(polarity)

    if polarity > 0:
        labels.append("Positive")
    elif polarity < 0:
        labels.append("Negative")
    else:
        labels.append("Neutral")

# Add new columns
df["textblob_score"] = scores
df["textblob_label"] = labels

# Save output
df.to_csv(output_path, index=False)

# Create summary
summary = {
    "total_articles": len(df),
    "average_score": float(df["textblob_score"].mean()),
    "positive_count": labels.count("Positive"),
    "negative_count": labels.count("Negative"),
    "neutral_count": labels.count("Neutral")
}

with open(summary_path, "w") as f:
    json.dump(summary, f, indent=4)

print("TextBlob analysis complete.")