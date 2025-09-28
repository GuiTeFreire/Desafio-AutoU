import sys
from pathlib import Path

from src.interfaces.api.app_factory import create_app

src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    import uvicorn
    
    app = create_app()
    
    print("🚀 Iniciando servidor AutoU Email Classifier...")
    print("📧 API disponível em: http://localhost:8000")
    print("📖 Documentação em: http://localhost:8000/docs")
    print("🔍 Health check em: http://localhost:8000/health")
    
    import os
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
