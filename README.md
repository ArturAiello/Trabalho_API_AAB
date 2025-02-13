# Trabalho API

construída com FastAPI para busca e análise de informações relativas a acidentes, utilizando dados do dataset do Kaggle (simulado) e a API Groq para processamento de linguagem. A API conta com medidas de segurança aprimoradas, como autenticação (token simples e JWT), rate limiting, cabeçalhos de segurança e configuração de CORS.  

---

## Sumário

- [Descrição do Projeto](#descrição-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Executando a API](#executando-a-api)
- [Endpoints](#endpoints)
- [Testes](#testes)
- [Medidas de Segurança](#medidas-de-segurança)
- [Contribuição](#contribuição)
- [Licença](#licença)


---

## Descrição do Projeto

Esta API oferece dois principais endpoints para busca:
- **Grau de Ferimento:** Retorna uma análise sobre a frequência dos graus de ferimento com base em uma pergunta.
- **Partes do Corpo Afetadas:** Retorna uma análise sobre as partes do corpo mais afetadas com base em uma pergunta.

A API utiliza dados extraídos de um CSV do Kaggle e integra com a API Groq para gerar respostas com análises resumidas, sempre em português brasileiro.

---

## Funcionalidades

- **Autenticação:**  
  - Verificação via token simples (definido no arquivo `.env`).
  - Suporte opcional para JWT (via prefixo `Bearer`).
- **Rate Limiting:**  
  - Utiliza a biblioteca SlowAPI para limitar o número de requisições (5 requisições por minuto por endpoint).
- **Segurança Adicional:**  
  - Configuração de CORS para permitir apenas origens autorizadas.
  - Middleware de cabeçalhos de segurança (X-Content-Type-Options, X-Frame-Options e X-XSS-Protection).
- **Validação de Dados:**  
  - Uso do Pydantic para validação dos modelos de entrada.
- **Logging:**  
  - Registro detalhado de requisições e erros para monitoramento e auditoria.
- **Integração com API Groq:**  
  - Processamento de prompts para gerar respostas com análises.

---

## Requisitos

- **Python:** 3.8 ou superior
- **Dependências:** As listadas no arquivo [requirements.txt](./requirements.txt)

---

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu_usuario/Trabalho_API_ACD.git
   cd Trabalho_API_ACD


2. **Crie e ative o ambiente virtual:**

- Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate

- Linux/Mac:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   
## Configuração do Ambiente

1. **Arquivo .env:**
Crie um arquivo chamado .env na raiz do projeto e configure as seguintes variáveis:

GROQ_API_KEY=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
API_TOKEN="123"
SECRET_KEY="minha_chave_secreta"  # Usada para a criação e validação de tokens JWT (opcional)

2. **Proteção do .env:**
- Certifique-se de que o arquivo .env esteja incluído no .gitignore (conforme definido no arquivo .gitmore).

## Executando a API

Para iniciar o servidor de desenvolvimento, execute:

   ```bash
   uvicorn main:app --reload
   
- A API estará disponível em: http://127.0.0.1:8000

## Endpoints
1. **Busca Grau de Ferimento**
- URL: /busca/grau-ferimento
- Método: POST
- Payload (JSON):

{
  "pergunta": "Qual é a incidência de ferimentos graves em acidentes de trabalho?"
}

Descrição: Retorna uma análise com base na frequência dos graus de ferimento presentes no dataset.

2. **Busca Partes do Corpo Afetadas**
- URL: /busca/partes-corpo-afetadas
- Método: POST
- Payload (JSON):

{
  "pergunta": "Quais partes do corpo são mais afetadas em acidentes de trânsito?"
}

Descrição: Retorna uma análise com base na frequência das partes do corpo afetadas presentes no dataset.

Observação: Todos os endpoints requerem um header de autenticação chamado api_token com o valor definido no .env (ou um token JWT com prefixo Bearer ).

## Testes
- Swagger UI:
Acesse http://127.0.0.1:8000/docs para visualizar a documentação interativa e testar os endpoints.

- Postman:
Importe a coleção ou realize chamadas para os endpoints utilizando o header api_token.

## Medidas de Segurança

1. **Autenticação:**
- Token simples definido no .env e suporte opcional para JWT.

2. **Rate Limiting:**
- Configurado com SlowAPI (5 requisições/minuto por endpoint).

3. **CORS:**
- Permite apenas origens autorizadas (configurar a lista de origens conforme necessidade).

4. **Cabeçalhos de Segurança:**
- Middleware que adiciona cabeçalhos HTTP para proteção contra ataques comuns.

5. **HTTPS:**
- Em produção, recomenda-se executar a API sob HTTPS (configuração via Uvicorn ou proxy reverso).

## Contribuição
1. **Faça um fork do repositório.**
2. **Crie uma branch com a sua feature: git checkout -b minha-feature.**
3. **Realize commit das alterações: git commit -m "Minha nova feature".**
4. **Envie para o branch: git push origin minha-feature.**
5. **Abra um Pull Request.**

## Licença
Este projeto está licenciado sob a Licença MIT.

##Contato
Para dúvidas ou suporte, entre em contato com trabalho_acd@aulaapi.com.


## Conclusão

Seguindo este passo a passo, você terá uma API robusta e segura, com endpoints específicos para a busca de informações sobre o grau de ferimento e partes do corpo afetadas, além de integração com a API do Groq e o dataset do Kaggle (simulado). Lembre-se de testar a API com o Postman e acessar a documentação Swagger para validar todas as funcionalidades. Por fim, não esqueça de versionar e realizar commits frequentes no seu repositório GitHub!

Boa codificação!
