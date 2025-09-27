from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "dev"
    MODEL_DIR: str = "model_artifacts"
    MODEL_FILE: str = "clf_nb_tfidf.pkl"

    # IA externa (opcional)
    AI_PROVIDER: str = "template"  # template | gemini | openai
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-1.5-flash"

    CLASSIFY_CONF_THRESHOLD: float = 0.65

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
