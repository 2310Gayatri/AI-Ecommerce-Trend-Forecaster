import requests
import pandas as pd
import os
from datetime import datetime
from config import NEWS_API_KEY, ECOMMERCE_BRANDS

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

def fetch_news_for_brands(brands, page_size=10):
    all_news = []

    url = "https://newsapi.org/v2/everything"

    for brand in brands:
        print(f"Fetching news for {brand}...")

        params = {
            "q": brand,
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"Error fetching data for {brand}: {response.status_code}")
            continue

        data = response.json()
        articles = data.get("articles", [])

        for article in articles:
            all_news.append({
                "brand": brand,
                "source": article["source"]["name"],
                "title": article["title"],
                "description": article["description"],
                "content": article["content"],
                "published_at": article["publishedAt"],
                "fetched_at": datetime.now()
            })

    df = pd.DataFrame(all_news)
    return df


def save_news_to_csv(df):
    # Use the already defined BASE_DIR
    save_dir = os.path.join(BASE_DIR, "data", "raw")
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, "news_data.csv")

    df.to_csv(file_path, index=False)
    print(f"\nNews data saved to: {file_path}")


if __name__ == "__main__":
    print("Starting multi-brand news ingestion...\n")

    brands = ECOMMERCE_BRANDS

    df = fetch_news_for_brands(brands, page_size=10)

    if df is not None and not df.empty:
        save_news_to_csv(df)
        print("\nSample Data:\n")
        print(df.head())
    else:
        print("No data fetched.")
