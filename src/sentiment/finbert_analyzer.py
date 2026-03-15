import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
import json

# Project root
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


def run_finbert():

    print("Starting FinBERT analysis...")

    input_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_news.csv")
    output_path = os.path.join(BASE_DIR, "data", "processed", "finbert_output.csv")
    summary_path = os.path.join(BASE_DIR, "data", "processed", "finbert_summary.json")

    df = pd.read_csv(input_path)

    model_name = "ProsusAI/finbert"

    print("Loading FinBERT model...")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    model.eval()

    device = torch.device("cpu")
    model.to(device)

    texts = df["Cleaned_Text"].astype(str).tolist()

    # truncate extremely long texts to reduce memory usage
    texts = [text[:500] for text in texts]

    # safe batch size for 16GB RAM
    batch_size = 8

    labels = []
    confidences = []

    print(f"Processing {len(texts)} articles in batches of {batch_size}...")

    for i in range(0, len(texts), batch_size):

        batch_texts = texts[i:i + batch_size]

        inputs = tokenizer(
            batch_texts,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=256
        ).to(device)

        with torch.no_grad():
            outputs = model(**inputs)

        probs = torch.nn.functional.softmax(outputs.logits, dim=1)

        batch_conf, batch_pred = torch.max(probs, dim=1)

        for conf, pred in zip(batch_conf, batch_pred):

            label = model.config.id2label[pred.item()].lower()

            labels.append(label)
            confidences.append(float(conf.item()))

        # free memory immediately
        del inputs
        del outputs
        torch.cuda.empty_cache()

    df["finbert_label"] = labels
    df["finbert_confidence"] = confidences

    df.to_csv(output_path, index=False)

    summary = {
        "total_articles": len(df),
        "positive_count": labels.count("positive"),
        "negative_count": labels.count("negative"),
        "neutral_count": labels.count("neutral")
    }

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=4)

    print("FinBERT analysis complete.")

    return output_path


if __name__ == "__main__":
    run_finbert()