import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def forecast_market_sentiment(base_dir, forecast_days=7):
    input_path = os.path.join(
        base_dir, "data", "processed", "daily_sentiment_index.csv"
    )

    if not os.path.exists(input_path):
        return {"error": "daily_sentiment_index.csv not found"}

    df = pd.read_csv(input_path)

    if df.empty or len(df) < 3:
        return {"error": "Not enough data for market forecasting"}

    df = df.sort_values("date")
    df["time_index"] = range(len(df))

    X = df[["time_index"]]
    y = df["sentiment_score"]

    model = LinearRegression()
    model.fit(X, y)

    slope = model.coef_[0]
    volatility = float(np.std(y))

    future_indices = pd.DataFrame({
        "time_index": range(len(df), len(df) + forecast_days)
    })
    future_predictions = model.predict(future_indices)

    if slope > 0.01:
        trend = "Bullish"
    elif slope < -0.01:
        trend = "Bearish"
    else:
        trend = "Stable"

    data_points = len(df)
    if data_points < 10:
        confidence = "Low"
    elif data_points < 30:
        confidence = "Medium"
    else:
        confidence = "High"

    return {
        "forecast_days": forecast_days,
        "trend_direction": trend,
        "trend_slope": round(float(slope), 4),
        "volatility": round(volatility, 4),
        "confidence": confidence,
        "predicted_values": [
            round(float(val), 4) for val in future_predictions
        ],
    }


def forecast_brand_sentiment(base_dir, forecast_days=7):
    input_path = os.path.join(
        base_dir, "data", "processed", "brand_daily_sentiment_index.csv"
    )

    if not os.path.exists(input_path):
        return {"error": "brand_daily_sentiment_index.csv not found"}

    df = pd.read_csv(input_path)

    if df.empty:
        return {"error": "No brand data available"}

    df = df.sort_values("date")
    brand_forecasts = []

    for brand in df["Brand"].unique():
        brand_df = df[df["Brand"] == brand].copy()
        brand_df = brand_df.sort_values("date")

        if len(brand_df) < 3:
            continue

        brand_df["time_index"] = range(len(brand_df))

        X = brand_df[["time_index"]]
        y = brand_df["sentiment_score"]

        model = LinearRegression()
        model.fit(X, y)

        slope = model.coef_[0]
        volatility = float(np.std(y))

        future_indices = pd.DataFrame({
            "time_index": range(len(df), len(df) + forecast_days)
        })

        future_predictions = model.predict(future_indices)

        if slope > 0.01:
            direction = "Improving"
        elif slope < -0.01:
            direction = "Declining"
        else:
            direction = "Stable"

        if len(brand_df) < 10:
            confidence = "Low"
        elif len(brand_df) < 30:
            confidence = "Medium"
        else:
            confidence = "High"

        brand_forecasts.append({
            "brand": brand,
            "trend_direction": direction,
            "trend_slope": round(float(slope), 4),
            "volatility": round(volatility, 4),
            "confidence": confidence,
            "predicted_values": [
                round(float(val), 4) for val in future_predictions
            ],
        })

    return {
        "forecast_days": forecast_days,
        "brand_forecasts": brand_forecasts
    }