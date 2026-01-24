import json
import random
import itertools
from pathlib import Path

QUESTIONS_PER_INTENT = 1000

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_PATH = BASE_DIR / "data" / "qa_contoh.json"
DATA_PATH = BASE_DIR / "data" / "qa.json"


def load_intents():
    with open(SOURCE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    intents = load_intents()
    dataset = []

    for intent in intents:
        templates = intent.get("templates", [])
        variants = intent.get("variants", [])
        answers = intent.get("answers", [])

        if not templates or not variants or not answers:
            continue

        combinations = list(itertools.product(templates, variants))
        random.shuffle(combinations)

        questions = []
        for t, v in combinations[:QUESTIONS_PER_INTENT]:
            q = t.format(v).strip().lower()
            questions.append(q)

        dataset.append({
            "intent": intent["intent"],
            "questions": questions,
            "answers": answers  # SIMPAN SEMUA JAWABAN
        })

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print("Dataset multi-jawaban berhasil dibuat")


if __name__ == "__main__":
    main()