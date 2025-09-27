from typing import Protocol

class ReplyGenerator(Protocol):
    def generate(self, category: str, original_text: str) -> str:
        ...
