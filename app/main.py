from agent import executar_agente

if __name__ == "__main__":
    print("=== Curador de Notícias Tech Inicializado ===")
    print("Digite 'sair' para encerrar o programa.\n")
    
    while True:
        entrada = input("\nPergunte algo sobre tecnologia: ")
        if entrada.lower() == 'sair':
            print("Encerrando o agente. Até logo!")
            break
        if entrada.strip() == "":
            continue
            
        executar_agente(entrada)