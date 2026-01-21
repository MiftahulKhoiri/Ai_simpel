from core.nlp_engine import NLPEngine
from core.data_manager import add_qa
from core.trainer import train

def main():
    ai = NLPEngine()
    print("AI siap. Ketik 'exit' untuk keluar.")

    while True:
        question = input("Kamu: ").strip()
        if question.lower() == "exit":
            break

        answer, score = ai.ask_with_score(question)

        if answer:
            print("AI:", answer)
            continue

        print("AI: Maaf, saya belum tahu jawabannya.")
        confirm = input("Apakah Anda mau memberikan jawabannya? (y/n): ").strip().lower()

        if confirm != "y":
            continue

        user_answer = input("Silakan masukkan jawabannya: ").strip()

        if add_qa(question.lower(), user_answer):
            print("AI: Terima kasih, saya akan mengingatnya.")
            print("AI: Melatih ulang model...")

            train()
            ai = NLPEngine()

            print("AI: Saya sudah belajar jawaban baru.")
        else:
            print("AI: Pertanyaan tersebut sudah ada.")

if __name__ == "__main__":
    main()