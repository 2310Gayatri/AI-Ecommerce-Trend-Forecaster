import pandas as pd
import os

def run_event_signals():
    print("Running Event Signal Engine...")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    input_path = os.path.join(BASE_DIR, "data", "processed", "finbert_output.csv")

    df = pd.read_csv(input_path)

    # Combine text fields safely
    # Use existing combined text column
    df["text_combined"] = df["Combined_Text"].fillna("").str.lower()

    # ---------------------------
    # 1️⃣ Define Keyword Sets
    # ---------------------------

    competition_keywords = [
        "sale", "discount", "cashback", "festive offer",
        "mega sale", "price cut", "clearance",
        "big billion", "great indian festival",
        "promotional"
    ]

    complaint_keywords = [
        "delivery delay", "fraud", "fake product",
        "refund issue", "complaint", "quality issue",
        "grievance", "poor service", "return issue"
    ]

    # ---------------------------
    # 2️⃣ Tag Competition & Complaint
    # ---------------------------

    def contains_keyword(text, keywords):
        return any(keyword in text for keyword in keywords)

    df["competition_flag"] = df.apply(
        lambda row: contains_keyword(row["text_combined"], competition_keywords)
        and row["finbert_label"] in ["positive", "neutral"],
        axis=1
    )

    df["complaint_flag"] = df.apply(
        lambda row: contains_keyword(row["text_combined"], complaint_keywords)
        and row["finbert_label"] == "negative",
        axis=1
    )

    # ---------------------------
    # 3️⃣ Daily Aggregation
    # ---------------------------

    df["Published_Date"] = pd.to_datetime(df["Published_Date"])
    df["date"] = df["Published_Date"].dt.date

    daily_signals = df.groupby("date").agg(
        competition_count=("competition_flag", "sum"),
        complaint_count=("complaint_flag", "sum"),
        article_volume=("text_combined", "count")
    ).reset_index()

    # ADD THIS LINE
    daily_signals["volume_ma7"] = daily_signals["article_volume"].rolling(7, min_periods=1).mean()

    # ---------------------------
    # 4️⃣ Enhanced Signal Calculations
    # ---------------------------

    latest = daily_signals.iloc[-1]

    # Competition Strength
    competition_ma7 = daily_signals["competition_count"].rolling(7, min_periods=1).mean().iloc[-1]
    competition_today = latest["competition_count"]

    if competition_ma7 == 0:
        competition_ratio = competition_today
    else:
        competition_ratio = competition_today / competition_ma7

    if competition_ratio >= 2:
        competition_level = "High"
    elif competition_ratio > 1:
        competition_level = "Moderate"
    elif competition_today == 0:
        competition_level = "Low"
    else:
        competition_level = "Stable"

    # Complaint Strength
    complaint_ma7 = daily_signals["complaint_count"].rolling(7, min_periods=1).mean().iloc[-1]
    complaint_today = latest["complaint_count"]

    if complaint_ma7 == 0:
        complaint_ratio = complaint_today
    else:
        complaint_ratio = complaint_today / complaint_ma7

    if complaint_ratio >= 2:
        complaint_level = "High"
    elif complaint_ratio > 1:
        complaint_level = "Moderate"
    elif complaint_today == 0:
        complaint_level = "Low"
    else:
        complaint_level = "Stable"

    # Sector Heat
    volume_today = latest["article_volume"]
    volume_ma7 = latest["volume_ma7"]

    heat_ratio = volume_today / volume_ma7 if volume_ma7 != 0 else 0

    if heat_ratio >= 1.5:
        sector_heat = "High Narrative Heat"
    elif heat_ratio > 1.1:
        sector_heat = "Elevated Attention"
    elif heat_ratio < 0.8:
        sector_heat = "Cooling"
    else:
        sector_heat = "Stable"

    # ---------------------------
    # 5️⃣ Brand Drivers
    # ---------------------------

    competition_brands = df[df["competition_flag"] == True]["Brand"].value_counts().index.tolist()
    complaint_brands = df[df["complaint_flag"] == True]["Brand"].value_counts().index.tolist()

    # ---------------------------
    # 6️⃣ Narrative Summary
    # ---------------------------

    summary = f"""
    Current ecommerce market signals indicate elevated competitive activity.
    
    Promotional intensity is classified as {competition_level}, 
    with activity running at {round(competition_ratio,2)} times the recent weekly average.
    This suggests increased promotional campaigns or discount activity across major platforms.
    
    Complaint-related coverage remains {complaint_level.lower()},
    indicating no significant rise in consumer grievance-driven negative narratives at this time.
    
    Sector media attention is categorized as {sector_heat}, 
    with overall article volume at {round(heat_ratio,2)} times the weekly baseline.
    This reflects heightened narrative attention toward the ecommerce sector.
    
    Promotion-related coverage is associated with: {competition_brands if competition_brands else "no dominant brand drivers"}.
    Complaint-related coverage is associated with: {complaint_brands if complaint_brands else "no significant complaint drivers"}.
    """
    # ---------------------------
    # 7️⃣ Structured Output
    # ---------------------------

    output = {
        "competition_intensity": competition_level,
        "competition_ratio": round(float(competition_ratio),2),
        "complaint_pressure": complaint_level,
        "complaint_ratio": round(float(complaint_ratio),2),
        "sector_heat": sector_heat,
        "heat_ratio": round(float(heat_ratio),2),
        "competition_brands": competition_brands,
        "complaint_brands": complaint_brands
    }

    print("\n--- Analytical Signals ---")
    print(output)

    print("\n--- Narrative Summary ---")
    print(summary)
    return output, summary

if __name__ == "__main__":
    output, summary = run_event_signals()
    print(summary)
    print(output)