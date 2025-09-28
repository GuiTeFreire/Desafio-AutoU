import os
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# carrega .env (se ainda não estiver carregado no shell)
load_dotenv(find_dotenv())

# configure a API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Listando modelos disponíveis para esta chave:\n")
for model in genai.list_models():
    print("-", model.name)
