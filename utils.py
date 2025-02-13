import os
import logging
import pandas as pd
from fastapi import HTTPException, Header, status
from groq import Groq
from dotenv import load_dotenv
from jose import JWTError, jwt
from datetime import datetime, timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Carrega as variáveis de ambiente
load_dotenv()


def obter_logger_e_configuracao():
    """
    Configura e retorna o logger para a aplicação.

    Returns:
        logging.Logger: Logger configurado com nível INFO e formato padrão.
    """
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(asctime)s: %(message)s")
    return logging.getLogger("TrabalhoAPI")


# Inicializa o logger para uso interno neste módulo
logger = obter_logger_e_configuracao()

# Recupera o token de autenticação da API a partir das variáveis de ambiente
API_TOKEN = os.getenv("API_TOKEN")
if API_TOKEN is None:
    logger.error("API_TOKEN não definido nas variáveis de ambiente")


def verifica_token(api_token: str = Header(..., description="Token de autenticação da API")):
    """
    Dependência que verifica se o token enviado no header é válido.

    Args:
        api_token (str): Token fornecido no header da requisição.

    Raises:
        HTTPException: Caso o token seja inválido.

    Returns:
        str: O token validado.
    """
    # Se o token começar com "Bearer ", trate-o como JWT
    if api_token.startswith("Bearer "):
        token = api_token[7:]  # remove o prefixo "Bearer "
        return verifica_token_jwt(token)
    # Caso contrário, use o método simples (token definido no .env)
    if api_token != API_TOKEN:
        logger.error("Token inválido recebido: %s", api_token)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return api_token


def executar_prompt(prompt: str) -> str:
    """
    Executa um prompt utilizando a API Groq e retorna a resposta.

    Args:
        prompt (str): Texto do prompt a ser processado.

    Returns:
        str: Resposta gerada pela API Groq.

    Raises:
        HTTPException: Em caso de falha ao executar o prompt.
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
        logger.info("Resposta do Groq obtida com sucesso.")
        return resposta
    except Exception as e:
        logger.error("Erro ao executar prompt: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar requisição"
        )


# --- NOVA FUNÇÃO: Carregamento do Dataset ---
DATA_PATH = "osha-accident-and-injury-data-1517/OSHA HSE DATA_ALL ABSTRACTS 15-17_FINAL.csv"

def dataset_return():
    """
    Carrega o dataset do Kaggle a partir do arquivo CSV.

    Returns:
        pd.DataFrame: DataFrame com os dados do dataset ou None em caso de erro.
    """
    try:
        df = pd.read_csv(DATA_PATH)
        logger.info("Dataset do Kaggle carregado com sucesso!")
        return df
    except Exception as e:
        logger.error("Erro ao carregar o dataset do Kaggle: %s", e)
        return None
    
    # Defina as configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "minha_chave_secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verifica_token_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # ou retorne informações relevantes do payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token JWT inválido")