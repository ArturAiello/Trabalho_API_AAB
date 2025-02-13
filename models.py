from pydantic import BaseModel

class BuscaGrauFerimento(BaseModel):
    """
    Modelo de dados para requisições de busca por grau de ferimento.

    Attributes:
        pergunta (str): Pergunta para análise do grau de ferimento.
    """
    pergunta: str


class BuscaPartesCorpo(BaseModel):
    """
    Modelo de dados para requisições de busca por partes do corpo afetadas.

    Attributes:
        pergunta (str): Pergunta para análise das partes do corpo afetadas.
    """
    pergunta: str
