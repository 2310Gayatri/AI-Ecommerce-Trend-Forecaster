import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
import json


def run_finbert():

    print("Starting FinBERT analysis...")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

    input_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_news.csv")
    output_path = os.path.join(BASE_DIR, "data", "processed", "finbert_output.csv")
    summary_path = os.path.join(BASE_DIR, "data", "processed", "finbert_summary.json")

    df = pd.read_csv(input_path)

    model_name = "ProsusAI/finbert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    labels = []
    scores = []

    for text in df["Cleaned_Text"]:
        inputs = tokenizer(
            str(text),
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        with torch.no_grad():
            outputs = model(**inputs)

        probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
        confidence, predicted_class = torch.max(probabilities, dim=1)

        label = model.config.id2label[predicted_class.item()]

        labels.append(label)
        scores.append(float(confidence.item()))

    df["finbert_label"] = labels
    df["finbert_confidence"] = scores

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