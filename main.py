import os
import logging
from enum import Enum

from fastapi import FastAPI, HTTPException, Depends, Header, status
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s: %(message)s')
logger = logging.getLogger("TrabalhoAPI")

# Carrega variáveis de ambiente
load_dotenv()

# Token da API para autenticação (simples)
API_TOKEN = "123"

def verifica_token(api_token: str = Header(..., description="Token de autenticação da API")):
    """
    Dependency que verifica se o token enviado no header é válido.
    """
    if api_token != API_TOKEN:
        logger.error("Token inválido")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return api_token

# Função para chamar a API Groq e processar a requisição
def executar_prompt(prompt: str) -> str:
    """
    Executa um prompt via API Groq e retorna a resposta.
    
    Args:
        prompt (str): O texto do prompt a ser processado.
    
    Returns:
        str: Resposta gerada pela API Groq.
    """
    try:
        # Obtém a chave da API Groq a partir do .env
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("Chave da API Groq não encontrada no .env")
        client = Groq(api_key=groq_api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="deepseek-r1-distill-llama-70b",
        )
        resposta = chat_completion.choices[0].message.content
        logger.info("Resposta do Groq obtida com sucesso")
        return resposta
    except Exception as e:
        logger.error(f"Erro ao executar prompt: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar requisição")

# Modelos para validação dos payloads

class BuscaGrauFerimento(BaseModel):
    pergunta: str

class BuscaPartesCorpo(BaseModel):
    pergunta: str

# Instanciando o FastAPI com dependência global de autenticação
app = FastAPI(
    title="Trabalho_API_AAB",
    description="""
API para busca de informações sobre:
- **Grau de Ferimento:** Recebe uma pergunta e retorna uma análise quanto ao grau do ferimento.
- **Partes do Corpo Afetadas:** Recebe uma pergunta e utiliza dados do dataset do Kaggle (simulado) para identificar partes do corpo afetadas, com processamento via API Groq.
    
**Observações de segurança:**  
- Autenticação via token simples (API_TOKEN).
- Validação dos dados com Pydantic.
- Logs e tratamento de erros com códigos HTTP apropriados.
    """,
    version="1.0.0",
    dependencies=[Depends(verifica_token)]
)

# Endpoint: Busca – Grau de Ferimento (POST)
@app.post(
    "/busca/grau-ferimento",
    summary="Busca grau de ferimento",
    description="Recebe uma pergunta via JSON e retorna uma análise sobre o grau do ferimento, utilizando a API Groq.",
    tags=["Buscas"]
)
def busca_grau_ferimento(dados: BuscaGrauFerimento):
    logger.info(f"Recebida requisição de grau de ferimento: {dados.pergunta}")
    prompt = f"Analise a seguinte pergunta e determine o grau do ferimento: {dados.pergunta}"
    resposta = executar_prompt(prompt)
    return {"resultado": resposta}

# Endpoint: Buscas – Partes do Corpo Afetadas (POST)
@app.post(
    "/busca/partes-corpo-afetadas",
    summary="Busca partes do corpo afetadas",
    description=("Recebe uma pergunta via JSON para identificar partes do corpo afetadas em acidentes, "
                 "utilizando dados do dataset do Kaggle (simulado) e a API Groq para processamento."),
    tags=["Buscas"]
)
def busca_partes_corpo(dados: BuscaPartesCorpo):
    logger.info(f"Recebida requisição de partes do corpo afetadas: {dados.pergunta}")
    prompt = (
        f"Utilize os dados do dataset do Kaggle sobre acidentes (OSHA 2015-2017) para responder a seguinte pergunta: {dados.pergunta}. "
        "Identifique as partes do corpo mais afetadas e forneça uma análise resumida."
    )
    resposta = executar_prompt(prompt)
    return {"resultado": resposta}
