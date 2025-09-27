from dataclasses import dataclass

@dataclass(frozen=True)
class Email:
    text: str
