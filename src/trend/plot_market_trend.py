import pandas as pd
import matplotlib.pyplot as plt
import os

print("Plotting Market Sentiment Trend...")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

input_path = os.path.join(BASE_DIR, "data", "processed", "daily_sentiment_index.csv")

df = pd.read_csv(input_path)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# ---- Plot 1: Raw Trend ----
plt.figure()
plt.plot(df["date"], df["sentiment_score"])
plt.xlabel("Date")
plt.ylabel("Sentiment Score")
plt.title("Raw Ecommerce Market Sentiment Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---- Plot 2: 7-Day Moving Average ----
df["ma_7"] = df["sentiment_score"].rolling(window=7, min_periods=1).mean()

plt.figure()
plt.plot(df["date"], df["ma_7"])
plt.xlabel("Date")
plt.ylabel("7-Day Moving Average Sentiment")
plt.title("Smoothed Ecommerce Market Sentiment Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()