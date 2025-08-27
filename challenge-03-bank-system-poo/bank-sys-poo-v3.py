# Versão 3 do Sistema Bancário, com uso de funções
from abc import ABC, abstractmethod     # para gerar classes abstratas classe abstrata

# ✅ Cliente
class Cliente:
    # inicializa os atributos do objeto instanciado
    def __init__(self, endereco):
        self._endereco = endereco   # str
        self._contas = []   # list
    
    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# ✅ PessoaFisica
class PessoaFisica(Cliente):
    # inicializa os atributos do objeto instanciado
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf     # str
        self._nome = nome   # str
        self._data_nascimento = data_nascimento     # date

    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento
    
    @property
    def endereco(self):
        return self._endereco

# ✅ Histórico
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        if transacao.__class__.__name__ == "Deposito":
            self._transacoes.append(
                {"tipo": transacao.__class__.__name__,
                "valor": transacao.valor}
            )

        elif transacao.__class__.__name__ == "Saque":
            self._transacoes.append(
                {"tipo": transacao.__class__.__name__,
                "valor": transacao.valor}
            )
        else:
            pass

# ✅ Conta
class Conta:
    # atributos de classe
    AGENCIA = "0001"
    # inicializa uma instância da classe
    def __init__(self, cliente, numero):
        # atributos do objeto
        self._saldo = 0.0       # float
        self._numero = numero   # int
        self._agencia = Conta.AGENCIA   # str
        self._cliente = cliente         # instância de Cliente
        self._historico = Historico()   # instância de Historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)     #  return Conta
    
    @property
    def saldo(self):
        return self._saldo      # return float
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    # ✅ método sacar
    def sacar(self, valor):
        saldo = self.saldo
        valor_saque_positivo = True if valor > 0 else False
        valor_excede_saldo = True if valor > saldo else False

        if valor_saque_positivo and not valor_excede_saldo:
            self._saldo -= valor
            print("""==================================\nSaque efetuado com sucesso!\n==================================""")
            return True
        elif valor_saque_positivo and valor_excede_saldo:
            print(f"{"=" * 80}"
                  f"\n[Ops...] Saldo insuficiente! Valor disponível em conta: R$ {saldo:.2f}\n"
                  f"{"=" * 80}")
        else:
            print(f"{"=" * 80}"
                  f"\n[ERRO] Valor informado para saque é inválido: R$ {valor}\n"
                  f"{"=" * 80}")

        return False
    
    # ✅ método depositar
    def depositar(self, valor):
        valor_deposito_positivo = True if valor > 0 else False
        
        if valor_deposito_positivo:
            self._saldo += valor
            print("""==================================\nDepósito efetuado com sucesso!\n==================================""")
            return True
        else:
            print(f"\n{'=' * 80}\n"
              f"[ERRO] Não é possível depositar esse valor [R$ {valor:.2f}]"
              f"\n{'=' * 80}\n") 

        return False

# ✅ ContaCorrente
class ContaCorrente(Conta):
    # atributos de classe:
    SAQUES_DISPONIVEIS_POR_DIA = 3
    LIMITE_POR_SAQUE = 500.00

    # inicializa os atributos do objeto
    def __init__(self, cliente, numero, limite=LIMITE_POR_SAQUE, limite_saques=SAQUES_DISPONIVEIS_POR_DIA):
        super().__init__(cliente, numero)
        self._limite = limite       # float
        self._limite_saques = limite_saques     # int

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques

    # sobrescreve o método sacar
    def sacar(self, valor):
        quantidade_de_saques = 0
        for transacao in self.historico.transacoes:
            if transacao["tipo"] == Saque.__name__:
                quantidade_de_saques += 1
        
        saque_desejado_excede_limite_saques = True if quantidade_de_saques >= self.limite_saques else False
        valor_desejado_excede_valor_limite = True if valor > self.limite else False

        if not saque_desejado_excede_limite_saques and not valor_desejado_excede_valor_limite:
            return super().sacar(valor)
        elif saque_desejado_excede_limite_saques and not valor_desejado_excede_valor_limite:
            print(f"{"=" * 80}"
              f"\n[Ops...] Você já sacou '{quantidade_de_saques} vez(es)' e atingiu seu limite de saques diários: {self.limite_saques}\n"
              f"{"=" * 80}")
        elif not saque_desejado_excede_limite_saques and valor_desejado_excede_valor_limite:
            print(f"\n{'=' * 80}\n"
              f"[Ops...] Seu valor R$ {valor:.2f} de saque ultrapassa o limite permitido por operação: R$ {self.limite:.2f}"
              f"\n{'=' * 80}\n")
        else:
            # não atingiu nenhum dos dois requisitos para o saque
            print(f"\n{'=' * 100}\n"
              f"[ERRO] Você não tem os requisitos para essa operação:\nvalor de saque desejado deve estar dentro do limite [ R$ 1.00 a R$ {self.limite:.2f} ] e\nquantidade de saques feitos ( {quantidade_de_saques} vezes ) deve ser menor que [ Número de Saques por dia: {self.limite_saques} ]"
              f"\n{'=' * 100}\n")
        return False

