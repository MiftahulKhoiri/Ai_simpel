import json
from pathlib import Path

from core.backup import backup

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "qa.json"


def load_data():
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    backup()
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_qa(question: str, answer: str) -> bool:
    data = load_data()
    question = question.strip().lower()
    answer = answer.strip()

    # Cari intent dengan jawaban sama
    for item in data:
        answers = item.get("answers", [])

        # Normalisasi: pastikan answers selalu list
        if isinstance(answers, str):
            answers = [answers]
            item["answers"] = answers

        if answer in answers:
            if question in item["questions"]:
                return False
            item["questions"].append(question)
            save_data(data)
            return True

    # Jika belum ada, buat intent baru
    new_intent = {
        "intent": f"auto_{len(data) + 1}",
        "questions": [question],
        "answers": [answer]   # ⬅⬅⬅ WAJIB LIST
    }

    data.append(new_intent)
    save_data(data)
    return True