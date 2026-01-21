import json
import pickle
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = "data/qa.json"
MODEL_PATH = "model/vectorizer.pkl"

class NLPEngine:
    def __init__(self):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        with open(MODEL_PATH, "rb") as f:
            self.vectorizer = pickle.load(f)

        self.questions = [item["question"] for item in self.data]
        self.answers = [item["answer"] for item in self.data]
        self.question_vectors = self.vectorizer.transform(self.questions)

    def ask(self, text: str) -> str:
        user_vector = self.vectorizer.transform([text])
        similarity = cosine_similarity(user_vector, self.question_vectors)
        best_index = similarity.argmax()

        if similarity[0][best_index] < 0.2:
            return "Maaf, saya belum mengerti pertanyaan itu."

        return self.answers[best_index]