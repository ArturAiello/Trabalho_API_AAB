import os
import logging
import pandas as pd
from enum import Enum

from fastapi import FastAPI, HTTPException, Depends, Header, status
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(asctime)s: %(message)s")
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


def executar_prompt(prompt: str) -> str:
    """
    Executa um prompt via API Groq e retorna a resposta.

    Args:
        prompt (str): O texto do prompt a ser processado.

    Returns:
        str: Resposta gerada pela API Groq.
    """
    try:
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar requisição"
        )


# Modelos para validação dos payloads
class BuscaGrauFerimento(BaseModel):
    pergunta: str


class BuscaPartesCorpo(BaseModel):
    pergunta: str


# Instanciando a aplicação FastAPI
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
    dependencies=[Depends(verifica_token)],
)


# Endpoint: Busca – Grau de Ferimento (POST)
@app.post("/busca/grau-ferimento", summary="Busca grau de ferimento")
def busca_grau_ferimento(dados: BuscaGrauFerimento):
    logger.info(f"Recebida requisição de grau de ferimento: {dados.pergunta}")

    if df_kaggle is None:
        raise HTTPException(status_code=500, detail="Dataset do Kaggle não carregado")

    try:
        partes = df_kaggle["degree_of_injury"].value_counts().to_dict()
    except Exception as e:
        logger.error(f"Erro ao processar dados do dataset: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar o dataset")

    prompt = (
        f"Utilize os dados do dataset do Kaggle e a seguinte informação: {partes}, "
        f"para responder: {dados.pergunta}. "
        "Forneça uma análise resumida sobre graus de ferimento mais comuns."
    )
    resposta = executar_prompt(prompt)
    return {"resultado": resposta, "dados": partes}


# Endpoint: Buscas – Partes do Corpo Afetadas (POST)
@app.post("/busca/partes-corpo-afetadas", summary="Busca partes do corpo afetadas")
def busca_partes_corpo(dados: BuscaPartesCorpo):
    logger.info(f"Recebida requisição de partes do corpo afetadas: {dados.pergunta}")

    if df_kaggle is None:
        raise HTTPException(status_code=500, detail="Dataset do Kaggle não carregado")

    try:
        partes = df_kaggle["body_part"].value_counts().to_dict()
    except Exception as e:
        logger.error(f"Erro ao processar dados do dataset: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar o dataset")

    prompt = (
        f"Utilize os dados do dataset do Kaggle e a seguinte informação: {partes}, "
        f"para responder: {dados.pergunta}. "
        "Forneça uma análise resumida sobre as partes do corpo mais afetadas."
    )
    resposta = executar_prompt(prompt)
    return {"resultado": resposta, "dados": partes}


# Carregamento do dataset do Kaggle
DATA_PATH = "data/osha_accident_injury_data.csv"

try:
    df_kaggle = pd.read_csv(DATA_PATH)
    logger.info("Dataset do Kaggle carregado com sucesso!")
except Exception as e:
    logger.error(f"Erro ao carregar o dataset do Kaggle: {e}")
    df_kaggle = None
