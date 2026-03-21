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

    # extract start + end
    df[["start_part", "end_part"]] = df["date"].str.split("–", expand=True)

    # extract year from end_part
    df["year"] = df["end_part"].str.extract(r'(\d{4})')
    df["year"] = df["year"].fillna(pd.Timestamp.now().year)
    # clean start part
    df["start_part"] = df["start_part"].str.strip()

    # convert start date
    start_date = pd.to_datetime(
        df["start_part"] + " " + df["year"],
        format="%b %d %Y",
        errors="coerce"
    )

    # extract end day
    df["end_day"] = df["end_part"].str.replace(",", "").str.extract(r'(\d{1,2})')

    end_date = pd.to_datetime(
        df["start_part"].str.split().str[0] + " " + df["end_day"] + " " + df["year"],
        format="%b %d %Y",
        errors="coerce"
    )
    end_date = end_date.fillna(start_date)

    # midpoint
    df["date"] = start_date + (end_date - start_date) / 2

    # cleanup
    df = df.drop(columns=["start_part", "end_part", "year","end_day"])

    df = df.dropna(subset=["date"])

    # ---------------------------
    # AGGREGATE DUPLICATES
    # ---------------------------
    df = df.groupby(['date', 'brand'], as_index=False)['trend_score'].mean()

    # 🔥 IMPORTANT: sort before smoothing
    df = df.sort_values(["brand", "date"])
    # set index for time-series
    df = df.set_index("date")

    # apply per brand WITHOUT duplicating columns
    df = (
        df.groupby("brand", group_keys=False)
        .apply(lambda x: x.asfreq("D").ffill())
        .reset_index()
    )
    # ---------------------------
    # SMOOTHING
    # ---------------------------
    df = df.sort_values(["brand", "date"])

    df["trend_score"] = df.groupby("brand")["trend_score"].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean()
    )
    # global normalization AFTER smoothing
    max_val = df["trend_score"].max()
    if max_val > 0:
        df["trend_score"] = df["trend_score"] / max_val

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