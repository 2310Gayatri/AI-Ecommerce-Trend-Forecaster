from src.ingestion.news_ingestion import fetch_news_for_brands, save_news_to_csv
from src.preprocessing.text_preprocessing import preprocess_news_data
from src.sentiment.finbert_analyzer import run_finbert
from src.trend.daily_sentiment_index import run_daily_sentiment_index
from src.trend.brand_daily_index import run_brand_daily_index
from src.forecasting.market_forecast import (
    forecast_market_sentiment,
    forecast_brand_sentiment,
)
from src.intelligence.market_intelligence import run_market_intelligence
from src.intelligence.event_signal_engine import run_event_signals
from src.narrative.explainability_engine import run_explainability_engine
from src.topic_modeling.topic_extractor_llm import run_topic_extraction
from src.utils.build_master_dataset import build_master_dataset
from src.intelligence.topic_sentiment_matrix import run_topic_sentiment_matrix
from src.intelligence.topic_momentum_tracker import run_topic_momentum_tracker
from src.intelligence.narrative_intelligence import run_narrative_intelligence
from src.narrative.narrative_summary import generate_market_report
import json
from datetime import datetime
import os


def main():

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # 1️⃣ Ingestion
    print("Running ingestion...")
    brands = [
        "Flipkart",
        "Amazon India",
        "Myntra",
        "Snapdeal",
        "Meesho",
        "Ajio",
        "BigBasket",
        "Nykaa",
        "Reliance Digital",
        "Tata Cliq"
    ]

    news_data = fetch_news_for_brands(brands)
    save_news_to_csv(news_data)

    # 2️⃣ Preprocessing
    print("Running preprocessing...")
    preprocess_news_data()

    # 3️⃣ Sentiment Analysis
    print("Running FinBERT sentiment analysis...")
    run_finbert()

    # 4️⃣ Topic Modeling (Milestone 2)
    print("Running topic extraction...")
    run_topic_extraction()

    print("Building master dataset...")
    build_master_dataset()

    # 5️⃣ Trend Indexes
    print("Generating daily sentiment index...")
    run_daily_sentiment_index()

    print("Generating brand daily sentiment index...")
    run_brand_daily_index()

    # 6️⃣ Intelligence
    print("Running market intelligence...")
    market_output, market_summary = run_market_intelligence()

    print("Running event signal engine...")
    event_output, event_summary = run_event_signals()

    print("Running topic sentiment matrix...")
    topic_matrix = run_topic_sentiment_matrix()

    print("Running topic momentum tracker...")
    topic_momentum = run_topic_momentum_tracker()

    print("Running narrative intelligence...")
    narrative_output = run_narrative_intelligence()

    # 7️⃣ Forecast Engine
    print("Running market forecast...")
    market_forecast = forecast_market_sentiment(BASE_DIR)

    print("Running brand forecast...")
    brand_forecast = forecast_brand_sentiment(BASE_DIR)

    # 8️⃣ Explainability Engine
    print("Running explainability engine...")
    explainability_output = run_explainability_engine(BASE_DIR)

    # 9️⃣ Final Output
    final_output = {
        "timestamp": str(datetime.now()),
        "market_signals": market_output,
        "event_signals": event_output,
        "topic_sentiment_matrix": topic_matrix,
        "topic_momentum": topic_momentum,
        "narrative_intelligence": narrative_output,
        "forecast_signals": {
            "market_forecast": market_forecast,
            "brand_forecast": brand_forecast
        },
        "explainability": explainability_output
    }

    output_path = os.path.join(BASE_DIR, "data/processed/final_market_signal.json")

    with open(output_path, "w") as f:
        json.dump(final_output, f, indent=4)

    print("Final market signal saved.")

    print("Generating AI market report...")
    generate_market_report(BASE_DIR)

if __name__ == "__main__":
    main()