# ✅ Transacao é interface
class Transacao(ABC):

    @abstractmethod
    def registrar(self, conta: Conta):
        pass

# ✅ Implementa o método registrar da classe abstrata Transacao
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor     # float

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_no_deposito = conta.depositar(self.valor)

        if sucesso_no_deposito:
            conta.historico.adicionar_transacao(self)


# ✅ Implementa o método registrar da classe abstrata Transacao
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_no_saque = conta.sacar(self.valor)

        if sucesso_no_saque:
            conta.historico.adicionar_transacao(self)

# ✅
def menu(cliente):
    # exibe opções da conta bancária
    return f"""\n{" MENU ":=^56}
Olá {cliente}, o que deseja fazer hoje?\n(digite uma letra)

[d] - depositar
[s] - sacar
[e] - extrato
[n] - nova conta
[l] - listar contas
[q] - sair

=> """

# ✅
def criar_cliente(cpf):
    nome = input("Digite seu nome: ").title().strip()
    data_nascimento = input(
        "Digite sua data de nascimento (ex.: dd/mm/aaaa): ").strip()
    endereco = input(
        "Endereço (ex.: logradouro, nro - bairro - cidade/sigla_estado): ").strip()

    # retorna uma instância de classe
    return PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)

# ✅
def criar_conta_corrente(cliente, numero_conta):
    # criar uma instância de conta passando o objeto cliente como atributo dela
    nova_conta_do_cliente = ContaCorrente(cliente=cliente, numero=numero_conta)

    # adicionar nova conta do cliente a sua lista de contas, ou seja, seu atributo contas
    cliente.adicionar_conta(conta=nova_conta_do_cliente)

    # retorna o objeto conta que foi criado, para ser adicionado na lista de contas do banco, onde ficam todas as contas de todos os clientes
    return nova_conta_do_cliente

# ✅
def escolher_conta(cliente):
    if len(cliente.contas):
        print("="*80 + f"\nVocê tem {len(cliente.contas)} contas:\n")
        for conta in cliente.contas:
            print(f"Agência: {conta.agencia:^12} -\tNúmero da Conta:\t{conta.numero}\n" + "="*80)
        selecionada = int(input(
            "\nEscolha em qual conta quer fazer a operação (apenas o número da conta):\n").strip())
        for conta in cliente.contas:
            if conta.numero == selecionada:
                return conta
            else:
                print("\n[MENSAGEM DO SISTEMA] Você não escolheu um número da conta válido\n")
                return 0
    else:
        print("\n[MENSAGEM DO SISTEMA] Você não tem contas, considere criar uma....\n")
        return 0    # mesmo que False

# ✅
def exibir_extrato(conta):
    transacoes = conta.historico.transacoes
    saldo = conta.saldo
    
    print("\n" + "="*15 + " EXTRATO " + "="*15 + "\n")
    extrato = ""
    if transacoes:
        transacoes_detalhadas = [f"{transacao["tipo"]:^8} \tR$ {transacao["valor"]:.2f}" for transacao in transacoes]
        extrato = "\n\n".join(transacoes_detalhadas)   
        print(extrato)    
    else:
        print(
            "\n" + "[MENSAGEM DO SISTEMA] Não foram realizadas movimentações" + "\n")
    print("\n========================================\n" + f"Saldo da Conta: R$ {saldo:.2f}\n")
    print()

# ✅
def listar_contas(contas):
    for conta in contas:
        print(f"{'='*80}\n"
              f"Agência: {conta.agencia}\n"
              f"Número da Conta: {conta.numero}\n"
              f"Cliente: {conta.cliente.nome}\n"
              f"{'='*80}"
              )
# Função que inicia a execução do programa:

