from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import settings
from src.adapters.persistence.local_model_store import LocalModelStore
from src.adapters.nlp.sklearn_classifier import SklearnEmailClassifier
from src.adapters.reply.templates import TemplateReplyGenerator

from src.adapters.reply.gemini_reply import GeminiReplyGenerator

from src.interfaces.api.routes.email_routes import router
from src.use_cases.classify_email import ClassifyEmailUseCase

def create_app() -> FastAPI:
    app = FastAPI(title="Email Classifier API", version="0.1.0")

    import os
    
    allowed_origins = ["*"]
    if os.getenv("ENV") == "prod":
        allowed_origins = [
            "https://desafio-autou-up1n.onrender.com",
            "https://desafio-autou.onrender.com"
        ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    store = LocalModelStore()
    classifier = SklearnEmailClassifier(store)

    reply = GeminiReplyGenerator() if settings.AI_PROVIDER.lower() == "gemini" else TemplateReplyGenerator()

    uc = ClassifyEmailUseCase(classifier, reply)
    app.state.uc = uc

    from fastapi import Depends
    def get_uc():
        return app.state.uc

    for r in router.routes:
        r.dependant.dependencies.insert(0, Depends(get_uc))

    app.include_router(router, prefix="/api")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
