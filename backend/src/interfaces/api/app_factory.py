from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from adapters.persistence.local_model_store import LocalModelStore
from adapters.nlp.sklearn_classifier import SklearnEmailClassifier
from adapters.reply.templates import TemplateReplyGenerator
from adapters.reply.gemini_reply import GeminiReplyGenerator
from interfaces.api.routes.email_routes import router
from use_cases.classify_email import ClassifyEmailUseCase
from config.settings import settings

def create_app() -> FastAPI:
    app = FastAPI(title="Email Classifier API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # composição/DI
    store = LocalModelStore()
    classifier = SklearnEmailClassifier(store)
    
    # Seleciona o gerador de resposta baseado na configuração
    if settings.AI_PROVIDER == "gemini" and settings.GEMINI_API_KEY:
        try:
            reply = GeminiReplyGenerator()
            print("🤖 Usando Gemini para geração de respostas")
        except Exception as e:
            print(f"⚠️ Erro ao inicializar Gemini: {e}")
            print("📝 Fallback para templates")
            reply = TemplateReplyGenerator()
    else:
        reply = TemplateReplyGenerator()
        print("📝 Usando templates para geração de respostas")
    
    uc = ClassifyEmailUseCase(classifier, reply)

    # dependency injection simples via state
    app.state.uc = uc

    # wire das rotas com dependência
    from fastapi import Depends

    def get_uc():
        return app.state.uc

    router.dependency_overrides = {}
    # injeta UC na rota
    from fastapi import APIRouter
    api = APIRouter()
    @api.post("/process_email", response_model=None, include_in_schema=False)
    async def _bind():
        # placeholder para documentação
        pass
    # substitui factory dependency diretamente no router:
    for r in router.routes:
        r.dependant.dependencies.insert(0, Depends(get_uc))

    app.include_router(router, prefix="/api")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

# uvicorn --factory src.interfaces.api.app_factory:create_app --reload
