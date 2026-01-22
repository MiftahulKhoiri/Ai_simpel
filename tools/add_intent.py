import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "qa.json"


def load_data():
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    data = load_data()

    intent = input("Intent: ").strip()
    answer = input("Jawaban: ").strip()

    questions = []
    print("Masukkan pertanyaan (kosongkan untuk selesai):")
    while True:
        q = input("- ").strip()
        if not q:
            break
        questions.append(q)

    if not questions:
        print("Tidak ada pertanyaan, dibatalkan.")
        return

    data.append({
        "intent": intent,
        "questions": questions,
        "answer": answer
    })

    save_data(data)
    print("Data intent berhasil ditambahkan.")
    print("Jalankan trainer untuk update model.")


if __name__ == "__main__":
    main()