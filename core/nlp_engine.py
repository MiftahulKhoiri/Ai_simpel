import json
import pickle
import random
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

from core.utils import preprocess_text
from core.trainer import train
from core.failed_logger import log_failed_question

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "qa.json"
MODEL_PATH = BASE_DIR / "model" / "vectorizer.pkl"


class NLPEngine:
    def __init__(self):
        # Auto-train jika model belum ada
        if not MODEL_PATH.exists():
            print("[INFO] Model belum ada, training awal...")
            train()

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        with open(MODEL_PATH, "rb") as f:
            self.vectorizer = pickle.load(f)

        self.questions = []
        self.answers = []

        # Flatten questions → map ke answers (LIST)
        for item in self.data:
            answers = item.get("answers", [])
            for q in item.get("questions", []):
                self.questions.append(preprocess_text(q))
                self.answers.append(answers)

        self.question_vectors = self.vectorizer.transform(self.questions)

    def ask_with_score(self, text: str):
        processed = preprocess_text(text)
        user_vector = self.vectorizer.transform([processed])

        similarity = cosine_similarity(user_vector, self.question_vectors)
        best_index = similarity.argmax()
        best_score = similarity[0][best_index]

        if best_score < 0.25:
            # ⬇⬇⬇ LOG PERTANYAAN GAGAL
            log_failed_question(text, best_score)
            return None, best_score

        # PILIH JAWABAN ACAK DARI LIST
        possible_answers = self.answers[best_index]
        answer = random.choice(possible_answers)

        return answer, best_score