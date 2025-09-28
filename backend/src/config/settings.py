from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "dev"
    MODEL_DIR: str = "model_artifacts"
    MODEL_FILE: str = "clf_nb_tfidf.pkl"

    AI_PROVIDER: str = "template"  # template | gemini

    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    GEMINI_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    CLASSIFY_CONF_THRESHOLD: float = 0.65

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
print(f"Settings carregadas - AI_PROVIDER: '{settings.AI_PROVIDER}', ENV: '{settings.ENV}'")
print(f"AI_PROVIDER type: {type(settings.AI_PROVIDER)}")
print(f"AI_PROVIDER repr: {repr(settings.AI_PROVIDER)}")
