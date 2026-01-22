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

    # Flatten semua pertanyaan dari semua intent
    questions = []
    for item in data:
        for q in item["questions"]:
            questions.append(preprocess_text(q))

    vectorizer = TfidfVectorizer()
    vectorizer.fit(questions)

    MODEL_PATH.parent.mkdir(exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    print("Model NLP (intent-based) berhasil dilatih.")


if __name__ == "__main__":
    train()