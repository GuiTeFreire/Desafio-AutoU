# AutoU Email Classifier

Sistema de classificação automática de emails usando Machine Learning e APIs de IA.

## 🚀 Como Executar

### Opção 1: Modo Desenvolvimento (com reload automático)

```bash
python start.py
```

### Opção 2: Modo Produção

```bash
python main.py
```

### Opção 3: Usando uvicorn diretamente

```bash
uvicorn src.interfaces.api.app_factory:create_app --factory --reload --host 127.0.0.1 --port 8000
```

## 📡 Endpoints

- **Health Check**: `GET /health`
- **Documentação**: `GET /docs` (Swagger UI)
- **Classificar Email**: `POST /api/process_email`

## 🔧 Configuração

### Variáveis de Ambiente

Copie o arquivo `env.example` para `.env` e configure:

```bash
cp env.example .env
```

**Configurações principais:**

- `ENV`: Ambiente (dev/prod)
- `MODEL_DIR`: Diretório dos modelos
- `AI_PROVIDER`: Provedor de IA (template/gemini/openai)
- `GEMINI_API_KEY`: Chave da API Gemini
- `OPENAI_API_KEY`: Chave da API OpenAI (opcional)
- `CLASSIFY_CONF_THRESHOLD`: Threshold de confiança (0.65)

### 🤖 Usando Gemini

1. **Obtenha uma API key do Gemini:**

   - Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Crie uma nova API key

2. **Configure o .env:**

   ```env
   AI_PROVIDER=gemini
   GEMINI_API_KEY=sua_chave_aqui
   GEMINI_MODEL=gemini-1.5-flash
   ```

3. **Execute o projeto:**
   ```bash
   python main.py
   ```

### 📝 Modo Template (Padrão)

Se não configurar uma API key, o sistema usará templates inteligentes baseados em palavras-chave.

## 📦 Dependências

Todas as dependências estão listadas em `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 🏗️ Estrutura do Projeto

```
src/
├── adapters/          # Adaptadores externos
│   ├── nlp/          # Processamento de linguagem natural
│   ├── parsers/      # Parsers de arquivos
│   ├── persistence/  # Armazenamento de modelos
│   └── reply/        # Geradores de resposta
├── config/           # Configurações
├── core/             # Entidades e protocolos
├── interfaces/       # API e schemas
└── use_cases/        # Casos de uso
```

## 🧪 Testando a API

### Health Check

```bash
curl http://localhost:8000/health
```

### Classificar Email

```bash
curl -X POST "http://localhost:8000/api/process_email" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Preciso de ajuda com o sistema"
```

### Upload de Arquivo

```bash
curl -X POST "http://localhost:8000/api/process_email" \
     -F "file=@email.txt"
```

### Teste Local

```bash
python test_gemini.py
```

### Exemplo de Resposta

```json
{
  "category": "Produtivo",
  "confidence": 0.8542,
  "suggested_reply": "Olá! Obrigado pela mensagem. Para apoiar no acesso, confirme usuário/login e, se houver, o erro exibido. Daremos sequência ao reset.",
  "classify_source": "SklearnEmailClassifier"
}
```
