import json
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

from core.utils import preprocess_text

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "qa.json"
MODEL_PATH = BASE_DIR / "model" / "vectorizer.pkl"


def train():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # PREPROCESS DATASET
    questions = [
        preprocess_text(item["question"])
        for item in data
    ]

    vectorizer = TfidfVectorizer()
    vectorizer.fit(questions)

    MODEL_PATH.parent.mkdir(exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    print("Model NLP (dengan stemming) berhasil dilatih.")


if __name__ == "__main__":
    train()