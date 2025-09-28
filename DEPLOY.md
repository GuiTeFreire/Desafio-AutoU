# Deploy no Render

## Configuração Automática

O projeto está configurado para deploy automático no Render através do arquivo `render.yaml`.

### Serviços Configurados:

1. **Backend API** (`autou-backend`)

   - Tipo: Web Service
   - Runtime: Python
   - Build: `pip install -r requirements.txt`
   - Start: `python main.py`
   - Health Check: `/health`

2. **Frontend** (`autou-frontend`)
   - Tipo: Static Site
   - Build: `npm install && npm run build`
   - Publish: `./dist`

### Variáveis de Ambiente:

**Backend:**

- `ENV=prod`
- `AI_PROVIDER=template`
- `GEMINI_API_KEY` (opcional, para usar Gemini)

**Frontend:**

- `VITE_API_URL=https://desafio-autou-back-fxvg.onrender.com`

### Como Fazer Deploy:

1. **Serviços já configurados:**

   - Backend: `desafio-autou-back`
   - Frontend: `desafio-autou`
   - URLs já funcionais

2. **Deploy automático:**

   - A cada commit na branch `main`, o deploy será executado automaticamente
   - O backend será deployado primeiro
   - O frontend será deployado com a URL do backend

3. **Configuração de variáveis:**
   - No dashboard do Render, configure `ENV=prod` no backend
   - Para usar Gemini, adicione `GEMINI_API_KEY` no backend

### URLs de Produção:

- **Backend:** `https://desafio-autou-back-fxvg.onrender.com`
- **Frontend:** `https://desafio-autou-up1n.onrender.com`
- **API Docs:** `https://desafio-autou-back-fxvg.onrender.com/docs`

### Monitoramento:

- Health checks automáticos
- Logs disponíveis no dashboard
- Métricas de performance
- Alertas de downtime

### Troubleshooting:

1. **Backend não inicia:**

   - Verifique os logs no dashboard
   - Confirme se todas as dependências estão no `requirements.txt`

2. **Frontend não carrega:**

   - Verifique se `VITE_API_URL` está correto
   - Confirme se o build foi executado com sucesso

3. **CORS errors:**
   - Verifique se as URLs estão corretas no `app_factory.py`
   - Confirme se o frontend está acessando a URL correta do backend
