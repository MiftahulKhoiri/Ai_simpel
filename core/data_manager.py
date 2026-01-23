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
    """
    Tambahkan pertanyaan ke intent yang cocok.
    - Jika answer sudah ada → tambah ke questions
    - Jika belum → buat intent baru
    Return True jika data berubah
    """
    data = load_data()
    question = question.strip().lower()
    answer = answer.strip()

    # Cari intent dengan jawaban sama
    for item in data:
        if item.get("answer") == answer:
            if question in item.get("questions", []):
                return False  # sudah ada
            item["questions"].append(question)
            save_data(data)
            return True

    # Jika belum ada intent dengan jawaban ini
    new_intent = {
        "intent": f"auto_{len(data)+1}",
        "questions": [question],
        "answer": answer
    }

    data.append(new_intent)
    save_data(data)
    return True