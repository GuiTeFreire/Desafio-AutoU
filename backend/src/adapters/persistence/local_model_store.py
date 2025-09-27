from pathlib import Path
import pickle
from typing import Any
from config.settings import settings

class LocalModelStore:
    def __init__(self, model_dir: str | None = None, model_file: str | None = None):
        self.dir = Path(model_dir or settings.MODEL_DIR)
        self.path = self.dir / (model_file or settings.MODEL_FILE)
        self.dir.mkdir(exist_ok=True)

    def save(self, obj: Any) -> None:
        with open(self.path, "wb") as f:
            pickle.dump(obj, f)

    def load(self) -> Any | None:
        if not self.path.exists():
            return None
        with open(self.path, "rb") as f:
            return pickle.load(f)
