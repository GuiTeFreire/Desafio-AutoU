import re
import nltk
from nltk.corpus import stopwords

try:
    STOPWORDS_PT = set(stopwords.words("portuguese"))
except LookupError:
    nltk.download("stopwords")
    STOPWORDS_PT = set(stopwords.words("portuguese"))

def clean_text(text: str) -> str:
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ0-9@.,!? ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocess(text: str) -> str:
    text = clean_text(text).lower()
    tokens = [t for t in text.split() if t not in STOPWORDS_PT]
    return " ".join(tokens)
