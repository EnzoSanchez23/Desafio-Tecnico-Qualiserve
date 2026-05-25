# 🤖 Curador de Notícias Tech — Desafio Técnico

Este repositório contém a solução desenvolvida para o processo seletivo da **Qualiserve** para a vaga de **Analista Junior**. 

O projeto consiste em um Agente de Conversação inteligente e autônomo, munido de uma interface gráfica construída em Streamlit, capaz de atuar em tempo real como um Curador de Notícias Tecnológicas. O agente analisa as perguntas dos utilizadores, identifica de forma autônoma a necessidade de buscar fatos ou tendências recentes na internet, consome APIs externas, consolida o contexto dinamicamente e gera respostas estruturadas e estritamente referenciadas.

---

## 🛠️ Ferramentas e APIs Utilizadas

Para cumprir rigorosamente os requisitos obrigatórios estabelecidos pelo desafio, foram integradas as seguintes tecnologias:

* **Orquestração e LLM (OpenRouter API):** Processamento cognitivo do agente através do modelo estável `google/gemini-2.5-flash` via API unificada do OpenRouter, utilizando a biblioteca oficial da `openai` de forma 100% compatível.
* **Pesquisa na Web (Serper.dev API):** Mecanismo de busca especializado para recuperação de dados estruturados e orgânicos do Google Search em formato JSON.
* **Interface do Usuário (Streamlit):** Front-end interativo em formato de Chat UI para fornecer uma experiência fluida, moderna e de fácil avaliação.

---

## 📁 Estrutura do Projeto

O projeto foi construído seguindo padrões rígidos de modularização e separação de responsabilidades (Separation of Concerns):

```text
Desafio-Tecnico-Qualiserve/
│
├── app/                      # Diretório principal da aplicação
│   ├── agent.py              # Core do Agente (Definição de ferramentas, prompts e lógica de Tool Calling)
│   ├── api.py                # Integração com os serviços externos (Busca no Serper.dev)
│   ├── config.py             # Inicialização dos clientes de API e chaves de ambiente
│   ├── interface.py          # Interface gráfica interativa construída com Streamlit
│   └── main.py               # Interface alternativa via Linha de Comando (CLI)
│
├── .env.example              # Modelo explicativo de configuração das chaves
├── .gitattributes            # Configurações de atributos do Git
├── .gitignore                # Arquivo de exclusão para Git (ignora venv e .env)
├── LICENSE                   # Licença de uso do projeto
├── README.md                 # Documentação principal do repositório
└── requirements.txt          # Lista de dependências e bibliotecas do projeto

```
---

⚙️ Configuração das Variáveis de Ambiente
O sistema utiliza variáveis de ambiente para gerenciar as credenciais com segurança.
    1. Na raiz do projeto, crie um arquivo chamado .env.
    2. Adicione as suas chaves de API seguindo o modelo abaixo:

    OPENROUTER_API_KEY=sua_chave_aqui_da_openrouter
    SERPER_API_KEY=sua_chave_aqui_da_serper_dev

## 🚀 Instalação e Execução
Siga os passos abaixo para configurar o ambiente virtual e executar a aplicação na sua máquina local:
1. Preparar o Ambiente Virtual (Recomendado)
    No terminal, dentro da pasta raiz do projeto, execute:

    # No Linux/macOS:
    python -m venv venv
    source venv/bin/activate

    # No Windows (Prompt de Comando):
    python -m venv venv
    venv\Scripts\activate

2. Instalar as Dependências
Com o ambiente virtual ativo, instale os pacotes necessários contidos no arquivo de requerimentos:

    pip install -r requirements.txt

3. Executar a Aplicação (Interface Web Streamlit)
Para iniciar o agente com a interface gráfica, execute o comando:

    streamlit run app.py

---

🧠 Explicação Estratégica da Solução

1. Lógica de Tool Calling e Engenharia de Prompt
Em vez de utilizar condicionais rígidas baseadas em strings (como if "pesquisa" in texto), a solução adota a tecnologia nativa de Tool Calling (Function Calling).
A ferramenta pesquisar_web é descrita detalhadamente para o modelo através de uma estrutura JSON, mapeando os parâmetros esperados. No SYSTEM_PROMPT do arquivo app.py, o modelo é explicitamente instruído sobre a sua identidade temporal (reconhecendo o ano vigente de 2026) e orientado a ativar a ferramenta de busca sempre que o usuário trouxer perguntas factuais sobre anos recentes ou novidades tecnológicas.

2. Manipulação de Dados e Contexto
Quando o modelo decide de forma autônoma que precisa de dados externos, o script intercepta a chamada, aciona o endpoint do Serper.dev e manipula o JSON retornado. Os títulos, snippets e URLs dos resultados mais relevantes são extraídos cirurgicamente e reinjetados no histórico da conversa sob a role de "tool", permitindo que a LLM faça a consolidação do texto final.

3. Citação Obrigatória e Formatação
O agente foi blindado via prompt e pós-processamento com expressões regulares para nunca alucinar ou embutir marcações de citação poluidoras no meio do texto (como ``). A resposta flui de forma natural, e as referências originais coletadas na web são exibidas de maneira organizada e obrigatória em uma seção exclusiva ao final do texto, chamada "Fontes Utilizadas:".

4. Resiliência e Tratamento de Exceções
As chamadas de rede às APIs externa do Serper.dev e do OpenRouter são encapsuladas em blocos de tratamento de erro (try-except). Caso ocorra falha de comunicação, timeout ou instabilidade em qualquer uma das pontas, o agente captura a exceção e retorna uma mensagem amigável ao usuário explicando o ocorrido, mitigando quebras abruptas na execução e prevenindo alucinações de dados fictícios.

5. Eficiência e FinOps
Para evitar o erro de cota 402 comum no OpenRouter ao trabalhar com Tool Calling (onde os modelos tentam reservar o limite máximo absoluto de tokens de saída por padrão), foi implementado o controle explícito de max_tokens=1000 em ambas as requisições, garantindo previsibilidade de custos e otimização do uso de créditos.
