# 📊 AI-Powered E-Commerce Market Signal & Forecast Engine

This project builds a multi-layered AI pipeline that collects real-time e-commerce news, performs financial sentiment analysis, detects competitive signals, and generates short-term market forecasts.

The system transforms raw news into structured market intelligence.

---

## 🚀 Core Capabilities

### 🔹 Real-Time News Ingestion
- Multi-brand tracking via **NewsAPI**
- 17+ Indian e-commerce brands monitored
- Structured raw data storage

---

### 🔹 Advanced Sentiment Analysis
- **VADER** (rule-based baseline)
- **TextBlob** (lexicon-based baseline)
- **FinBERT** (finance-domain transformer model)
- Article-level polarity classification
- Confidence scoring

---

### 🔹 Daily Market Sentiment Index
- Converts sentiment to numeric values
- Aggregates into daily average index
- Time-series representation of overall market mood

---

### 🔹 Brand-Level Intelligence
- Brand daily sentiment index
- Brand momentum detection
- Brand volatility analysis
- Top improving & declining brands

---

### 🔹 Event Signal Engine

Detects structural signals such as:

- 🔥 Competition intensity  
- ⚠️ Complaint pressure  
- 📢 Sector narrative heat  

Uses ratio-based classification and keyword-driven detection.

---

### 🔹 Forecast Engine
- 7-day market sentiment forecast
- 7-day brand-level sentiment forecast
- Linear regression trend projection
- Volatility measurement
- Confidence scoring

---

### 🔹 Unified Output

Generates structured output:
data/processed/final_market_signal.json


Includes:
- Market signals
- Event signals
- Forecast signals

Fully backend-ready.

---

## 🏗 Project Structure

AI-Ecommerce-Trend-Forecaster/
│
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── sentiment/
│   ├── trend/
│   │   ├── daily_sentiment_index.py
│   │   ├── brand_daily_index.py
│   │   ├── market_forecast.py
│   │   ├── market_intelligence.py
│   │   ├── event_signal_engine.py
│   │   └── ...
│   └── topic_modeling/ (planned expansion)
│
├── data/
│   ├── raw/
│   └── processed/
│
├── run_market_engine.py
├── config.py
├── requirements.txt
├── .env.example
└── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <repo-url>
cd AI-Ecommerce-Trend-Forecaster
```
2️⃣ Create Virtual Environment
```bash
2python -m venv .venv
.venv\Scripts\activate
```

Mac / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Configure Environment

1. Create a .env file in the root directory:

2. NEWS_API_KEY=your_news_api_key
```bash
NEWS_API_KEY=your_actual_news_api_key_here
```
3. Get your API key from:
👉 https://newsapi.org

⚠️ Do NOT commit your .env file to GitHub.

▶️ Run Complete Pipeline
```bash
python run_market_engine.py
```
The pipeline executes:

1. Ingestion
2. Preprocessing
3. Sentiment analysis
4. Daily index generation
5. Brand intelligence
6. Event signal detection
7. Market & brand forecasting
8. Final JSON export

📊 Output Example

Final structured output:
```bash
data/processed/final_market_signal.json
```
Contains:

📉 Market direction (Bullish / Bearish / Stable)

🔥 Competition intensity

⚠️ Complaint pressure

📢 Sector heat

📈 7-day sentiment forecast

🏷 Brand-level projections

🧠 System Design
```bash
Data Layer
   ↓
NLP Layer
   ↓
Aggregation Layer
   ↓
Intelligence Layer
   ↓
Forecast Layer
   ↓
Structured Output
```

This is a sentiment-driven market signal detection and forecasting engine.