# AI-Powered E-Commerce Market Intelligence & Trend Forecast Engine

An AI-driven analytics platform that analyzes news sentiment, emerging narratives, and market signals to generate consumer trend insights and sentiment forecasts for the e-commerce industry.

The system combines NLP models, machine learning forecasting, and Retrieval-Augmented Generation (RAG) to convert raw news data into structured market intelligence.

---

## Project Features

### Data Collection
Collects e-commerce related news articles using NewsAPI and tracks multiple Indian e-commerce brands.

### Sentiment Analysis
Uses FinBERT (financial transformer model) for sentiment analysis and generates sentiment scores for each article.

### Topic Modeling
Uses LLM-based topic classification to extract emerging narratives such as logistics, expansion, funding, customer complaints, and regulations.

### Market Intelligence Engine
Detects key signals including:
- market sentiment trend
- brand momentum
- narrative momentum
- sentiment volatility
- topic drivers

### Event Signal Engine
Identifies sector-wide signals like:
- competition intensity
- complaint pressure
- sector narrative heat

### Forecasting Engine
Uses Random Forest Regression to forecast:
- 7-day sentiment trend
- 30-day sentiment trend
- 90-day sentiment trend

### RAG Market Insight Engine
Uses LangChain + FAISS + Llama (Groq API) to generate:
- AI-generated market explanations
- contextual consumer insights
- market risk signals

### Explainability Layer
Provides transparency via:
- feature importance
- forecast drivers
- narrative attribution

### AI Market Report Generator
Automatically produces a human-readable market intelligence report.

---

## Project Architecture

```

News API
↓
Data Ingestion
↓
Text Preprocessing
↓
FinBERT Sentiment Analysis
↓
LLM Topic Extraction
↓
Master Dataset
↓
Analytics Engines
↓
Market Intelligence
↓
RAG Insight Engine
↓
ML Forecast Model
↓
Explainability Engine
↓
AI Market Report

```

---

## Project Structure

```

AI-Ecommerce-Trend-Forecaster
│
├── src
│   ├── ingestion
│   ├── preprocessing
│   ├── sentiment
│   ├── topic_modeling
│   ├── analytics
│   ├── intelligence
│   ├── narrative
│   ├── models
│   ├── rag
│   └── utils
│
├── data
│   ├── raw
│   ├── processed
│   └── output
│
├── vector_store
│
├── run_market_engine.py
├── requirements.txt
└── README.md

````

### Directory Notes

**src/**  
Contains the core modules of the project pipeline including ingestion, sentiment analysis, topic modeling, forecasting models, and RAG engines.

**data/**  
Stores raw, processed, and output datasets generated throughout the pipeline.

**vector_store/**  
FAISS vector database used for semantic retrieval in the RAG insight engine.

---

## Installation & Setup

### Clone Repository
```bash
git clone https://github.com/your-repo-name.git
cd AI-Ecommerce-Trend-Forecaster
````

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate environment:

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```
GROQ_API_KEY=your_groq_api_key
NEWS_API_KEY=your_newsapi_key
```

These are required for:

* Groq LLM API
* NewsAPI ingestion

---

## Running the Pipeline

Execute the full system:

```bash
python run_market_engine.py
```

This runs:

1. News ingestion
2. Text preprocessing
3. FinBERT sentiment analysis
4. LLM topic extraction
5. Master dataset creation
6. Market intelligence analytics
7. Event signal detection
8. Narrative intelligence
9. Forecast generation
10. RAG market insights
11. Explainability engine
12. AI market report generation

---

## Output Files

### Structured Data

```
data/processed/final_market_signal.json
```

Contains:

* market signals
* topic insights
* event signals
* forecast predictions
* RAG explanations

### AI Generated Market Report

```
data/processed/market_report.txt
```

Includes:

* market overview
* brand dynamics
* narrative trends
* emerging risks
* AI-generated strategic insights

---

## Example Forecast Output

Trend Direction: Bearish
Trend Slope: -0.023
Volatility: 0.46
Confidence Score: 0.53

Forecast Horizons:

* 7 Day Forecast
* 30 Day Forecast
* 90 Day Forecast

---

## Technologies Used

### NLP / AI

* FinBERT
* Llama 3
* HuggingFace Transformers
* LangChain

### Machine Learning

* Random Forest Regression
* Feature Engineering
* Walk-forward validation

### Retrieval Augmented Generation

* FAISS Vector Database
* Sentence Transformers
* Groq API

### Data Processing

* Pandas
* NumPy

---

## Model Evaluation

Example evaluation metrics:

```
MAE: 0.42
RMSE: 0.47
R²: -3.25
```

Low R² occurs due to limited historical data (~14 days).

With more data (40–60 days), performance improves significantly.

---

## Future Improvements

Potential enhancements:

* real-time social media sentiment analysis
* dashboard visualization
* alert system for market risk signals
* automated weekly intelligence reports
* deployment as a web API

---

## License

This project is developed for educational and research purposes.

---

## Contributors

Project developed as part of an AI Market Intelligence System for analyzing e-commerce sentiment and trends.

