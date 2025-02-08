# Trabalho API

Esta API foi desenvolvida para realizar buscas relacionadas a **grau de ferimento** e **partes do corpo afetadas** em acidentes, utilizando a API do Groq para processamento dos dados (com base, de forma simulada, no dataset do Kaggle [OSHA Accident and Injury Data 2015-2017](https://www.kaggle.com/datasets/ruqaiyaship/osha-accident-and-injury-data-1517/data)).  

A API foi construída com **FastAPI** e utiliza **Pydantic** para validação dos dados, além de contar com autenticação simples, logging, tratamento de erros e documentação automática via Swagger.

---

## Sumário

- [Requisitos](#requisitos)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Instalação](#instalação)
- [Execução da API](#execução-da-api)
- [Endpoints](#endpoints)
- [Testes com Postman e Swagger](#testes-com-postman-e-swagger)
- [Contribuição e Versionamento](#contribuição-e-versionamento)
- [Licença](#licença)

---

## Requisitos

- Python 3.8 ou superior
- Git e GitHub Desktop (para controle de versão e clonagem)
- [Pip] (https://pip.pypa.io/)
- Biblioteca [Ruff](https://docs.astral.sh/ruff/) para formatação automática (opcional)

---

## Configuração do Ambiente

1. **Clone o repositório:**

   - Utilize o GitHub Desktop para clonar o repositório `Trabalho API` para sua máquina local.

2. **Crie e ative o ambiente virtual:**

   ```bash
   python -m venv venv

- No Windows: 
   ```bash
   venv\Scripts\activate
 
- No Linux/Mac: 
   ```bash
   source venv/bin/activate

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt

4. **Configure o arquivo .env:**

Crie um arquivo chamado .env na raiz do projeto e adicione a sua chave da API Groq: GROQ_API_KEY=_sua_chave_aqui_
 
5. **Verifique se o .gitignore está configurado:**
Certifique-se de que a pasta venv/ esteja listada no arquivo .gitignore para evitar o versionamento desnecessário.

---

## Instalação

- Após clonar o repositório e configurar o ambiente, instale as bibliotecas necessárias: 
 
   ```bash
   pip install fastapi uvicorn python-dotenv groq

- Para gerar o arquivo de dependências: 
 
   ```bash
   pip freeze > requirements.txt


---

## Execução da API
**Modo de Desenvolvimento**

- Execute a API com o Uvicorn (servidor ASGI):

   ```bash
   uvicorn main:app --reload

- A flag --reload garante que o servidor seja reiniciado a cada modificação no código.

**Modo de Produção**

- Em produção, utilize:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 80

- Dica: Considere utilizar um servidor de produção como Gunicorn com Uvicorn Workers para melhor performance.

---

## Endpoints

1. **Busca – Grau de Ferimento**

- URL: /busca/grau-ferimento

- Método: POST
 
- Payload (JSON):

   ```bash
   {
  "pergunta": "Descreva os níveis de ferimento para uma queda de altura."
   }

- Descrição: 
Recebe uma pergunta e utiliza a API do Groq para determinar o grau do ferimento.

2. **Busca – Parte do Corpo Afetadas**

- URL: /busca/partes-corpo-afetadas

- Método: POST

- Payload (JSON):

   ```bash
   {
  "pergunta": "Quais partes do corpo são mais afetadas em acidentes?"
   }

- Descrição: 
Realiza uma busca considerando dados do dataset do Kaggle (simulado) e utiliza a API do Groq para processar a resposta.

Nota:
Em todas as requisições, inclua no header o token de autenticação:

   ```bash
   api_token: 123

---

## Testes com Postman e Swagger

- Swagger UI:

Ao iniciar a API, acesse http://127.0.0.1:8000/docs para visualizar e testar os endpoints.

- Postman: 
   - Crie uma nova coleção e importe o arquivo openapi.json (que pode ser baixado da URL /openapi.json da API) para testar os endpoints.
   - Realize chamadas passando o header api_token com o valor 123.

---

## Contribuição e Versionamento

- Repositório no GitHub:
Realize commits frequentes com mensagens descritivas e utilize branches para desenvolver novas funcionalidades.

- Versionamento dos Endpoints:
Se necessário, implemente versionamento (por exemplo, /v1/busca/grau-ferimento) para manter compatibilidade com versões anteriores.

- Ferramenta de Formatação:
Utilize o [Ruff](https://docs.astral.sh/ruff/) para garantir a formatação do código e a verificação de sintaxe.

---

## Licança

Este projeto está licenciado sob a [Licença Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

---

## Observações Finais

- Segurança:
   - Não commit a chave da API (GROQ_API_KEY) no repositório público. Utilize variáveis de ambiente.
   
   - Em produção, utilize HTTPS para criptografar as requisições.

- Logs:
O sistema de logging registra informações importantes sobre as requisições e erros. Verifique os logs para monitorar o funcionamento da API.


---

## Conclusão

Seguindo este passo a passo, você terá uma API robusta e segura, com endpoints específicos para a busca de informações sobre o grau de ferimento e partes do corpo afetadas, além de integração com a API do Groq e o dataset do Kaggle (simulado). Lembre-se de testar a API com o Postman e acessar a documentação Swagger para validar todas as funcionalidades. Por fim, não esqueça de versionar e realizar commits frequentes no seu repositório GitHub!

Boa codificação!
