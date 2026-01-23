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

    for item in data:
        if item["question"] == question:
            return False  # duplikat

    data.append({
        "question": question,
        "answer": answer
    })

    save_data(data)
    return True