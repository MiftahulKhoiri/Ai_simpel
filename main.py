from core.nlp_engine import NLPEngine

def main():
    ai = NLPEngine()
    print("AI Siap. Ketik 'exit' untuk keluar.")

    while True:
        text = input("Kamu: ")
        if text.lower() == "exit":
            break
        print("AI:", ai.ask(text))

if __name__ == "__main__":
    main()