import os
from dotenv import load_dotenv
from openai import AzureOpenAI, APIError

# Carrega as variáveis declaradas no arquivo .env
load_dotenv()

# Instancia o cliente do Azure OpenAI mapeando as variáveis de ambiente
client = AzureOpenAI(
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("API_KEY"),
    # Define uma versão recente e suportada da API do Azure
    api_version=os.getenv("API_VERSION", "2023-11-01")
)

deployment_name = os.getenv("GPT5_MODEL")

print("--- Agente de Atendimento Iniciado ---")

while True:
    pergunta = input("\nDigite sua pergunta (ou 'sair' para encerrar): ").strip()

    if pergunta.lower() == "sair":
        print("Atendimento finalizado. Até logo!")
        break

    if not pergunta:
        print("Por favor, digite uma pergunta válida.")
        continue

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um agente de atendimento prestativo e cortês."
                },
                {
                    "role": "user",
                    "content": pergunta
                }
            ],
            temperature=0.7
        )

        resposta_texto = response.choices[0].message.content
        print(f"\nResposta:\n{resposta_texto}")

    except APIError as e:
        print(f"\n[Erro na API]: {e.message}")
    except Exception as e:
        print(f"\n[Erro inesperado]: {e}")
