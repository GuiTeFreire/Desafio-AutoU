from dataclasses import dataclass
from src.adapters.nlp.preprocessing import is_toxic
from src.core.enums.category import Category
from src.core.entities.email import Email
from src.core.protocols.classifier import EmailClassifier
from src.core.protocols.reply_generator import ReplyGenerator

@dataclass
class ClassifyEmailInput:
    text: str

@dataclass
class ClassifyEmailOutput:
    category: str
    confidence: float
    suggested_reply: str
    classify_source: str
    reply_source: str | None = None


class ClassifyEmailUseCase:
    def __init__(self, classifier: EmailClassifier, reply: ReplyGenerator):
        self.classifier = classifier
        self.reply = reply

    def execute(self, inp: ClassifyEmailInput) -> ClassifyEmailOutput:
        text = inp.text
        print(f"Processando email: {text[:50]}...")
        
        # 1 guarda-chuva de segurança
        if is_toxic(text):
            print("Email detectado como tóxico")
            category = Category.IMPRODUTIVO
            confidence = 0.99
            suggested = self.reply.generate("Improdutivo", text)
            if hasattr(self.reply, "generate_subtype"):
                suggested = self.reply.generate_subtype("toxico", text)
            return ClassifyEmailOutput(
                category=category.value,
                confidence=confidence,
                suggested_reply=suggested,
                classify_source="rule:toxicity",
                reply_source=type(self.reply).__name__,
            )

        # 2 fluxo normal
        print("Classificando email com ML...")
        email = Email(text=text)
        category, confidence = self.classifier.predict(email)
        print(f"Classificação: {category.value} ({confidence:.3f})")
        
        suggested = self.reply.generate(category.value, text)
        print("Resposta gerada com sucesso")
        
        return ClassifyEmailOutput(
            category=category.value,
            confidence=round(confidence, 4),
            suggested_reply=suggested,
            classify_source=type(self.classifier).__name__,
            reply_source=type(self.reply).__name__,
        )
