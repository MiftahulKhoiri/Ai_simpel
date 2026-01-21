import sys
import os

from core.update import SelfUpdater
from core.nlp_engine import NLPEngine
from core.cms_logger import get_logger

log = get_logger("AI_MAIN")


def restart_program():
    log.warning("Restarting aplikasi...")
    os.execv(sys.executable, [sys.executable] + sys.argv)


def main():
    # ===== AUTO UPDATE =====
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    updater = SelfUpdater(repo_dir=repo_dir)

    if updater.update_if_needed():
        restart_program()

    # ===== AI ENGINE =====
    ai = NLPEngine()
    print("AI siap. Ketik 'exit' untuk keluar.")

    while True:
        text = input("Kamu: ").strip()
        if text.lower() == "exit":
            break

        jawab = ai.ask(text)
        print("AI:", jawab)


if __name__ == "__main__":
    main()