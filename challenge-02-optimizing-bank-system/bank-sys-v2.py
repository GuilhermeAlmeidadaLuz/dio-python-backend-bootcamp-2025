# Versão 2 do Sistema Bancário, com uso de funções

def menu(cliente):
    # exibe opções da conta bancária
    return f"""\n{" MENU ":=^56}
Olá {cliente}, o que deseja fazer hoje? (digite uma letra)

[d] - depositar
[s] - sacar
[e] - extrato
[n] - nova conta
[l] - listar contas
[q] - sair

=> """


def criar_usuario():
    # cria um cliente do banco (como um dicionário)
    # 1. armazenar usuário em uma lista
    # 2. usuário: nome, data de nascimento, cpf e endereço
    # 3. endereço é string com formato: logradouro, nro - bairro - cidade/sigla_estado
    # 4. CPF somente em números, como string
    # 5. Um CPF para um Cliente, não permite cadastrar o mesmo CPF para dois clientes diferentes, retornar msg de erro
    # cria somente as chaves e atribui None a elas por padrão
    cliente = dict.fromkeys(
        ["nome", "data de nascimento", "cpf", "endereco"], None)
    cliente["nome"] = input("Digite seu nome: ").title()
    cliente["data de nascimento"] = input(
        "Digite sua data de nascimento (ex.: dd/mm/aaaa): ")
    cliente["cpf"] = input("CPF (somente números): ")
    cliente["endereco"] = input(
        "Endereço (ex.: logradouro, nro - bairro - cidade/sigla_estado): ")

    return cliente


def criar_conta_corrente(agencia, numero_da_conta, usuario_da_conta, saldo_da_conta, extrato_da_conta):
    # vincular conta a usuário existente, que foi criado
    # Dica: Para vincular um usuário a uma conta, filtre a lista de usuários buscando o número do CPF informado para cada usuário da lista

    conta = {}.fromkeys(["agencia", "numero da conta",
                        "usuario", "saldo da conta", "extrato da conta"])
    conta["agencia"] = agencia
    conta["numero da conta"] = numero_da_conta
    conta["usuario"] = usuario_da_conta
    conta["saldo da conta"] = saldo_da_conta
    conta["extrato da conta"] = extrato_da_conta

    return conta
    # 1. armazenar contas em uma lista
    # 2. composição da conta: agência, número da conta e usuário
    # 3. o número da conta é sequencial, iniciando em 1
    # 4. o número da agência é fixo (ex.: "0001")
    # 5. o usuário pode ter mais de uma conta, mas uma conta pertence a somente um usuário


