from typing import Protocol, Tuple
from src.core.entities.email import Email
from src.core.enums.category import Category

class EmailClassifier(Protocol):
    def predict(self, email: Email) -> Tuple[Category, float]:
        """Retorna (categoria, confiança)."""
        ...
