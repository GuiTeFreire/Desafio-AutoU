from typing import Protocol, Tuple
from core.entities.email import Email
from core.enums.category import Category

class EmailClassifier(Protocol):
    def predict(self, email: Email) -> Tuple[Category, float]:
        """Retorna (categoria, confiança)."""
        ...
