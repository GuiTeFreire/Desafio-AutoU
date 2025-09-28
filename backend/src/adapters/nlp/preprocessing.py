import re

# Stopwords em português hardcoded para evitar download no Render
STOPWORDS_PT = {
    'a', 'ao', 'aos', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo', 'as', 'até', 'com', 'como', 'da', 'das', 'do', 'dos', 'e', 'ela', 'elas', 'ele', 'eles', 'em', 'entre', 'era', 'eram', 'essa', 'essas', 'esse', 'esses', 'esta', 'estamos', 'estas', 'estava', 'estavam', 'este', 'esteja', 'estejam', 'estejamos', 'estes', 'esteve', 'estive', 'estivemos', 'estiver', 'estivera', 'estiveram', 'estiverem', 'estivermos', 'estivesse', 'estivessem', 'estivéramos', 'estivéssemos', 'estou', 'está', 'estão', 'eu', 'foi', 'fomos', 'for', 'fora', 'foram', 'forem', 'formos', 'fosse', 'fossem', 'fui', 'fôramos', 'fôssemos', 'haja', 'hajam', 'hajamos', 'havemos', 'havia', 'hei', 'houve', 'houvemos', 'houver', 'houvera', 'houveram', 'houverei', 'houverem', 'houveremos', 'houveria', 'houveriam', 'houveríamos', 'houverão', 'houverá', 'houveríamos', 'houvesse', 'houvessem', 'houvéramos', 'houvéssemos', 'há', 'hão', 'isso', 'isto', 'já', 'lhe', 'lhes', 'mais', 'mas', 'me', 'mesmo', 'meu', 'meus', 'minha', 'minhas', 'muito', 'na', 'nas', 'nem', 'no', 'nos', 'nossa', 'nossas', 'nosso', 'nossos', 'num', 'numa', 'não', 'nós', 'o', 'os', 'ou', 'para', 'pela', 'pelas', 'pelo', 'pelos', 'por', 'qual', 'quando', 'que', 'quem', 'se', 'seja', 'sejam', 'sejamos', 'sem', 'ser', 'seria', 'seriam', 'será', 'serão', 'seríamos', 'seu', 'seus', 'sua', 'suas', 'são', 'só', 'sua', 'suas', 'também', 'te', 'tem', 'temos', 'tenha', 'tenham', 'tenhamos', 'tenho', 'ter', 'terei', 'teremos', 'teria', 'teriam', 'terá', 'terão', 'teríamos', 'teve', 'tinha', 'tinham', 'tive', 'tivemos', 'tiver', 'tivera', 'tiveram', 'tiverem', 'tivermos', 'tivesse', 'tivessem', 'tivéramos', 'tivéssemos', 'tu', 'tua', 'tuas', 'tém', 'tínhamos', 'um', 'uma', 'você', 'vocês', 'vos', 'à', 'às', 'éramos'
}

def clean_text(text: str) -> str:
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ0-9@.,!? ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocess(text: str) -> str:
    try:
        text = clean_text(text).lower()
        tokens = [t for t in text.split() if t not in STOPWORDS_PT]
        result = " ".join(tokens)
        print(f"Preprocessing: '{text[:50]}...' -> '{result[:50]}...'")
        return result
    except Exception as e:
        print(f"Erro no preprocessing: {e}")
        return text.lower() if text else ""

BAD_WORDS = {
    "arrombado","idiota","imbecil","merda","lixo","odiar","te odeio",
    "vai se f*","vai se ferrar","desgraça","otário","otaria","burro","burra"
    # ajuste conforme necessário
}

def is_toxic(text: str) -> bool:
    t = text.lower()
    return any(w in t for w in BAD_WORDS)