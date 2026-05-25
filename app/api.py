import json
import requests
from config import SERPER_API_KEY

#Realizar buscas no Google e retornar uma estrutura limpa
def pesquisar_web(query: str) -> str:

    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({"q": query, "gl": "br", "hl": "pt-br"})
    
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        dados = response.json()
        
        resultados = []
        
        # Resposta orgânica do Google 
        if "organic" in dados:
            for item in dados["organic"][:4]: #4 principais resultados
                titulo = item.get("title", "Sem título")
                snippet = item.get("snippet", "")
                link = item.get("link", "")
                resultados.append(f"Título: {titulo}\nResumo: {snippet}\nFonte (URL): {link}\n---")
                
        if not resultados:
            return "Nenhum resultado relevante foi encontrado na internet para essa busca."
            
        return "\n".join(resultados)
        
    except requests.exceptions.RequestException as e:
        print(f"\n[LOG-ERRO] Falha ao conectar com o Serper.dev: {e}")
        return "ERRO_CONEXAO: Não foi possível acessar a internet no momento para buscar dados atualizados."