import json
from core.trainer import train
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "qa.json"



def load_data():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    data = load_data()

    question = input("Pertanyaan: ").strip().lower()
    answer = input("Jawaban   : ").strip()

    for item in data:
        if item["question"] == question:
            print("Pertanyaan sudah ada, dibatalkan.")
            return

    data.append({
        "question": question,
        "answer": answer
    })

    save_data(data)
    print("Data ditambahkan, training ulang...")

    train()
    print("Selesai.")


if __name__ == "__main__":
    main()