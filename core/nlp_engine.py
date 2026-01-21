import json
import pickle
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

from core.utils import preprocess_text
from core.trainer import train

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "qa.json"
MODEL_PATH = BASE_DIR / "model" / "vectorizer.pkl"


class NLPEngine:
    def __init__(self):
        # === PASTIKAN MODEL ADA ===
        if not MODEL_PATH.exists():
            print("[INFO] Model belum ada, training awal dijalankan...")
            train()

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        with open(MODEL_PATH, "rb") as f:
            self.vectorizer = pickle.load(f)

        self.questions = [preprocess_text(item["question"]) for item in self.data]
        self.answers = [item["answer"] for item in self.data]

        self.question_vectors = self.vectorizer.transform(self.questions)

    def ask_with_score(self, text: str):
        processed = preprocess_text(text)
        user_vector = self.vectorizer.transform([processed])

        similarity = cosine_similarity(user_vector, self.question_vectors)
        best_index = similarity.argmax()
        best_score = similarity[0][best_index]

        if best_score < 0.25:
            return None, best_score

        return self.answers[best_index], best_score