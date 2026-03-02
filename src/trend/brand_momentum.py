import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import numpy as np

print("Calculating Brand Momentum...")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

input_path = os.path.join(BASE_DIR, "data", "processed", "brand_daily_sentiment_index.csv")

df = pd.read_csv(input_path)

results = []

for brand in df["Brand"].unique():
    brand_df = df[df["Brand"] == brand].copy()
    brand_df = brand_df.sort_values("date")

    if len(brand_df) < 2:
        continue  # Not enough data to compute slope

    brand_df["time_index"] = range(len(brand_df))

    X = brand_df[["time_index"]]
    y = brand_df["sentiment_score"]

    model = LinearRegression()
    model.fit(X, y)

    slope = model.coef_[0]

    results.append({
        "brand": brand,
        "slope": slope
    })

momentum_df = pd.DataFrame(results)

momentum_df = momentum_df.sort_values("slope", ascending=False)

print("\nBrand Momentum Ranking:")
print(momentum_df)