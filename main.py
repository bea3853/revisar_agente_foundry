import os
from dotenv import load_dotenv
from openai import AzureOpenAI, APIError


load_dotenv(override=True)

client = AzureOpenAI(
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("API_KEY"),
 
    api_version=os.getenv("API_VERSION", "2025-04-01-preview")
)


deployment_name = os.getenv("GPT5_MODEL")


def validar_configuracao():
    faltando = []
    if not os.getenv("ENDPOINT"):
        faltando.append("ENDPOINT")
    if not os.getenv("API_KEY"):
        faltando.append("API_KEY")
    if not deployment_name:
        faltando.append("GPT5_MODEL")

    if faltando:
        print("\n[Erro de configuração] As seguintes variáveis não foram definidas no .env:")
        for var in faltando:
            print(f"  - {var}")
        print("\nPreencha o arquivo .env e tente novamente.")
        return False
    return True


def main():
    if not validar_configuracao():
        return


    api_key = os.getenv("API_KEY", "")
    api_key_mascarada = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "(vazia ou muito curta)"
    print(" diagnostico ... ")
    print(f"ENDPOINT  : {os.getenv('ENDPOINT')!r}")
    print(f"API_VERSION : {os.getenv('API_VERSION')!r}")
    print(f"GPT5_MODEL: {os.getenv('GPT5_MODEL')!r}")
    print(f"API_KEY : {api_key_mascarada}")
    print("------------------------------------")

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
                ]
  
            )

            resposta_texto = response.choices[0].message.content
            print(f"\nResposta:\n{resposta_texto}")

        except APIError as e:
        
            print(f"\n[Erro na API]: {e}")
        except Exception as e:
            print(f"\n[Erro inesperado]: {e}")


if __name__ == "__main__":
    main()
