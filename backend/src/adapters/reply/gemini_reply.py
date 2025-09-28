# src/adapters/reply/gemini_reply.py
import os
import json
import logging
import google.generativeai as genai
from google.generativeai import GenerativeModel
from dotenv import load_dotenv, find_dotenv

# garante que o .env foi lido (também no subprocess do uvicorn --reload)
load_dotenv(find_dotenv())

logger = logging.getLogger("gemini_reply")
logger.setLevel(logging.INFO)

PREFERRED = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro-latest",
]

def _normalize_name(name: str) -> str:
    return (name or "").strip().replace("models/", "")

def _supports_generate_content(model) -> bool:
    methods = getattr(model, "supported_generation_methods", None)
    if isinstance(methods, (list, tuple, set)):
        return "generateContent" in methods or "generate_content" in methods
    return True

def _configure_gemini():
    # aceita GEMINI_API_KEY ou GOOGLE_API_KEY
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY/GOOGLE_API_KEY ausente no ambiente (.env).")
    genai.configure(api_key=api_key)

def _resolve_gemini_model_name() -> str:
    _configure_gemini()
    desired = _normalize_name(os.getenv("GEMINI_MODEL", "").strip())

    available = list(genai.list_models())
    names = {_normalize_name(m.name): m for m in available}

    if desired:
        m = names.get(desired)
        if m and _supports_generate_content(m):
            logger.info(f"✔ Usando modelo Gemini configurado: {desired}")
            return desired
        if not m and desired.endswith("-flash"):
            alt = desired + "-latest"
            if alt in names and _supports_generate_content(names[alt]):
                logger.info(f"⚠ Modelo {desired} não encontrado; usando {alt}")
                return alt
        logger.warning(f"⚠ Modelo {desired} não suportado; tentando fallback.")

    for cand in PREFERRED:
        if cand in names and _supports_generate_content(names[cand]):
            logger.info(f"✔ Usando modelo Gemini fallback: {cand}")
            return cand

    for m in available:
        n = _normalize_name(m.name)
        if _supports_generate_content(m):
            logger.info(f"✔ Usando primeiro modelo válido encontrado: {n}")
            return n

    raise RuntimeError("Nenhum modelo Gemini disponível com generateContent.")

def _gemini_model() -> GenerativeModel:
    model_name = _resolve_gemini_model_name()
    return GenerativeModel(model_name)

class GeminiReplyGenerator:
    def __init__(self):
        self._model = None

    def _model_instance(self) -> GenerativeModel:
        if self._model is None:
            self._model = _gemini_model()
        return self._model

    def generate(self, category: str, original_text: str) -> str:
        prompt = (
            "Você é um assistente de atendimento de uma empresa do setor financeiro.\n"
            f"Classificação do email: {category}.\n"
            "Escreva uma resposta breve, clara e cordial em PT-BR, com tom profissional.\n"
            "Se for Produtivo, agradeça, diga que analisará/atualizará o status e peça informações extras.\n"
            "Se for Improdutivo, agradeça e diga que não há ação necessária.\n\n"
            f"Email original (resuma discretamente, NÃO copie tudo):\n{original_text[:1200]}"
        )
        resp = self._model_instance().generate_content(prompt)
        return (resp.text or "").strip()

    def classify(self, raw_text: str) -> tuple[str, float]:
        prompt = (
            "Classifique o email como \"Produtivo\" ou \"Improdutivo\" e retorne JSON:\n"
            "{\"category\":\"Produtivo|Improdutivo\",\"confidence\":0.xx}\n\n"
            f"Email:\n{raw_text[:3000]}"
        )
        resp = self._model_instance().generate_content(prompt)
        out = resp.text or ""
        try:
            data = json.loads(out)
            cat = data.get("category", "").strip()
            conf = float(data.get("confidence", 0.65))
            if cat not in ("Produtivo", "Improdutivo"):
                raise ValueError
            return cat, max(0.0, min(conf, 1.0))
        except Exception:
            logger.warning("⚠ JSON inválido do Gemini; usando heurística simples.")
            t = raw_text.lower()
            cat = "Produtivo" if any(k in t for k in ["status","ticket","senha","fatura","erro","anexo","suporte"]) else "Improdutivo"
            return cat, 0.65
