import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_PATH = "data/qa.json"
MODEL_PATH = "model/vectorizer.pkl"

def train():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = [item["question"] for item in data]

    vectorizer = TfidfVectorizer()
    vectorizer.fit(questions)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    print("Model NLP berhasil dilatih dan disimpan.")

if __name__ == "__main__":
    train()