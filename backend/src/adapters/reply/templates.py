from core.enums.category import Category

def detect_subtype(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["status", "andamento", "ticket", "chamado"]):
        return "status"
    if any(k in t for k in ["senha", "reset", "acesso", "login"]):
        return "senha"
    if any(k in t for k in ["fatura", "boleto", "cobrança", "pagamento", "segunda via", "2ª via"]):
        return "fatura"
    if any(k in t for k in ["anexo", "arquivo", "documento"]):
        return "anexo"
    if any(k in t for k in ["erro", "bug", "falha"]):
        return "erro"
    return "geral"

TEMPLATES = {
    "status": "Olá! Obrigado pelo contato. Estamos verificando o status da sua solicitação e retornaremos em breve. Se tiver número do chamado, por favor informe.",
    "senha": "Olá! Obrigado pela mensagem. Para apoiar no acesso, confirme usuário/login e, se houver, o erro exibido. Daremos sequência ao reset.",
    "fatura": "Olá! Obrigado pelo contato. Encaminharemos a fatura/2ª via. Confirme o número do contrato/conta e o período desejado.",
    "anexo": "Olá! Recebemos o arquivo e vamos analisar os detalhes. Se houver pendências, retornaremos solicitando informações complementares.",
    "erro": "Olá! Obrigado por reportar. Estamos avaliando o comportamento informado e retornamos com orientação ou correção.",
    "geral": "Olá! Obrigado pelo contato. Recebemos sua solicitação e vamos analisar os detalhes. Em breve retornaremos com próximos passos.",
}

class TemplateReplyGenerator:
    def generate(self, category: str, original_text: str) -> str:
        if category == Category.IMPRODUTIVO.value:
            return "Obrigado pela mensagem! Não há ação necessária no momento. Permanecemos à disposição."
        subtype = detect_subtype(original_text)
        return TEMPLATES.get(subtype, TEMPLATES["geral"])
