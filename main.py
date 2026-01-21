import os
import sys

from core.update import SelfUpdater
from core.bootstrap import bootstrap
from core.nlp_engine import NLPEngine
from core.data_manager import add_qa
from core.trainer import train
from core.cms_logger import get_logger

log = get_logger("AI_MAIN")


def restart_program():
    os.execv(sys.executable, [sys.executable] + sys.argv)


def main():
    bootstrap()
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    updater = SelfUpdater(repo_dir=repo_dir)

    if updater.update_if_needed():
        restart_program()

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

        # ===== AI TIDAK TAHU =====
        print("AI: Maaf, saya belum tahu jawabannya.")
        confirm = input("Apakah Anda mau memberikan jawabannya? (y/n): ").strip().lower()

        if confirm != "y":
            continue

        user_answer = input("Silakan masukkan jawabannya: ").strip()

        if add_qa(question.lower(), user_answer):
            print("AI: Terima kasih, saya akan mengingatnya.")
            print("AI: Melatih ulang model...")

            train()
            ai = NLPEngine()  # reload model

            print("AI: Saya sudah belajar jawaban baru.")
        else:
            print("AI: Pertanyaan tersebut sudah ada sebelumnya.")


if __name__ == "__main__":
    main()