def main():
    clientes = []
    contas = []

    while True:
        tipo_acesso = input("\n" + "Bem-vindo ao Banco" + "\n"
                            "Digite:" + "\n"
                            "[1] - Acessar cadastro\n"
                            "[2] - Criar novo cadastro\n"
                            "[3] - Listar contas de clientes\n"
                            "[4] - Fechar\n"
                            "=> ")
        # ✅ Feito:
        if tipo_acesso == '1':  # Acessar cadastro
            # passar nome e fazer login mediante a lista de clientes
            cpf_cliente = input(
                "Para acessar, digite o CPF (somente números): ").strip()
            cliente_logado = False
            for cliente in clientes:    # cliente é objeto
                print(cliente.cpf)
                if cpf_cliente == cliente.cpf:
                    cliente_logado = cliente
            if cliente_logado:
                while True:
                    opcao = input(menu(cliente=cliente_logado.nome))
                    if opcao == 'd':    # ✅ depositar
                        conta_escolhida = escolher_conta(cliente=cliente_logado)
                        if conta_escolhida:
                            valor_deposito = float(input("\nQual o valor desejado para depósito: R$ ").strip())
                            transacao_de_deposito = Deposito(valor = valor_deposito)
                            # cliente realiza a transação
                            cliente_logado.realizar_transacao(conta = conta_escolhida, transacao = transacao_de_deposito)
                            
                    elif opcao == 's':  # ✅ sacar
                        conta_escolhida = escolher_conta(cliente=cliente_logado)
                        if conta_escolhida:
                            valor_saque = float(input("\nQual o valor desejado para saque: R$ ").strip())
                            transacao_de_saque = Saque(valor = valor_saque)
                            # cliente realiza a transação
                            cliente_logado.realizar_transacao(conta = conta_escolhida, transacao = transacao_de_saque)
                    elif opcao == 'e':  # ✅ exibir extrato
                        conta_escolhida = escolher_conta(cliente=cliente_logado)
                        if conta_escolhida:
                            exibir_extrato(conta=conta_escolhida)

                    elif opcao == 'n':  # ✅ criar nova conta
                        numero_conta = len(contas) + 1
                        nova_conta = criar_conta_corrente(cliente_logado, numero_conta)
                        contas.append(nova_conta)
                        print(
                            "\n[MENSAGEM DO SISTEMA] Nova conta criada com sucesso...\n")
                    elif opcao == 'l':  # ✅ listar contas do cliente logado
                        contas_do_cliente_logado = cliente_logado.contas
                        if contas_do_cliente_logado:
                            listar_contas(contas_do_cliente_logado)
                        else:
                            print("\n[MENSAGEM DO SISTEMA] Não há contas a serem listadas...\n")
                    elif opcao == 'q':  # ✅ sair da área do cliente
                        print(
                            f"\n[MENSAGEM DO SISTEMA] Fechando Sessão do Cliente {cliente_logado.nome}...\n")
                        break
                    else:
                        print(
                            "\n" + "[MENSAGEM DO SISTEMA] Você não escolheu um opção válida, tente novamente!" + "\n")
            else:
                print(
                    f"\n[MENSAGEM DO SISTEMA] Esse CPF {cpf_cliente} não foi encontrado em nossa base de dados! Considere escolher outra opção!\n")

        # ✅ Feito:
        elif tipo_acesso == "2":    # Criar novo cadastro
            cpf_novo_cliente = input("CPF (somente números): ").strip()

            if clientes:
                cpf_existente = False
                for cliente in clientes:
                    # verifica na lista de clientes se já há cadastro com o mesmo cpf, cada cliente é um dicionário com valores acessáveis por chave
                    if cpf_novo_cliente == cliente.cpf:
                        print(
                            "\n[MENSAGEM DO SISTEMA] CPF já cadastrado para outro usuário! Não é permitido cadastrar com o mesmo CPF\n")
                        cpf_existente = True
                        break
                    
                if not cpf_existente:
                    novo_cliente = criar_cliente(cpf_novo_cliente)
                    clientes.append(novo_cliente)
                    print(f"\n[MENSAGEM DO SISTEMA] Novo cliente [{novo_cliente.nome}] cadastrado com sucesso!\n")
            else:
                novo_cliente = criar_cliente(cpf_novo_cliente)
                clientes.append(novo_cliente)
                print(f"\n[MENSAGEM DO SISTEMA] Novo cliente [{novo_cliente.nome}] cadastrado com sucesso!\n")

        # ✅ Feito:
        elif tipo_acesso == "3":    # listar todas as contas do banco e seus respectivos clientes
            if contas:
                listar_contas(contas)
            else:
                print("\n[MENSAGEM DO SISTEMA] Não há contas a serem listadas...\n")

        # ✅ Feito:
        elif tipo_acesso == "4":    # Fechar
            break
        else:
            print(
                "\n" + "[MENSAGEM DO SISTEMA] Você não escolheu um opção válida, tente novamente!" + "\n")
#
# Começo do programa, chamada da função principal:
#
main()