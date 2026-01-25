import json
import pickle
import random
from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity

from core.utils import preprocess_text
from core.trainer import train
from core.failed_logger import log_failed_question
from core.text_generator import TextGenerator

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

        self.questions: list[str] = []
        self.answers: list[list[str]] = []

        # Flatten questions -> answers (multi jawaban)
        for item in self.data:
            answers = item.get("answers", [])
            for q in item.get("questions", []):
                self.questions.append(preprocess_text(q))
                self.answers.append(answers)

        self.question_vectors = self.vectorizer.transform(self.questions)

        # ===== INIT GENERATOR (FALLBACK) =====
        all_answer_texts: list[str] = []
        for ans_list in self.answers:
            all_answer_texts.extend(ans_list)

        self.generator = TextGenerator(all_answer_texts)

    # ===============================
    # QA DENGAN SCORE
    # ===============================
    def ask_with_score(self, text: str):
        processed = preprocess_text(text)
        user_vector = self.vectorizer.transform([processed])

        similarity = cosine_similarity(user_vector, self.question_vectors)
        best_index = similarity.argmax()
        best_score = similarity[0][best_index]

        if best_score < 0.25:
            log_failed_question(text, best_score)
            return None, best_score

        possible_answers = self.answers[best_index]
        if not possible_answers:
            return None, best_score

        answer = random.choice(possible_answers)
        return answer, best_score

    # ===============================
    # MODE HYBRID (QA → GENERATIVE)
    # ===============================
    def ask(self, text: str):
        answer, score = self.ask_with_score(text)

        if answer:
            return answer, score

        # Fallback ke generator (mode eksperimen)
        generated = self.generator.generate(text)
        if generated:
            return generated, score

        return "Saya belum bisa menjawab pertanyaan ini.", score