import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import numpy as np
import json
def run_market_intelligence():
    print("Running Market Intelligence Engine...")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    daily_path = os.path.join(BASE_DIR, "data", "processed", "daily_sentiment_index.csv")
    brand_path = os.path.join(BASE_DIR, "data", "processed", "brand_daily_sentiment_index.csv")

    # -------------------------
    # 1️⃣ Overall Market Trend
    # -------------------------

    daily_df = pd.read_csv(daily_path)
    daily_df = daily_df.sort_values("date")
    daily_df["time_index"] = range(len(daily_df))

    X = daily_df[["time_index"]]
    y = daily_df["sentiment_score"]

    model = LinearRegression()
    model.fit(X, y)

    market_slope = model.coef_[0]
    current_sentiment = daily_df["sentiment_score"].iloc[-1]

    if market_slope > 0:
        market_direction = "Bullish"
    elif market_slope < 0:
        market_direction = "Bearish"
    else:
        market_direction = "Stable"

    # -------------------------
    # 2️⃣ Brand Momentum
    # -------------------------

    brand_df = pd.read_csv(brand_path)

    momentum_results = []

    for brand in brand_df["Brand"].unique():
        temp = brand_df[brand_df["Brand"] == brand].sort_values("date")

        if len(temp) < 2:
            continue

        temp["time_index"] = range(len(temp))
        Xb = temp[["time_index"]]
        yb = temp["sentiment_score"]

        model = LinearRegression()
        model.fit(Xb, yb)

        slope = model.coef_[0]

        momentum_results.append((brand, slope))

    momentum_results = sorted(momentum_results, key=lambda x: x[1], reverse=True)

    top_positive_brand = momentum_results[0][0]
    top_negative_brand = momentum_results[-1][0]

    # -------------------------
    # 3️⃣ Brand Volatility
    # -------------------------

    volatility_results = []

    for brand in brand_df["Brand"].unique():
        temp = brand_df[brand_df["Brand"] == brand]

        if len(temp) < 2:
            continue

        volatility = temp["sentiment_score"].std()
        volatility_results.append((brand, volatility))

    volatility_results = sorted(volatility_results, key=lambda x: x[1], reverse=True)

    most_volatile_brand = volatility_results[0][0]

    # -------------------------
    # 4️⃣ Generate Insight
    # -------------------------

    summary = f"""
    Overall ecommerce market sentiment is currently {market_direction.lower()} 
    with a slope of {round(market_slope, 4)}.
    
    Current sentiment score stands at {round(current_sentiment, 3)}.
    
    Brand momentum analysis shows {top_positive_brand} gaining the strongest positive sentiment momentum, 
    while {top_negative_brand} is experiencing the sharpest decline.
    
    Sentiment volatility is highest for {most_volatile_brand}, 
    indicating increased uncertainty or news-driven fluctuations.
    """

    # -------------------------
    # 5️⃣ JSON Output
    # -------------------------

    output = {
        "market_direction": market_direction,
        "market_slope": round(float(market_slope), 6),
        "current_sentiment": round(float(current_sentiment), 6),
        "top_positive_brand": top_positive_brand,
        "top_negative_brand": top_negative_brand,
        "most_volatile_brand": most_volatile_brand
    }

    print("\n--- Human Readable Insight ---")
    print(summary)

    print("\n--- JSON Output ---")
    print(json.dumps(output, indent=4))

    return output, summary

if __name__ == "__main__":
    output, summary = run_market_intelligence()
    print(summary)
    print(output)