import random
from collections import defaultdict

class TextGenerator:
    def __init__(self, texts):
        self.model = defaultdict(list)
        self.build_model(texts)

    def build_model(self, texts):
        for text in texts:
            words = text.lower().split()
            for i in range(len(words) - 1):
                self.model[words[i]].append(words[i + 1])

    def generate(self, seed, max_words=20):
        words = seed.lower().split()
        if not words:
            return ""

        current = words[-1]
        result = words.copy()

        for _ in range(max_words):
            next_words = self.model.get(current)
            if not next_words:
                break
            current = random.choice(next_words)
            result.append(current)

        return " ".join(result)