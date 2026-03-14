import os
import pandas as pd


def get_base_dir():
    """
    Returns project root directory
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load_master_dataset():

    base_dir = get_base_dir()

    path = os.path.join(
        base_dir,
        "data",
        "processed",
        "news_master_dataset.csv"
    )

    if not os.path.exists(path):
        raise FileNotFoundError("news_master_dataset.csv not found")

    df = pd.read_csv(path)

    return df


def load_daily_metrics():

    base_dir = get_base_dir()

    path = os.path.join(
        base_dir,
        "data",
        "processed",
        "daily_market_metrics.csv"
    )

    if not os.path.exists(path):
        raise FileNotFoundError("daily_market_metrics.csv not found")

    return pd.read_csv(path)


def load_brand_metrics():

    base_dir = get_base_dir()

    path = os.path.join(
        base_dir,
        "data",
        "processed",
        "brand_daily_metrics.csv"
    )

    if not os.path.exists(path):
        raise FileNotFoundError("brand_daily_metrics.csv not found")

    return pd.read_csv(path)