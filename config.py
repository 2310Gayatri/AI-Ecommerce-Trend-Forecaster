import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ECOMMERCE_BRANDS = [
    "Flipkart",
    "Amazon India",
    "Myntra",
    "Snapdeal",
    "Meesho",
    "Ajio",
    "BigBasket",
    "Nykaa",
    "Reliance Digital",
    "Tata Cliq"
]
