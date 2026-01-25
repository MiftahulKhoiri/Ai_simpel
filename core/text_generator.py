import random
from collections import defaultdict


class TextGenerator:
    """
    Generator teks sederhana berbasis Markov Chain (bigram).
    Digunakan sebagai fallback jika QA tidak menemukan jawaban.
    """

    def __init__(self, texts: list[str]):
        self.model = defaultdict(list)
        self.build_model(texts)

    def build_model(self, texts: list[str]):
        for text in texts:
            words = text.lower().split()
            for i in range(len(words) - 1):
                self.model[words[i]].append(words[i + 1])

    def generate(self, seed: str, max_words: int = 20) -> str | None:
        words = seed.lower().split()
        if not words:
            return None

        current = words[-1]
        result = words.copy()

        for _ in range(max_words):
            next_words = self.model.get(current)
            if not next_words:
                break
            current = random.choice(next_words)
            result.append(current)

        return " ".join(result)