def escolher_conta(usuario, contas):
    quantidade_contas = 0
    contas_do_usuario = []
    for indice, conta in enumerate(contas):
        if usuario is conta["usuario"]:
            quantidade_contas += 1
            contas_do_usuario.append(
                f"{indice}: CC {conta["numero da conta"]}")
    if quantidade_contas:
        selecionada = int(input(
            f"\nVocê tem {quantidade_contas} contas, digite o índice dela:\n{"\n".join(contas_do_usuario)}\n=> "))

        return contas[selecionada]
    else:
        print("\n[MENSAGEM DO SISTEMA] Você não tem contas, considere criar uma....\n")
        return 0    # mesmo que False


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    # argumentos por nome, keyword-only

    # lógica de saque
    valor_saque_positivo = True if valor > 0 else False
    requisito_para_saque_atingido = (numero_saques < limite_saques) and (
        valor <= limite)

    if valor_saque_positivo and requisito_para_saque_atingido:
        # efetua saque se valor de saque é menor ou igual que o saldo da conta
        if valor <= saldo:
            saldo -= valor
            # contabiliza o saque
            # numero_saques += 1    # não funciona dentro da função pois vem do escopo main(), logo é preciso atualizar lá
            # adiciona ao extrato a movimentação
            extrato += f"\n========================================\n(saque)\t\t⬇ R$ -{valor:.2f}"
            # mensagem de sucesso
            print("""==================================\nSaque efetuado com sucesso!\n==================================""")
        else:
            print(f"{"=" * 80}"
                  f"\n[Ops...] Saldo insuficiente! Valor disponível em conta: {saldo:.2f}\n"
                  f"{"=" * 80}")

        # verificação se atingiu a quantidade de saques diários
    elif valor_saque_positivo and (numero_saques == limite_saques) and (valor <= limite):
        print(f"{"=" * 80}"
              f"\n[Ops...] Você já atingiu seu limite de saques diários: {numero_saques}\n"
              f"{"=" * 80}")

        # verificação se ultrapassa o valor limite de saque por operação
    elif valor_saque_positivo and (valor > limite) and (numero_saques < limite_saques):
        print(f"\n{'=' * 80}\n"
              f"[Ops...] Seu valor R$ {valor:.2f} de saque ultrapassa o limite permitido por operação: {limite:.2f}"
              f"\n{'=' * 80}\n")

        # caso não atinja nenhum dos dois requisitos para saque
    else:
        print(f"\n{'=' * 100}\n"
              f"[ERRO] Você não tem os requisitos para essa operação:\nvalor de saque desejado deve estar dentro do limite [ R$ 1.00 a R${limite:.2f} ] e\nquantidade de saques feitos ( {numero_saques} vezes ) deve ser menor que [ Número de Saques por dia: {limite_saques} ]"
              f"\n{'=' * 100}\n")

    # retorno da operação
    return saldo, extrato


def depositar(saldo, valor, extrato, /):
    # argumentos por posição, positional-only

    # lógica de depósito
    if valor > 0:
        # efetuar depósito
        saldo += valor
        # adiciona ao extrato a movimentação
        extrato += f"\n========================================\n(depósito)\t⬆ R$ +{valor:.2f}"
        # mensagem de sucesso:
        print("""==================================\nDepósito efetuado com sucesso!\n==================================""")
    else:
        # caso a tentativa de depósito seja de valor negativo:
        print(f"\n{'=' * 80}\n"
              f"[ERRO] Não é possível depositar esse valor [R$ {valor:.2f}]"
              f"\n{'=' * 80}\n")

    # retorno da operação
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    # argumento posicional: saldo (positional only), argumento nomeado: extrato (keyword only)
    # lógica de impressão de extrato
    if extrato != '':
        print("\n\t\tEXTRATO" + extrato)
        print("\n========================================\n" + f"Saldo da Conta: R$ {saldo:.2f}\n")
    else:
        print(
            "\n" + "[MENSAGEM DO SISTEMA] Não foram realizadas movimentações" + "\n")
    # lógica de exibição do extrato
    print()


def listar_contas(contas):
    for conta in contas:
        print(f"{'='*80}\n"
              f"Agência: {conta["agencia"]}\n"
              f"Número da Conta: {conta["numero da conta"]}\n"
              f"Cliente: {conta["usuario"]["nome"]}\n"
              f"{'='*80}"
              )
# Função que inicia a execução do programa:

