import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

_factory = StemmerFactory()
_stemmer = _factory.create_stemmer()


def preprocess_text(text: str) -> str:
    """
    - lowercase
    - hapus karakter non-huruf
    - stemming Bahasa Indonesia
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return _stemmer.stem(text)