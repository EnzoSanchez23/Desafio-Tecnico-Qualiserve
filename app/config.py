#######################################
# Configurações gerais do projeto
# Leitura das chaves na .env
# Definição do modelo a ser utilizado
#######################################

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENROUTER_API_KEY") or not os.getenv("SERPER_API_KEY"):
    raise ValueError("Por favor, configure as chaves OPENROUTER_API_KEY e SERPER_API_KEY no arquivo .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL_NAME = "google/gemini-2.5-flash"
SERPER_API_KEY = os.getenv("SERPER_API_KEY")