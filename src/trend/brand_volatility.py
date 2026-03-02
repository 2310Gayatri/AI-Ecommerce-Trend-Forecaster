import pandas as pd
import os

print("Calculating Brand Volatility...")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

input_path = os.path.join(BASE_DIR, "data", "processed", "brand_daily_sentiment_index.csv")

df = pd.read_csv(input_path)

results = []

for brand in df["Brand"].unique():
    brand_df = df[df["Brand"] == brand]

    if len(brand_df) < 2:
        continue

    volatility = brand_df["sentiment_score"].std()

    results.append({
        "brand": brand,
        "volatility": volatility
    })

vol_df = pd.DataFrame(results)
vol_df = vol_df.sort_values("volatility", ascending=False)

print("\nBrand Volatility Ranking:")
print(vol_df)