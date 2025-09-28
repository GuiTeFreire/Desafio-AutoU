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
    ("Não consigo acessar minha conta", Category.PRODUTIVO),
    ("O boleto não chegou", Category.PRODUTIVO),
    ("Quando sai a segunda via da fatura", Category.PRODUTIVO),
    ("Meu cartão foi bloqueado", Category.PRODUTIVO),
    ("Preciso cancelar uma transação", Category.PRODUTIVO),
    ("Como altero meus dados cadastrais", Category.PRODUTIVO),
    ("O sistema está lento hoje", Category.PRODUTIVO),
    ("Não recebi o comprovante por email", Category.PRODUTIVO),
    ("Preciso de uma declaração de imposto de renda", Category.PRODUTIVO),
    ("Minha transferência não foi processada", Category.PRODUTIVO),
    ("O aplicativo está travando", Category.PRODUTIVO),
    ("Preciso falar com um gerente", Category.PRODUTIVO),
    ("Meu limite foi reduzido sem aviso", Category.PRODUTIVO),
    ("Como faço para contestar uma cobrança", Category.PRODUTIVO),
    ("Não consigo fazer PIX", Category.PRODUTIVO),
    ("Preciso de ajuda com o internet banking", Category.PRODUTIVO),
    ("Minha conta foi debitada indevidamente", Category.PRODUTIVO),
    ("O atendimento presencial está funcionando", Category.PRODUTIVO),
    ("Preciso de orientação sobre investimentos", Category.PRODUTIVO),
    ("Como solicito um empréstimo", Category.PRODUTIVO),
    
    # Emails improdutivos - sociais, ofensivos, não relacionados
    ("eu te odeio", Category.IMPRODUTIVO),
    ("seu atendimento é uma porcaria", Category.IMPRODUTIVO),
    ("vocês são uns idiotas", Category.IMPRODUTIVO),
    ("vai se ferrer", Category.IMPRODUTIVO),
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
    ("oi tudo bem", Category.IMPRODUTIVO),
    ("que calor hoje", Category.IMPRODUTIVO),
    ("viu o jogo ontem", Category.IMPRODUTIVO),
    ("bom final de semana", Category.IMPRODUTIVO),
    ("feliz dia das mães", Category.IMPRODUTIVO),
    ("parabéns pela promoção", Category.IMPRODUTIVO),
    ("adoro trabalhar aqui", Category.IMPRODUTIVO),
    ("vocês são demais", Category.IMPRODUTIVO),
    ("que equipe incrível", Category.IMPRODUTIVO),
    ("até segunda pessoal", Category.IMPRODUTIVO),
    ("boa sorte na apresentação", Category.IMPRODUTIVO),
    ("muito obrigado por tudo", Category.IMPRODUTIVO),
    ("adorei a festa de ontem", Category.IMPRODUTIVO),
    ("vamos tomar um café", Category.IMPRODUTIVO),
    ("que dia lindo hoje", Category.IMPRODUTIVO),
    ("estou de férias na praia", Category.IMPRODUTIVO),
    ("minha filha nasceu", Category.IMPRODUTIVO),
    ("comprei um carro novo", Category.IMPRODUTIVO),
    ("vou me casar mês que vem", Category.IMPRODUTIVO),
    ("ganhei na loteria", Category.IMPRODUTIVO),
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
        print("Iniciando treinamento do modelo...")
        # Sempre treinar em memória para evitar problemas de arquivo
        X = [t for t, _ in SEED]
        y = [c.value for _, c in SEED]
        pipe = self._build()
        pipe.fit(X, y)
        self.pipe = pipe
        print("Modelo treinado em memória com sucesso")

    def predict(self, email: Email) -> Tuple[Category, float]:
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
