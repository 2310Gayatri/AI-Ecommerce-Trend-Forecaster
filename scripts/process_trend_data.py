import pandas as pd
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

INPUT_PATH = os.path.join(BASE_DIR, "data", "raw", "trend_data.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "trend_data_cleaned.csv")


# ---------------------------
# MAIN PROCESS FUNCTION
# ---------------------------
def process_trend_data():

    if not os.path.exists(INPUT_PATH):
        print("❌ Trend data not found, skipping processing")
        return

    print("Processing trend data...")

    # ---------------------------
    # LOAD DATA
    # ---------------------------
    df = pd.read_csv(INPUT_PATH)

    print("Original Data:")
    print(df.head())

    # ---------------------------
    # CLEANING
    # ---------------------------

    # ensure numeric
    df['trend_score'] = pd.to_numeric(df['trend_score'], errors='coerce')

    # fill missing
    df['trend_score'] = df['trend_score'].fillna(0)

    # ensure string format
    df['date'] = df['date'].astype(str)

    # ---------------------------
    # AGGREGATE DUPLICATES
    # ---------------------------
    df = df.groupby(['date', 'brand'], as_index=False)['trend_score'].mean()

    # 🔥 IMPORTANT: sort before smoothing
    df = df.sort_values(["brand", "date"])

    # ---------------------------
    # SMOOTHING
    # ---------------------------
    df["trend_score"] = df.groupby("brand")["trend_score"].transform(
        lambda x: x.rolling(3, min_periods=1).mean()
    )

    # ---------------------------
    # SAVE CLEAN DATA
    # ---------------------------
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\n✅ Cleaned trend data saved!")
    print(df.head())


# ---------------------------
# OPTIONAL: RUN STANDALONE
# ---------------------------
if __name__ == "__main__":
    process_trend_data()