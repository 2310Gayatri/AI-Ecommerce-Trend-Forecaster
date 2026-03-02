from src.ingestion.news_ingestion import fetch_news_for_brands, save_news_to_csv
from src.preprocessing.text_preprocessing import preprocess_news_data
from src.sentiment.finbert_analyzer import run_finbert
from src.trend.daily_sentiment_index import run_daily_sentiment_index
from src.trend.brand_daily_index import run_brand_daily_index
from src.trend.market_forecast import (
    forecast_market_sentiment,
    forecast_brand_sentiment,
)
from src.trend.market_intelligence import run_market_intelligence
from src.trend.event_signal_engine import run_event_signals
import json
from datetime import datetime
import os

def main():

    # 1. Ingestion
    print("Running ingestion...")

    # 2. Preprocessing
    print("Running preprocessing...")

    # 3. Sentiment
    print("Running FinBERT...")

    # 4. Trend
    print("Generating daily index...")

    # 5. Intelligence
    market_output, market_summary = run_market_intelligence()
    event_output, event_summary = run_event_signals()

    # 🔥 ADD THIS BLOCK HERE
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    print("Running market forecast...")
    market_forecast = forecast_market_sentiment(BASE_DIR)

    print("Running brand forecast...")
    brand_forecast = forecast_brand_sentiment(BASE_DIR)

    # 🔥 MODIFY FINAL OUTPUT
    final_output = {
        "timestamp": str(datetime.now()),
        "market_signals": market_output,
        "event_signals": event_output,
        "forecast_signals": {
            "market_forecast": market_forecast,
            "brand_forecast": brand_forecast
        }
    }

    with open("data/processed/final_market_signal.json", "w") as f:
        json.dump(final_output, f, indent=4)

    print("Final market signal saved.")
if __name__ == "__main__":
    main()