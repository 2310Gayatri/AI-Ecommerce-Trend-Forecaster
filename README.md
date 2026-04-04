# 🚀 AI-Powered Market Trend & Consumer Sentiment Forecaster

An end-to-end AI system that analyzes ecommerce market trends using multi-source data (news + Google Trends + consumer signals) and generates actionable business insights with explainability. The project features a fully automated data pipeline and a modern, live frontend dashboard.

---

## 📌 Overview

This project builds a **real-time market intelligence pipeline** that:

- Aggregates ecommerce news and Google Trends data
- Performs sentiment analysis using FinBERT
- Extracts topics using LLM-based modeling
- Computes trend scores, momentum, and volatility
- Generates explainable insights using RAG (Retrieval-Augmented Generation)
- Produces alerts, forecasts, and PDF reports
- **Automatically updates a live React/Vite dashboard deployed on Vercel** using GitHub Actions

---

## 🔄 System Workflow

```text
News API + Google Trends
        ↓
Data Preprocessing
        ↓
Sentiment Analysis (FinBERT)
        ↓
Topic Modeling (LLM)
        ↓
Feature Engineering (trend, velocity, entropy)
        ↓
Market Intelligence Engine
        ↓
Forecasting + Signals
        ↓
RAG-based Explainability
        ↓
Reports + Alerts + Live Dashboard JSON
        ↓
GitHub Actions Auto-Commit
        ↓
Vercel Auto-Deployment
```

---

## 🧠 Key Features

✔ Multi-source data ingestion (News + Google Trends)  
✔ NLP-based sentiment analysis (FinBERT)  
✔ Topic modeling using LLM  
✔ Time-series trend analysis (momentum, velocity, entropy)  
✔ Market intelligence engine (signals, risks, drivers)  
✔ RAG-based explainable insights  
✔ Forecasting module & Event signal detection  
✔ Automated PDF report generation  
✔ **Live Frontend Dashboard (React + Vite + TailwindCSS)**  
✔ **Automated CI/CD Pipeline (GitHub Actions)**  

---

## 🏗️ Project Architecture

```
TEAM-REPO/
│
├── .github/workflows/          # CI/CD pipelines (Auto-updating dashboard)
│
├── frontend/                   # React + Vite Dashboard Application
│   ├── public/                 # Output location for JSON data
│   ├── src/
│   │   ├── components/         # Reusable UI elements (Sidebar, Charts)
│   │   └── pages/              # Dashboard pages (Overview, Brands, Topics, Sources, etc.)
│   └── vite.config.js          # Vite configuration
│
├── data/                       # Contains raw, processed, and archive datasets
├── scripts/                    # Helper scripts for data fetching
├── src/                        # Core Python intelligence pipeline
│   ├── analytics/
│   ├── consumer/
│   ├── ingestion/
│   ├── intelligence/
│   ├── models/
│   ├── rag/
│   ├── reporting/
│   ├── sentiment/
│   └── topic_modeling/
│
├── vector_store/               # FAISS vector database for RAG retrieval
├── config.py                   # Global configuration
├── run_market_engine.py        # Main execution script
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 📊 Live Frontend Dashboard

The project includes a robust and rich frontend dashboard built with React and Vite. It consumes the `market_dashboard_data.json` outputted by the Python engine. 

### Key Dashboard Pages:
* **Overview:** High-level metrics, trend direction (Bullish/Bearish), and market summary.
* **Brand Insights:** Compares top e-commerce brands' digital momentum and sentiment over time.
* **Topics & Keywords:** Discover trending hashtags, emerging entities, and major market narrative shifts.
* **News Details:** See chronological news data grouped by sentiment categories.
* **Alerts & Forecasts:** Identifies sudden volatility peaks and short-term forecasting indicators.
* **Research Sources:** RAG-powered reference page, listing transparent sources used by the intelligence engine for deep dive research.

---

## ⚙️ Installation & Setup

### Clone Repository
```bash
git clone https://github.com/your-repo-name.git
cd AI-Ecommerce-Trend-Forecaster
```

### Backend (Python Engine) Setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```
GROQ_API_KEY=your_groq_api_key
NEWS_API_KEY=your_newsapi_key
SERP_API_KEY=your_serpapi_key
```

These are required for:
* Groq LLM API (for RAG and Topic Extraction)
* NewsAPI ingestion
* SerpAPI Google Trends data

---

## 🚀 Running the Pipeline

### Manual Run
To execute the pipeline locally, run the main orchestration engine:

```bash
python run_market_engine.py
```

### Automated Run (GitHub Actions)
The repository is configured to **automate the dashboard update every 6 hours**.
- The `update_dashboard.yml` workflow triggers on schedule.
- Checks out the code and installs Python dependencies.
- Runs `run_market_engine.py`.
- Takes the newly generated `market_dashboard_data.json` and automatically commits/pushes it to the branch.
- This push automatically triggers Vercel to redeploy the frontend with fresh dashboard data. No persistent backend servers required!

---

## 📦 Output Files Generated

### Processed Data
* `news_master_dataset.csv`, `daily_market_metrics.csv`
* `brand_daily_metrics.csv`, `consumer_sentiment.csv`

### AI Generated Market Report
* `data/output/market_report.pdf`
* `market_report.txt`

### Dashboard Content 
* **`frontend/public/market_dashboard_data.json`** - The master payload driving the frontend visualization UI.
* `alerts.json` - High momentum shifts and volatility detection arrays.

---

## 🧪 Model Evaluation

Example evaluation metrics for the backend forecasting logic:

```
MAE: 0.42
RMSE: 0.47
R²: -3.25
```

*Note: Low R² occurs due to limited historical data (~14 days). With a longer running cron-job (40–60 days), performance model stabilizes significantly.*

---

## 🛠️ Technologies Used

### Backend AI Engine
* **NLP:** FinBERT, HuggingFace Transformers
* **Topic Modeling:** Llama 3 (via Groq API), LangChain
* **RAG:** FAISS Vector Database, Sentence Transformers
* **ML Analytics:** Random Forest Regression, Scikit-Learn, Pandas, NumPy

### Frontend Application
* **Framework:** React 18, Vite
* **Styling:** Tailwind CSS, Framer Motion (for dynamic UI animations)
* **Charts & Data Viz:** Recharts

### DevOps
* **CI/CD:** GitHub Actions
* **Hosting:** Vercel (Static Frontend & Edge delivery)

---

## 🚀 Deployment on Vercel

Because all AI processing happens asynchronously via GitHub Actions, the resulting React dashboard can be deployed as an infinitely scalable static site on **Vercel**:

1. Push complete project code to a GitHub repository.
2. Log in to [Vercel](https://vercel.com/) and click **Add New** -> **Project**.
3. Import GitHub repository.
4. Framework Preset: **Vite**
5. Root Directory: **`frontend`**
6. Build Command: `npm run build`, Output Directory: `dist`
7. Click **Deploy**. Vercel will build your application.

Now, every time GitHub Actions successfully runs the Python AI Engine and updates `market_dashboard_data.json`, Vercel will detect the new commit and rebuild the frontend to keep your market data live constantly.

---

## License

This project is developed for educational and research purposes.

---

## Contributors

Project developed as part of an AI Market Intelligence System for analyzing e-commerce sentiment and trends.
