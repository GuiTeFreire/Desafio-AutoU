import google.generativeai as genai
from typing import Optional
from config.settings import settings
from core.enums.category import Category

class GeminiReplyGenerator:
    def __init__(self):
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """Configura o cliente Gemini"""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não configurada. Defina a variável de ambiente.")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Usa modelo mais estável e disponível
        self.client = genai.GenerativeModel("gemini-1.5-flash")
    
    def _generate_classification_prompt(self, text: str) -> str:
        """Gera prompt para classificação do email"""
        return f"""
Analise o seguinte email e classifique-o como "Produtivo" ou "Improdutivo":

Email: "{text}"

Critérios:
- PRODUTIVO: Solicitações, problemas técnicos, pedidos de ajuda, atualizações de status, reset de senha, faturas, relatórios, etc.
- IMPRODUTIVO: Cumprimentos, agradecimentos genéricos, mensagens de felicitações, spam, etc.

Responda APENAS com: "Produtivo" ou "Improdutivo"
"""
    
    def _generate_reply_prompt(self, category: str, text: str) -> str:
        """Gera prompt para criação de resposta automática"""
        if category == Category.IMPRODUTIVO.value:
            return f"""
Email recebido: "{text}"

Este email foi classificado como IMPRODUTIVO (cumprimento/agradecimento genérico).

Gere uma resposta profissional e cordial, agradecendo e indicando que não há ação necessária.

Responda em português brasileiro, de forma concisa e profissional.
"""
        else:
            return f"""
Email recebido: "{text}"

Este email foi classificado como PRODUTIVO (solicitação que requer ação).

Analise o conteúdo e gere uma resposta automática profissional que:
1. Agradeça o contato
2. Confirme o recebimento da solicitação
3. Solicite informações adicionais se necessário
4. Indique próximos passos
5. Seja específica ao contexto da solicitação

Tipos comuns de solicitações:
- Status de chamado/ticket
- Reset de senha/acesso
- Fatura/segunda via
- Anexos/documentos
- Relatórios de erro
- Solicitações gerais

Responda em português brasileiro, de forma profissional e útil.
"""
    
    def classify_email(self, text: str) -> tuple[str, float]:
        """Classifica o email usando Gemini"""
        try:
            prompt = self._generate_classification_prompt(text)
            response = self.client.generate_content(prompt)
            
            result = response.text.strip().lower()
            confidence = 0.8  # Gemini não retorna confiança, usamos valor padrão
            
            if "produtivo" in result:
                return Category.PRODUTIVO.value, confidence
            else:
                return Category.IMPRODUTIVO.value, confidence
                
        except Exception as e:
            print(f"Erro na classificação Gemini: {e}")
            # Fallback para classificação baseada em palavras-chave
            return self._fallback_classification(text)
    
    def _fallback_classification(self, text: str) -> tuple[str, float]:
        """Classificação de fallback baseada em palavras-chave"""
        text_lower = text.lower()
        
        productive_keywords = [
            "preciso", "solicito", "problema", "erro", "bug", "senha", "reset",
            "acesso", "login", "fatura", "boleto", "pagamento", "chamado", "ticket",
            "status", "andamento", "anexo", "arquivo", "documento", "relatório"
        ]
        
        unproductive_keywords = [
            "obrigado", "obrigada", "parabéns", "feliz", "natal", "ano novo",
            "boas festas", "cumprimentos", "saudações"
        ]
        
        productive_score = sum(1 for word in productive_keywords if word in text_lower)
        unproductive_score = sum(1 for word in unproductive_keywords if word in text_lower)
        
        if productive_score > unproductive_score:
            return Category.PRODUTIVO.value, 0.6
        else:
            return Category.IMPRODUTIVO.value, 0.6
    
    def generate(self, category: str, original_text: str) -> str:
        """Gera resposta automática usando Gemini"""
        try:
            prompt = self._generate_reply_prompt(category, original_text)
            response = self.client.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Erro na geração de resposta Gemini: {e}")
            # Fallback para resposta genérica
            return self._fallback_reply(category)
    
    def _fallback_reply(self, category: str) -> str:
        """Resposta de fallback caso Gemini falhe"""
        if category == Category.IMPRODUTIVO.value:
            return "Obrigado pela mensagem! Não há ação necessária no momento. Permanecemos à disposição."
        else:
            return "Olá! Obrigado pelo contato. Recebemos sua solicitação e vamos analisar os detalhes. Em breve retornaremos com próximos passos."
