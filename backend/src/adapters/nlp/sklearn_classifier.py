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
    # Emails produtivos - solicitações, problemas, suporte
    ("Preciso de atualização do chamado", Category.PRODUTIVO),
    ("Poderiam resetar minha senha", Category.PRODUTIVO),
    ("Segue em anexo o relatório solicitado", Category.PRODUTIVO),
    ("Estou enfrentando problemas com o sistema", Category.PRODUTIVO),
    ("Preciso de ajuda urgente", Category.PRODUTIVO),
    ("Solicitação de suporte técnico", Category.PRODUTIVO),
    ("Problema com pagamentos", Category.PRODUTIVO),
    ("Erro no sistema de login", Category.PRODUTIVO),
    ("Status do projeto", Category.PRODUTIVO),
    ("Relatório mensal", Category.PRODUTIVO),
    ("Problema com transação", Category.PRODUTIVO),
    ("Solicitação de informações", Category.PRODUTIVO),
    ("Bug no aplicativo", Category.PRODUTIVO),
    ("Atualização de dados", Category.PRODUTIVO),
    ("Consulta sobre faturamento", Category.PRODUTIVO),
    
    # Emails improdutivos - sociais, ofensivos, não relacionados
    ("eu te odeio", Category.IMPRODUTIVO),
    ("seu atendimento é uma porcaria", Category.IMPRODUTIVO),
    ("vocês são uns idiotas", Category.IMPRODUTIVO),
    ("vai se ferrar", Category.IMPRODUTIVO),
    ("lixo de empresa", Category.IMPRODUTIVO),
    ("obrigado!", Category.IMPRODUTIVO),
    ("feliz natal", Category.IMPRODUTIVO),
    ("feliz aniversário", Category.IMPRODUTIVO),
    ("bom dia pessoal", Category.IMPRODUTIVO),
    ("como vocês estão", Category.IMPRODUTIVO),
    ("parabéns pelo trabalho", Category.IMPRODUTIVO),
    ("vamos almoçar juntos", Category.IMPRODUTIVO),
    ("fim de semana bom", Category.IMPRODUTIVO),
    ("conversa de corredor", Category.IMPRODUTIVO),
    ("mensagem de cumprimento", Category.IMPRODUTIVO),
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
        try:
            obj = self.store.load()
            if obj is not None:
                self.pipe = obj
                print("Modelo carregado com sucesso")
                return
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
        
        # treino inicial
        try:
            print("Iniciando treinamento do modelo...")
            X = [t for t, _ in SEED]
            y = [c.value for _, c in SEED]
            pipe = self._build()
            pipe.fit(X, y)
            self.store.save(pipe)
            self.pipe = pipe
            print("Modelo treinado e salvo com sucesso")
        except Exception as e:
            print(f"Erro no treinamento: {e}")
            # Fallback: modelo em memória sem salvar
            X = [t for t, _ in SEED]
            y = [c.value for _, c in SEED]
            pipe = self._build()
            pipe.fit(X, y)
            self.pipe = pipe
            print("Modelo treinado em memória (não salvo)")

    def predict(self, email: Email) -> Tuple[Category, float]:
        try:
            print(f"Predicting for: '{email.text[:50]}...'")
            if self.pipe is None:
                print("Pipeline is None!")
                return Category.IMPRODUTIVO, 0.5
            
            proba = self.pipe.predict_proba([email.text])[0]
            classes = self.pipe.classes_
            idx = proba.argmax()
            result = Category(classes[idx]), float(proba[idx])
            print(f"Prediction result: {result}")
            return result
        except Exception as e:
            print(f"Erro na predição: {e}")
            return Category.IMPRODUTIVO, 0.5
