# 🤖 Curador de Notícias Tech — Desafio Técnico

[cite_start]Bem-vindo ao **Curador de Notícias Tech**, uma aplicação desenvolvida como parte do processo seletivo da Qualiserve para a vaga de Desenvolvedor de Soluções de IA[cite: 4, 14].

[cite_start]O objetivo deste projeto é entregar um agente de conversação inteligente capaz de atuar de forma autônoma[cite: 19, 20]. [cite_start]Quando provocado com perguntas sobre eventos, lançamentos ou tendências recentes do mundo da tecnologia, o agente identifica a necessidade de buscar dados atualizados, realiza pesquisas em tempo real na web, consolida o contexto e responde ao usuário de forma clara, amigável e estritamente referenciada[cite: 20, 24, 25].

---

## 🛠️ Tecnologias e Ferramentas Obrigatórias

[cite_start]Para garantir a conformidade com os requisitos do desafio, o projeto utiliza as seguintes ferramentas de base[cite: 27]:

- [cite_start]**Orquestração e LLM (OpenRouter):** Processamento do modelo de linguagem através da API unificada do OpenRouter (utilizando a biblioteca oficial `openai`), configurado por padrão com o modelo estável `google/gemini-2.5-flash`[cite: 28, 29].
- [cite_start]**Pesquisa na Web (Serper.dev):** API especializada para retornar dados estruturados do Google Search em formato JSON[cite: 40, 41].
- [cite_start]**Interface do Usuário (Streamlit):** Front-end interativo em formato de Chat, fornecendo uma experiência de uso simples e moderna.

---

## 📁 Estrutura do Projeto

O projeto foi unificado em um script principal de interface gráfica, mantendo a raiz organizada da seguinte forma:

```text
curador_tech/
│
├── app.py             # Arquivo Único: Contém as configurações, ferramentas, core do agente e interface Streamlit.
├── requirements.txt   # Lista de dependências e bibliotecas do projeto.
└── .env               # Arquivo local com as variáveis de ambiente (Chaves de API).

---

⚙️ Configuração das Variáveis de Ambiente
O sistema utiliza variáveis de ambiente para gerenciar as credenciais com segurança.
    1. Na raiz do projeto, crie um arquivo chamado .env.
    2. Adicione as suas chaves de API seguindo o modelo abaixo:

    OPENROUTER_API_KEY=sua_chave_aqui_da_openrouter
    SERPER_API_KEY=sua_chave_aqui_da_serper_dev

🚀 Instalação e Execução
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
```