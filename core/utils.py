import re
from pathlib import Path
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# ===== STEMMER =====
_factory = StemmerFactory()
_stemmer = _factory.create_stemmer()

# ===== STOPWORDS =====
BASE_DIR = Path(__file__).resolve().parent.parent
STOPWORDS_PATH = BASE_DIR / "data" / "stopwords_id.txt"

def _load_stopwords():
    try:
        with open(STOPWORDS_PATH, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

_STOPWORDS = _load_stopwords()


def preprocess_text(text: str) -> str:
    """
    Pipeline:
    - lowercase
    - hapus karakter non-huruf
    - stemming Bahasa Indonesia
    - stopword removal
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    # stemming
    text = _stemmer.stem(text)

    # stopword removal
    tokens = [t for t in text.split() if t not in _STOPWORDS]

    return " ".join(tokens)