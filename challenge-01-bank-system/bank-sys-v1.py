cliente_banco = input("Digite seu nome: ")

# mensagem exibida a cada execução no loop while
menu = f"""
Olá {cliente_banco}, o que deseja fazer hoje? (digite uma letra)

[d] - depositar
[s] - sacar
[e] - extrato
[q] - sair

=> """

# Variáveis utilizadas:
saldo = 0
extrato = ''
contagem_saques = 0
SAQUES_DISPONIVEIS_POR_DIA = 3
LIMITE_POR_SAQUE = 500.00

# Execução da interface:
while True:
    opcao = input(menu)  # recebe do teclado a escolha do cliente bancário

    if opcao == 'd':
        # lógica de déposito
        valor_deposito = float(
            input("\nQual o valor desejado para depósito: R$ "))

        if valor_deposito > 0:
            # efetuar depósito
            saldo += valor_deposito
            # adiciona ao extrato a movimentação
            extrato += f"\n========================================\n(depósito)\t⬆ R$ +{valor_deposito:.2f}"
            # mensagem de sucesso:
            print("""==================================\nDepósito efetuado com sucesso!\n==================================""")

        else:
            # caso a tentativa de depósito seja de valor negativo:
            print(f"\n{'=' * 80}\n"
                  f"[ERRO] Não é possível depositar esse valor [R$ {valor_deposito:.2f}]"
                  f"\n{'=' * 80}\n")

    elif opcao == 's':
        # lógica de saque
        valor_saque = float(input("Qual o valor desejado para saque: R$ "))

        valor_saque_positivo = True if valor_saque > 0 else False
        requisito_para_saque_atingido = (contagem_saques < SAQUES_DISPONIVEIS_POR_DIA) and (
            valor_saque <= LIMITE_POR_SAQUE)
        
        if valor_saque_positivo and requisito_para_saque_atingido:
            # efetua saque se valor de saque é menor ou igual que o saldo da conta  
            if valor_saque <= saldo:
                saldo -= valor_saque
                # contabiliza o saque
                contagem_saques += 1
                # adiciona ao extrato a movimentação
                extrato += f"\n========================================\n(saque)\t\t⬇ R$ -{valor_saque:.2f}"
                # mensagem de sucesso
                print("""==================================\nSaque efetuado com sucesso!\n==================================""")
            else:
                print(f"{"=" * 80}"
                  f"\n[Ops...] Saldo insuficiente! Valor disponível em conta: {saldo}\n"
                  f"{"=" * 80}")
        
        # verificação se atingiu a quantidade de saques diários
        elif valor_saque_positivo and (contagem_saques == SAQUES_DISPONIVEIS_POR_DIA) and (valor_saque <= LIMITE_POR_SAQUE):
            print(f"{"=" * 80}"
                  f"\n[Ops...] Você já atingiu seu limite de saques diários: {contagem_saques}\n"
                  f"{"=" * 80}")

        # verificação se ultrapassa o valor limite de saque por operação
        elif valor_saque_positivo and (valor_saque > LIMITE_POR_SAQUE) and (contagem_saques < SAQUES_DISPONIVEIS_POR_DIA):
            print(f"\n{'=' * 80}\n"
                  f"[Ops...] Seu valor R$ {valor_saque} de saque ultrapassa o limite permitido por operação: {LIMITE_POR_SAQUE:.2f}"
                  f"\n{'=' * 80}\n")

        # caso não atinja nenhum dos dois requisitos para saque 
        else:
            print(f"\n{'=' * 100}\n"
                  f"[ERRO] Você não tem os requisitos para essa operação:\nvalor de saque desejado deve estar dentro do limite [ R$ 1.00 a R${LIMITE_POR_SAQUE:.2f} ] e\nquantidade de saques feitos ( {contagem_saques} vezes ) deve ser menor que [ Número de Saques por dia: {SAQUES_DISPONIVEIS_POR_DIA} ]"
                  f"\n{'=' * 100}\n")

    elif opcao == 'e':
        # lógica de impressão de extrato
        if extrato != '':
            print("\n\t\tEXTRATO" + extrato)
            print("\n========================================\n" + f"Saldo da Conta: R$ {saldo:.2f}\n")

        else:
            print(
                "\n" + "[MENSAGEM DO SISTEMA] Não foram realizadas movimentações" + "\n")

    elif opcao == 'q':
        print("[MENSAGEM DO SISTEMA] saindo da aplicação...")
        break

    else:
        print(
            "\n" + "[MENSAGEM DO SISTEMA] Você não escolheu um opção válida, tente novamente!" + "\n")
