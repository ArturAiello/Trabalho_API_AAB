from fastapi import APIRouter, HTTPException
import pandas as pd

from models import BuscaGrauFerimento, BuscaPartesCorpo
from utils import executar_prompt, obter_logger_e_configuracao, dataset_return

from utils import limiter
from fastapi import Request

# Configuração do roteador da API
router = APIRouter()

# Obter o logger configurado
logger = obter_logger_e_configuracao()


@router.post("/busca/grau-ferimento", summary="Busca grau de ferimento")
@limiter.limit("5/minute")
def busca_grau_ferimento(request: Request, dados: BuscaGrauFerimento):
    """
    Endpoint para buscar o grau de ferimento com base em uma pergunta.

    Este endpoint utiliza os dados do dataset do Kaggle para identificar a frequência dos
    graus de ferimento e consulta a API Groq para gerar uma resposta com uma análise resumida.

    Args:
        dados (BuscaGrauFerimento): Modelo de dados contendo a pergunta.

    Returns:
        dict: Dicionário contendo a resposta gerada e os dados de frequência dos graus de ferimento.
    """
    logger.info("Requisição recebida para busca de grau de ferimento: %s", dados.pergunta)

    df_kaggle = dataset_return()
    if df_kaggle is None:
        logger.error("Dataset do Kaggle não foi carregado.")
        raise HTTPException(status_code=500, detail="Dataset do Kaggle não carregado")

    try:
        frequencia_grau = df_kaggle["Degree of Injury"].value_counts().to_dict()
    except Exception as e:
        logger.error("Erro ao processar dados do dataset: %s", e)
        raise HTTPException(status_code=500, detail="Erro ao processar o dataset")

    prompt = (
        f"Utilize os dados do dataset do Kaggle e a seguinte informação: {frequencia_grau}, "
        f"para responder: {dados.pergunta}. "
        "Forneça uma análise resumida em português brasileiro sobre graus de ferimento mais comuns. Os resultados não devem ser mostrados em língua inglesa."
    )
    resposta = executar_prompt(prompt)
    logger.info("Resposta gerada com sucesso para busca de grau de ferimento.")
    return {"resultado": resposta, "dados": frequencia_grau}



@router.post("/busca/partes-corpo-afetadas", summary="Busca partes do corpo afetadas")
@limiter.limit("5/minute")
def busca_partes_corpo(request: Request, dados: BuscaPartesCorpo):
    """
    Endpoint para buscar as partes do corpo afetadas com base em uma pergunta.

    Este endpoint utiliza os dados do dataset do Kaggle para identificar a frequência das
    partes do corpo afetadas e consulta a API Groq para gerar uma resposta com uma análise resumida.

    Args:
        dados (BuscaPartesCorpo): Modelo de dados contendo a pergunta.

    Returns:
        dict: Dicionário contendo a resposta gerada e os dados de frequência das partes do corpo afetadas.
    """
    logger.info("Requisição recebida para busca de partes do corpo afetadas: %s", dados.pergunta)

    df_kaggle = dataset_return()
    if df_kaggle is None:
        logger.error("Dataset do Kaggle não foi carregado.")
        raise HTTPException(status_code=500, detail="Dataset do Kaggle não carregado")

    try:
        frequencia_partes = df_kaggle["Part of Body"].value_counts().to_dict()
    except Exception as e:
        logger.error("Erro ao processar dados do dataset: %s", e)
        raise HTTPException(status_code=500, detail="Erro ao processar o dataset")

    prompt = (
        f"Utilize os dados do dataset do Kaggle e a seguinte informação: {frequencia_partes}, "
        f"para responder: {dados.pergunta}. "
        "Forneça uma análise resumida em português brasileiro sobre as partes do corpo mais afetadas. Os resultados não devem ser mostrados em língua inglesa."
    )
    resposta = executar_prompt(prompt)
    logger.info("Resposta gerada com sucesso para busca de partes do corpo afetadas.")
    return {"resultado": resposta, "dados": frequencia_partes}

