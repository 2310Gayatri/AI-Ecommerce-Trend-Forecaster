# src/trend/explainability_engine.py

import os
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords


def run_explainability_engine(base_dir):

    processed_path = os.path.join(
        base_dir, "data", "processed", "finbert_output.csv"
    )

    if not os.path.exists(processed_path):
        return {"error": "Processed news file not found"}

    df = pd.read_csv(processed_path)

    if df.empty:
        return {"error": "No data available for explainability"}

    # -----------------------------
    # Required Columns
    # -----------------------------
    required_cols = ["Brand", "finbert_label", "Combined_Text", "Cleaned_Text"]
    for col in required_cols:
        if col not in df.columns:
            return {"error": f"Missing column: {col}"}

    # -----------------------------
    # Setup
    # -----------------------------
    stop_words = set(stopwords.words("english"))

    complaint_keywords = ["refund", "delay", "fraud", "complaint"]
    competition_keywords = ["sale", "discount", "offer", "cashback"]
    regulatory_keywords = ["ccpa", "fine", "regulation", "compliance"]
    market_keywords = ["ipo", "market", "valuation", "funding", "bearish", "bullish"]
    employment_keywords = ["hiring", "layoff", "jobs"]

    # -----------------------------
    # 1️⃣ Market-Level Drivers
    # -----------------------------
    brand_sentiment = (
        df.groupby("Brand")["finbert_label"]
        .value_counts()
        .unstack()
        .fillna(0)
    )

    negative_drivers = []
    positive_drivers = []

    if "negative" in brand_sentiment.columns:
        negative_drivers = (
            brand_sentiment["negative"]
            .sort_values(ascending=False)
            .head(2)
            .index
            .tolist()
        )

    if "positive" in brand_sentiment.columns:
        positive_drivers = (
            brand_sentiment["positive"]
            .sort_values(ascending=False)
            .head(2)
            .index
            .tolist()
        )

    # -----------------------------
    # 2️⃣ Representative Articles (Market-Level)
    # -----------------------------
    top_negative_articles = (
        df[df["finbert_label"] == "negative"]
        .head(3)["Combined_Text"]
        .tolist()
    )

    top_positive_articles = (
        df[df["finbert_label"] == "positive"]
        .head(3)["Combined_Text"]
        .tolist()
    )

    # -----------------------------
    # 3️⃣ Market-Level Keyword Extraction
    # -----------------------------
    negative_texts = (
        df[df["finbert_label"] == "negative"]["Cleaned_Text"]
        .dropna()
        .tolist()
    )

    market_word_counter = Counter()

    for text in negative_texts:
        market_word_counter.update(text.split())

    dominant_negative_keywords = [
        word
        for word, _ in market_word_counter.most_common(5)
        if len(word) > 3 and word not in stop_words
    ]

    # -----------------------------
    # 4️⃣ Market-Level Causal Interpretation
    # -----------------------------

    driver_scores = {
        "Complaint-driven": sum(market_word_counter[k] for k in complaint_keywords if k in market_word_counter),
        "Competition-driven": sum(market_word_counter[k] for k in competition_keywords if k in market_word_counter),
        "Regulatory-driven": sum(market_word_counter[k] for k in regulatory_keywords if k in market_word_counter),
        "Market/IPO-driven": sum(market_word_counter[k] for k in market_keywords if k in market_word_counter),
        "Employment-driven": sum(market_word_counter[k] for k in employment_keywords if k in market_word_counter),
    }

    top_driver = max(driver_scores, key=driver_scores.get)
    top_score = driver_scores[top_driver]

    if top_score <= 1:  # threshold to avoid weak signals
        causal_interpretation = "Negative sentiment appears broadly distributed across themes."
    else:
        causal_interpretation = f"Negative sentiment appears primarily {top_driver.lower()}."
    # -----------------------------
    # 5️⃣ Brand-Level Explainability
    # -----------------------------
    brand_explanations = []

    for brand in df["Brand"].unique():

        brand_df = df[df["Brand"] == brand]

        # Skip brands with very few articles (avoid noise)
        if len(brand_df) < 3:
            continue

        brand_negative_texts = (
            brand_df[brand_df["finbert_label"] == "negative"]["Cleaned_Text"]
            .dropna()
            .tolist()
        )

        brand_word_counter = Counter()

        for text in brand_negative_texts:
            brand_word_counter.update(text.split())

        dominant_keywords = [
            word
            for word, _ in brand_word_counter.most_common(3)
            if len(word) > 3 and word not in stop_words
        ]

        brand_driver_scores = {
            "Complaint-driven": sum(brand_word_counter[k] for k in complaint_keywords if k in brand_word_counter),
            "Competition-driven": sum(brand_word_counter[k] for k in competition_keywords if k in brand_word_counter),
            "Regulatory-driven": sum(brand_word_counter[k] for k in regulatory_keywords if k in brand_word_counter),
            "Market/IPO-driven": sum(brand_word_counter[k] for k in market_keywords if k in brand_word_counter),
            "Employment-driven": sum(brand_word_counter[k] for k in employment_keywords if k in brand_word_counter),
        }

        top_driver = max(brand_driver_scores, key=brand_driver_scores.get)

        if brand_driver_scores[top_driver] == 0:
            trend_driver = "Broad-based or Low signal"
        else:
            trend_driver = top_driver
        representative_article = (
            brand_df[brand_df["finbert_label"] == "negative"]
            .head(1)["Combined_Text"]
            .values[0]
            if not brand_df[brand_df["finbert_label"] == "negative"].empty
            else None
        )

        brand_explanations.append({
            "brand": brand,
            "trend_driver": trend_driver,
            "dominant_keywords": dominant_keywords,
            "representative_article": representative_article
        })

    # -----------------------------
    # Final Output
    # -----------------------------
    explainability_output = {
        "market_explainability": {
            "primary_negative_brands": negative_drivers,
            "primary_positive_brands": positive_drivers,
            "representative_negative_articles": top_negative_articles,
            "representative_positive_articles": top_positive_articles,
            "dominant_negative_keywords": dominant_negative_keywords,
            "causal_interpretation": causal_interpretation
        },
        "brand_explainability": brand_explanations
    }

    return explainability_output