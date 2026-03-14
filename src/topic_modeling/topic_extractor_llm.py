import os
import json
import pandas as pd
import re
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Project root directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


def extract_topics_batch(texts):
    """
    Sends a batch of news articles to the LLM and returns topic predictions.
    """

    numbered_text = "\n\n".join(
        [f"{i+1}. {t}" for i, t in enumerate(texts)]
    )

    prompt = f"""
You are analyzing e-commerce news.

For each numbered news item, classify the MAIN topic.

Topics:
- Discounts
- Logistics
- Competition
- Funding
- Customer Complaints
- Regulation
- Expansion
- Partnerships
- Technology
- Other

Return ONLY a JSON list.

Example:

[
  {{"topic":"Expansion","confidence":0.85}},
  {{"topic":"Technology","confidence":0.90}}
]

News Articles:
{numbered_text}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        result = response.choices[0].message.content

        print("LLM BATCH RESPONSE:", result)

        json_match = re.search(r"\[.*\]", result, re.DOTALL)

        if json_match:
            return json.loads(json_match.group())

        return [{"topic": "Other", "confidence": 0.0}] * len(texts)

    except Exception as e:

        print("TOPIC EXTRACTION ERROR:", e)

        return [{"topic": "Other", "confidence": 0.0}] * len(texts)


def run_topic_extraction():
    """
    Runs topic extraction on the cleaned news dataset.
    """

    input_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_news.csv")
    output_path = os.path.join(BASE_DIR, "data", "processed", "news_with_topics.csv")

    df = pd.read_csv(input_path)

    texts = df["Combined_Text"].tolist()

    batch_size = 10

    topics = []
    confidences = []

    for i in range(0, len(texts), batch_size):

        batch = texts[i:i + batch_size]

        results = extract_topics_batch(batch)

        for r in results:
            topics.append(r["topic"])
            confidences.append(r["confidence"])

    df["topic"] = topics
    df["topic_confidence"] = confidences

    df.to_csv(output_path, index=False)

    print("✅ Topic extraction completed")