def main():
    saldo = 0
    extrato = ''
    contagem_saques = 0
    AGENCIA = "0001"
    SAQUES_DISPONIVEIS_POR_DIA = 3
    LIMITE_POR_SAQUE = 500.00
    usuarios = []
    contas = []

    while True:
        tipo_acesso = input("\n" + "Bem-vindo ao Banco" + "\n"
                            "Digite:" + "\n"
                            "[1] - Acessar cadastro\n"
                            "[2] - Criar novo cadastro\n"
                            "[3] - Fechar\n"
                            "=> ")
        # ✅ Feito:
        if tipo_acesso == '1':  # Acessar cadastro
            # passar nome e fazer login mediante a lista de usuarios
            cpf_cliente = input(
                "Para acessar, digite o CPF (somente números): ")
            usuario_logado = {}
            for usuario in usuarios:    # usuário é dicionário
                if cpf_cliente in usuario["cpf"]:
                    usuario_logado = usuario
            if usuario_logado:
                while True:
                    cliente = usuario_logado["nome"]
                    opcao = input(menu(cliente=cliente))
                    if opcao == 'd':    # depositar
                        conta_escolhida = escolher_conta(usuario_logado, contas)
                        if conta_escolhida:
                            valor_deposito = float(input("\nQual o valor desejado para depósito: R$ "))
                            conta_escolhida["saldo da conta"], conta_escolhida["extrato da conta"] = depositar(
                                conta_escolhida["saldo da conta"],
                                valor_deposito,
                                conta_escolhida["extrato da conta"]
                            )
                    elif opcao == 's':  # sacar
                        conta_escolhida = escolher_conta(usuario_logado, contas)
                        if conta_escolhida:
                            valor_saque = float(input("\nQual o valor desejado para saque: R$ "))

                            conta_escolhida["saldo da conta"], conta_escolhida["extrato da conta"] = sacar(
                                saldo = conta_escolhida["saldo da conta"], 
                                valor = valor_saque, 
                                extrato = conta_escolhida["extrato da conta"], 
                                limite = LIMITE_POR_SAQUE, 
                                numero_saques = contagem_saques, 
                                limite_saques = SAQUES_DISPONIVEIS_POR_DIA
                            )
                            contagem_saques += 1
                    elif opcao == 'e':  # exibir extrato
                        conta_escolhida = escolher_conta(usuario_logado, contas)
                        if conta_escolhida:
                            exibir_extrato(conta_escolhida["saldo da conta"], extrato=conta_escolhida["extrato da conta"])

                    elif opcao == 'n':  # criar nova conta
                        numero_conta = len(contas) + 1
                        conta = criar_conta_corrente(
                            agencia=AGENCIA,
                            numero_da_conta=numero_conta,
                            usuario_da_conta=usuario_logado,
                            saldo_da_conta=saldo,
                            extrato_da_conta=extrato
                        )
                        contas.append(conta)
                        print(
                            "\n[MENSAGEM DO SISTEMA] Nova conta criada com sucesso...\n")
                    elif opcao == 'l':  # listar contas
                        if contas:
                            listar_contas(contas)
                        else:
                            print("\n[MENSAGEM DO SISTEMA] Não há contas a serem listadas...\n")
                    elif opcao == 'q':  # sair da área do cliente
                        contagem_saques = 0
                        print(
                            f"\n[MENSAGEM DO SISTEMA] Fechando Sessão do Cliente {usuario_logado["nome"]}...\n")
                        break
                    else:
                        print(
                            "\n" + "[MENSAGEM DO SISTEMA] Você não escolheu um opção válida, tente novamente!" + "\n")
            else:
                print(
                    f"\n[MENSAGEM DO SISTEMA] Esse CPF {cpf_cliente} não foi encontrado em nossa base de dados! Considere escolher outra opção!\n")

        # ✅ Feito:
        elif tipo_acesso == "2":    # Criar novo cadastro
            novo_cliente = criar_usuario()

            cpf_existente = False
            for usuario in usuarios:
                # verifica na lista de usuarios se já há cadastro com o mesmo cpf, cada usuario é um dicionário com valores acessáveis por chave
                if novo_cliente["cpf"] in usuario["cpf"]:
                    print(
                        "\n[MENSAGEM DO SISTEMA] CPF já cadastrado para outro usuário! Não é permitido cadastrar com o mesmo CPF\n")
                    cpf_existente = True
                    break

            if not cpf_existente:
                usuarios.append(novo_cliente)

        # ✅ Feito:
        elif tipo_acesso == "3":    # Fechar
            break
        else:
            print(
                "\n" + "[MENSAGEM DO SISTEMA] Você não escolheu um opção válida, tente novamente!" + "\n")
#
# Começo do programa, chamada da função principal:
#
main()
