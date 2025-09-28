"""
Ponto de entrada principal para a API de classificação de emails.
"""
import sys
from pathlib import Path

from src.interfaces.api.app_factory import create_app

# Adiciona o diretório src ao Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    import uvicorn
    
    app = create_app()
    
    print("🚀 Iniciando servidor AutoU Email Classifier...")
    print("📧 API disponível em: http://localhost:8000")
    print("📖 Documentação em: http://localhost:8000/docs")
    print("🔍 Health check em: http://localhost:8000/health")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )
