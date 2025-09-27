from dataclasses import dataclass
from core.entities.email import Email
from core.protocols.classifier import EmailClassifier
from core.protocols.reply_generator import ReplyGenerator

@dataclass
class ClassifyEmailInput:
    text: str

@dataclass
class ClassifyEmailOutput:
    category: str
    confidence: float
    suggested_reply: str
    classify_source: str

class ClassifyEmailUseCase:
    def __init__(self, classifier: EmailClassifier, reply: ReplyGenerator):
        self.classifier = classifier
        self.reply = reply

    def execute(self, inp: ClassifyEmailInput) -> ClassifyEmailOutput:
        email = Email(text=inp.text)
        category, confidence = self.classifier.predict(email)
        suggested = self.reply.generate(category.value, inp.text)
        return ClassifyEmailOutput(
            category=category.value,
            confidence=round(confidence, 4),
            suggested_reply=suggested,
            classify_source=type(self.classifier).__name__,
        )
