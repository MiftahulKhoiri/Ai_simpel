import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FAILED_PATH = BASE_DIR / "data" / "failed_questions.json"


def log_failed_question(question: str, score: float):
    """
    Catat pertanyaan yang gagal dijawab AI.
    Tidak duplikat, disimpan permanen.
    """
    question = question.strip().lower()

    if not FAILED_PATH.exists():
        data = []
    else:
        with open(FAILED_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

    # Cegah duplikat
    for item in data:
        if item["question"] == question:
            return

    data.append({
        "question": question,
        "confidence": round(score, 3),
        "first_seen": datetime.now().isoformat()
    })

    with open(FAILED_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)