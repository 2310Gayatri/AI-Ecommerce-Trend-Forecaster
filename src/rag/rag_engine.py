import os
from dotenv import load_dotenv
import sys
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.rag.build_vector_store import build_vector_store
from groq import Groq


load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

VECTOR_PATH = os.path.join(BASE_DIR, "vector_store", "news_index")


# -----------------------------
# Load embedding + vector store once
# -----------------------------

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Ensure vector store exists
# -----------------------------
index_file = os.path.join(VECTOR_PATH, "index.faiss")

if not os.path.exists(index_file):
    print("⚠️ Vector store not found. Building now...")
    build_vector_store()

# -----------------------------
# Load vector store
# -----------------------------
vector_store = FAISS.load_local(
    VECTOR_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 8, "fetch_k": 20}
)


# -----------------------------
# LLM client
# -----------------------------

def get_llm_client():

    return Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------------
# RAG response
# -----------------------------

def generate_rag_response(query):

    client = get_llm_client()

    # Improve retrieval with context hint
    enhanced_query = f"ecommerce market trends {query}"

    docs = retriever.invoke(enhanced_query)

    # Handle empty retrieval (edge case)
    if not docs:
        return "No relevant information found in the dataset.", []

    sources = [
        {
            "source_id": i + 1,
            "content": doc.page_content[:200]
        }
        for i, doc in enumerate(docs)
    ]

    context = "\n\n".join([
        f"[Source {i + 1}]\n{doc.page_content[:400]}"
        for i, doc in enumerate(docs)
    ])

    prompt = f"""
    You are a senior ecommerce market intelligence analyst.

    Your task is to analyze the provided news context STRICTLY based on evidence.

    ⚠️ RULES:
    - Use ONLY the provided context.
    - DO NOT make assumptions or guesses.
    - If information is not present, say "Not explicitly mentioned".
    - Be specific and reference brands/topics from context.
    - Always reference source numbers like (Source 1), (Source 2).
    - If a brand is not present in the context, DO NOT mention it.
    - Do not combine external signals (like top_negative_brand) with retrieved context.

    Context:
    {context}

    Question:
    {query}

    Provide output using clean bullet points (no numbering).

    1. Key Market Signals
    - Bullet points of clear signals from the news.

    2. Brand Impact
    - Mention ONLY brands explicitly present in the context.
    - Explain impact using evidence.

    3. Consumer Sentiment Drivers
    - Link sentiment to actual events/topics in context.

    4. Strategic Insight
    - One concise, actionable takeaway.
    
    Avoid generic statements like "may", "might", or "could".
    Keep the answer concise, factual, and evidence-based.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )

        answer = response.choices[0].message.content

    except Exception as e:
        print(f"⚠️ LLM skipped due to: {e}")
        answer = "LLM response skipped due to rate limit."

    return answer, sources

    return response.choices[0].message.content, sources


# -----------------------------
# Risk signal detector
# -----------------------------

def generate_market_risk_signal():
    query = """
    Analyze ecommerce market risks STRICTLY based on the provided context.

    Classify risks into:

    - Regulatory risk
    - Logistics risk
    - Competition pressure
    - Consumer complaints
    - Technology disruption

    For each risk:
    - Mention the affected brand
    - Provide supporting evidence
    - Reference sources

    If no evidence exists, say "Not explicitly mentioned".

    Keep output concise and structured.
    """

    insight, sources = generate_rag_response(query)

    return insight

# -----------------------------
# Brand Insight Generator
# -----------------------------
def generate_brand_ai_insight(market_output):
    query = """
    Analyze brand performance trends using ONLY the provided news context.

    - Identify which brands show positive or negative sentiment based strictly on evidence.
    - Do NOT assume any brand performance unless explicitly supported.
    - If insufficient data exists, say "Not explicitly mentioned".

    Explain clearly WHY brands are performing this way based ONLY on the context.
    """
    insight, _ = generate_rag_response(query)

    return insight


# -----------------------------
# Topic Insight Generator
# -----------------------------
def generate_topic_ai_insight(market_output):
    query = """
    Explain topic trends in the ecommerce market using ONLY the provided context.

    - Identify which topics are increasing or decreasing based on evidence.
    - Do NOT rely on external computed metrics.
    - If not explicitly mentioned, say "Not explicitly mentioned".

    Explain WHY these topics are rising or falling.
    """

    insight, _ = generate_rag_response(query)

    return insight