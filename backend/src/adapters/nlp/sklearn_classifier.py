from typing import Tuple
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from src.core.entities.email import Email
from src.core.enums.category import Category
from src.core.protocols.model_store import ModelStore
from src.adapters.nlp.preprocessing import preprocess

# dataset semente para inicializar
SEED = [
    ("Preciso de atualização do chamado", Category.PRODUTIVO),
    ("Poderiam resetar minha senha", Category.PRODUTIVO),
    ("Segue em anexo o relatório solicitado.", Category.PRODUTIVO),
    ("eu te odeio", Category.IMPRODUTIVO),
    ("seu atendimento é uma merda", Category.IMPRODUTIVO),
    ("vocês são uns idiotas", Category.IMPRODUTIVO),
    ("vai se ferrar", Category.IMPRODUTIVO),
    ("lixo de empresa", Category.IMPRODUTIVO),
    ("obrigado!", Category.IMPRODUTIVO),
    ("feliz natal", Category.IMPRODUTIVO),
]

class SklearnEmailClassifier:
    def __init__(self, store: ModelStore):
        self.store = store
        self.pipe: Pipeline | None = None
        self._load_or_train()

    def _build(self) -> Pipeline:
        return Pipeline([
            ("tfidf", TfidfVectorizer(preprocessor=preprocess, ngram_range=(1,2), min_df=1)),
            ("clf", MultinomialNB()),
        ])

    def _load_or_train(self):
        obj = self.store.load()
        if obj is not None:
            self.pipe = obj
            return
        # treino inicial
        X = [t for t, _ in SEED]
        y = [c.value for _, c in SEED]
        pipe = self._build()
        pipe.fit(X, y)
        self.store.save(pipe)
        self.pipe = pipe

    def predict(self, email: Email) -> Tuple[Category, float]:
        proba = self.pipe.predict_proba([email.text])[0]
        classes = self.pipe.classes_
        idx = proba.argmax()
        return Category(classes[idx]), float(proba[idx])
