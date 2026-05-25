import json
from config import client, MODEL_NAME
from api import pesquisar_web

# Definição da ferramenta estruturada para o modelo 
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "pesquisar_web",
            "description": "Busca informações em tempo real na internet sobre notícias, eventos recentes, lançamentos ou tendências do mundo tecnológico.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "O termo ou frase de busca otimizado para o Google."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# Prompt de instruções para a busca
SYSTEM_PROMPT = (
    "Você é o Curador de Notícias Tech, um assistente especialista em tecnologia atualizada.\n\n"
    "Regra de Ouro:\n"
    "O ano atual é 2026. Se o usuário perguntar sobre qualquer evento, dado factual ou tendência fora do seu limite de conhecimento (especialmente anos como 2024, 2025 ou 2026), NÃO diga que não sabe. Você DEVE acionar imediatamente a ferramenta 'pesquisar_web' para buscar no Google.\n\n"
    "Instruções Obrigatórias:\n"
    "1. Baseie-se estritamente nos dados retornados pela pesquisa. Não invente informações.\n"
    "2. Você DEVE obrigatoriamente listar os links (URLs) das fontes utilizadas no final do texto sob o título 'Fontes Utilizadas:'.\n"
    "3. Se a busca falhar ou der erro de conexão, explique isso amigavelmente em vez de quebrar a execução.\n"
    "4. NÃO use marcadores como '' ou '[1]' no meio do texto. Escreva de forma fluida."
)

def executar_agente(pergunta_usuario: str, callback_status=None):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": pergunta_usuario}
    ]
    
    # Primeira chamada à LLM
    try:

        if callback_status:
            callback_status.write("Analisando a pergunta... ⌛")
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=1000
        )
    except Exception as e:
        return f"Desculpe, ocorreu um erro de comunicação com o provedor de IA. ({e})"

    resposta_mensagem = response.choices[0].message
    tool_calls = resposta_mensagem.tool_calls

    # Verifica se o modelo decidiu acionar a busca na web
    if tool_calls:

        if callback_status:
            callback_status.write("Necessito buscar dados na Web...")
        
        
        messages.append(resposta_mensagem)
        

        for tool_call in tool_calls:

            if tool_call.function.name == "pesquisar_web":

                argumentos = json.loads(tool_call.function.arguments)
                termo_busca = argumentos.get("query")

                if callback_status:
                    callback_status.write(f"Dando um 'Google' por: *'{termo_busca}'*")
                
                # Executa a ferramenta de busca externa
                resultado_pesquisa = pesquisar_web(termo_busca)
                
                # Injeta os resultados no contexto
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": "pesquisar_web",
                    "content": resultado_pesquisa
                })
        
        # Segunda chamada à LLM
        try:

            if callback_status:
                callback_status.write("Validando as informações...")
            
            segunda_resposta = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=1000
            )
            return segunda_resposta.choices[0].message.content
        except Exception as e:
            return f"Desculpe, falha ao processar os dados da pesquisa. ({e})"
            
    else:
        # Resposta caso não precise de dados externos
        return resposta_mensagem.content