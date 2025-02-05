import os

from colorama import init, Fore, Back, Style
init()

# dicionário que serve como banco de dados
usuarios = {}

def validar_senha(senha):
    """Função para validar a quantidade de caracteres inseridos pelo usuário"""
    return len(senha) >= 8

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastrar_usuario():
    """Função que insere os dados cadastrados pelo usuário no dicionário"""
    print("\n————————— Cadastro de Usuário —————————")
    nome = None  # inicializa o nome como None fora do loop para o código saber se o nome já foi validado ou precisa ser solicitado novamente, pra evitar repetições desnecessárias

    while True:
        if not nome:
            nome = input("\nDigite um nome de usuário: ").strip()
            if not nome:
                print("\nNome de usuário não pode estar vazio. Insira um nome válido.")
                nome = None
                continue 
            if nome in usuarios:
                print("\nNome de usuário já existe. Escolha outro.")
                nome = None
                continue
        
        senha = input("\nDigite uma senha (mínimo 8 caracteres): ").strip()
        if not validar_senha(senha):
            print("\nSenha inválida. Deve ter pelo menos 8 caracteres.")
            continue
        
        senha_confirmada = input("\nConfirme a senha: ").strip()
        if senha != senha_confirmada:
            print("\nAs senhas não coincidem. Tente novamente.")
            continue

        usuarios[nome] = {"senha": senha, "atividades": []} # create
        print(f"Usuário '{nome}' cadastrado com sucesso!") # read
        clear()
        break

def login():
    """Função que define o usuário atual a partir da validação dos dados inseridos com os dados cadastrados"""
    print("\n———————————————— Login ————————————————")
    nome = input("Nome de usuário: ").strip()
    senha = input("Senha: ").strip()
    
    if nome in usuarios and usuarios[nome]["senha"] == senha:
        print(f"\nBem-vindo, {nome}!")
        return nome
    print("\nCredenciais inválidas. Tente novamente.")
    return None

def adicionar_atividade(usuario):  # create
    """Função que adiciona uma atividade ao dicionário do usuário logado"""
    print("\n————————— Adicionar Atividade —————————")
    nome_atividade = input("\nNome da Atividade: ").strip()
    if not nome_atividade:
        print("\nNome da atividade não pode estar vazio.")
        return

    print("\nTipo de Atividade:")
    print("[1] Hábito (atividade que se repete)")
    print("[2] Tarefa única")
    print("[3] Checklist (lista de itens a serem concluídos)")
    tipo = input("\nEscolha o tipo: ").strip()
    
    if tipo not in ("1", "2", "3"):
        print("\n *Opção inválida.")
        return

    frequencia = None
    dias_especificos = None
    checklist = []

    if tipo == "1":  # hábito
        print("\nCom que frequência você deseja realizar esse hábito:")
        print("[1] Todos os dias")
        print("[2] Dias específicos")
        frequencia = input("\nEscolha uma opção: ").strip()

        if frequencia == "2": # dias específicos
            print("\nEscolha os dias da semana (exemplo: 2,4,6 para segunda, quarta e sexta):")
            print("[1] Domingo")
            print("[2] Segunda")
            print("[3] Terça")
            print("[4] Quarta")
            print("[5] Quinta")
            print("[6] Sexta")
            print("[7] Sábado")

            dias_input = input("\nInforme os números dos dias separados por vírgula: ").strip()
            dias_especificos = dias_input.split(',')
            dias_validos = []

            for dia in dias_especificos:
                if dia.isdigit():  # verifica se é um número
                    numero_dia = int(dia)
                    if 1 <= numero_dia <= 7:  # verifica se está entre 1 e 7
                        dias_validos.append(numero_dia)

            if not dias_validos:
                print("\nNenhum dia válido selecionado. Frequência definida como 'Todos os dias'.")
                frequencia = "1"
            else:
                dias_especificos = dias_validos
        else:
            dias_especificos = None

    elif tipo == "3":  # checklist
        print("\nInsira os itens do checklist (digite 'fim' para encerrar):")
        checklist = []
        while True:
            item = input("Item: ").strip()
            if item.lower() == "fim":
                break
            elif item:  # verifica se não está vazio
                checklist.append({"item": item, "concluido": False})
            else:
                print("O item não pode estar vazio. Tente novamente.")

# adicionando a atividade ao dicionário

    if tipo == "1":
        tipo_atividade = "Hábito"
    elif tipo == "2":
        tipo_atividade = "Tarefa"
    elif tipo == "3":
        tipo_atividade = "Checklist"

    if frequencia == "1":
        frequencia_atividade = "Todos os dias"
    elif frequencia == "2":
        frequencia_atividade = "Dias específicos"
    else:
        frequencia_atividade = None

    usuarios[usuario]["atividades"].append({
        "nome": nome_atividade,
        "tipo": tipo_atividade,
        "frequencia": frequencia_atividade,
        "dias_especificos": dias_especificos if tipo == "1" and frequencia == "2" else None,
        "checklist": checklist if tipo == "3" else None,
        "historico": []
    })

    print(f"\nAtividade '{nome_atividade}' adicionada com sucesso!")

def mostrar_atividades(usuario):  # read
    """Função que exibe as atividades do usuário e os itens do checklist"""
    print("\n———————— Atividades Cadastradas ————————")
    atividades = usuarios[usuario]["atividades"]

    if not atividades:
        print("\nNenhuma atividade cadastrada.")
        return

    for i, atividade in enumerate(atividades, 1):
        print(Style.RESET_ALL+Fore.WHITE+f"[{i}] {atividade['nome']} ({atividade['tipo']})")
        
        # se a atividade for do tipo checklist exibe os itens
        if atividade["tipo"] == "Checklist" and "checklist" in atividade:
            print("\n  Itens do Checklist:")
            for item in atividade["checklist"]:
                status = Fore.LIGHTGREEN_EX+"(Concluído [ \u2714 ])" if item["concluido"] else Fore.RED+"(Pendente [ \u2716 ])"
                print(Style.RESET_ALL+Fore.WHITE+f"    - {item['item']} {status}")

def edit_delete_atividade(usuario): # update e delete
    """Função que permite o usuário editar ou excluir atividades do dicionário"""
    mostrar_atividades(usuario)
    atividades = usuarios[usuario]["atividades"]
    if not atividades:
        return

    escolha = input("\nEscolha o número da atividade que deseja atualizar ou excluir: ").strip()
    if not escolha.isdigit() or int(escolha) not in range(1, len(atividades) + 1):
        print("\n *Opção inválida.")
        return

    escolha = int(escolha) - 1
    print("\n[1] Editar\n[2] Excluir")
    acao = input("Escolha uma ação: ").strip()

# *as escolhas tem +1 e -1 porque pro usuário a contagem é iniciada do número 1 mas no índice de listagem por padrão a contagem começa pelo 0

    if acao == "1":
        novo_nome = input("Novo nome para a atividade: ").strip()
        if novo_nome:
            atividades[escolha]["nome"] = novo_nome
            print("\nAtividade atualizada com sucesso!")
        else:
            print("\nO nome não pode ser vazio.")
    elif acao == "2":
        atividades.pop(escolha)
        print("\nAtividade excluída com sucesso!")
    else:
        print("\nAção inválida.")

def marcar_concluida(usuario):
    """Função que permite ao usuário marcar as atividades como concluídas"""
    mostrar_atividades(usuario)
    atividades = usuarios[usuario]["atividades"]
    if not atividades:
        return

    escolha = input(Style.RESET_ALL+Fore.WHITE+"\nEscolha o número da atividade que deseja marcar como concluída: ").strip()
    if not escolha.isdigit() or int(escolha) not in range(1, len(atividades) + 1):
        print("\n *Opção inválida.")
        return

    escolha = int(escolha) - 1
    atividade = atividades[escolha]
    
    if atividade["tipo"] == "Checklist":
        # se for uma Checklist mostra os itens
        print(f"\nAtividade: {atividade['nome']}")
        print("Itens do checklist:")
        for i, item in enumerate(atividade["checklist"], 1):
            status = Fore.LIGHTGREEN_EX+"Concluído [ \u2714 ]" if item["concluido"] else Fore.RED+"Pendente [ \u2716 ]"
            print(Style.RESET_ALL+Fore.WHITE+f"[{i}] {item['item']} - {status}")             
        # pergunta ao usuário qual item ele deseja marcar como concluído
        item_escolhido = input(Style.RESET_ALL+Fore.WHITE+"\nEscolha o número do item para marcar como concluído ou digite 'fim' para finalizar: ").strip()
        if item_escolhido.lower() == "fim":
            print("\nOperação finalizada.")
            return

        if not item_escolhido.isdigit() or int(item_escolhido) not in range(1, len(atividade["checklist"]) + 1):
            print("\n *Opção inválida.")
            return

        item_escolhido = int(item_escolhido) - 1
        atividade["checklist"][item_escolhido]["concluido"] = True
        print(f"\nItem '{atividade['checklist'][item_escolhido]['item']}' marcado como concluído!")

    else: # caso a atividade não seja do tipo checklist, marca a atividade como concluída normalmente
        data = input("\nInforme a data da conclusão: ").strip()
        atividade["historico"].append(data)
        print(f"\nAtividade '{atividade['nome']}' marcada como concluída: {data}!")

        if atividade["tipo"] == "Tarefa":
            atividades.pop(escolha)
        #  linha para atividades únicas que depois de concluídas são apagadas do bd

def historico(usuario):
    """Função que permite o usuário visualizar quantas vezes uma atividade foi concluída"""
    mostrar_atividades(usuario)
    atividades = usuarios[usuario]["atividades"]
    if not atividades:
        return

    escolha = input("Escolha o número da atividade para visualizar o histórico: ").strip()
    if not escolha.isdigit() or int(escolha) not in range(1, len(atividades) + 1):
        print("\n *Opção inválida.")
        return

    escolha = int(escolha) - 1
    atividade = atividades[escolha]
    
    if atividade["tipo"] == "Checklist":
        # se for uma atividade com checklist mostra o n° de itens concluídos
        total_itens = len(atividade["checklist"])
        itens_concluidos = sum(1 for item in atividade["checklist"] if item["concluido"])
        print(f"\nHistórico da atividade {atividade['nome']}:")
        print(f"Total de itens: {total_itens}")
        print(f"Itens concluídos: {itens_concluidos}")
        print(f"Itens pendentes: {total_itens - itens_concluidos}")
    else:
        # pra atividades sem checklist exibe o histórico de conclusão
        historico = atividade["historico"]
        if not historico:
            print("\nNenhum histórico para esta atividade.")
            return

        print(f"\nHistórico da atividade '{atividade['nome']}':")
        for data in historico:
            print(data)
        print(f"\nTotal: {len(historico)} vezes concluída.")

def menu():
    """Menu Principal"""
    usuario_atual = None
    while True:
        print(Fore.WHITE+Style.BRIGHT+"\n                 \U0001f570\n           ———— veZo ————")
        print("——————————————————————————————————————")
        print(Style.RESET_ALL+Fore.WHITE+"[1] Cadastro de Usuário")
        print("[2] Login")
        print("[3] Adicionar Atividade")
        print("[4] Mostrar Atividades")
        print("[5] Editar ou Excluir Atividades")
        print("[6] Marcar Atividade como Concluída")
        print("[7] Visualizar Histórico")
        print("[0] Sair")
        print("——————————————————————————————————————")
        
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            clear()
            cadastrar_usuario()
        elif opcao == "2":
            clear()
            usuario_atual = login()
        elif opcao == "3":
            clear()
            if usuario_atual:
                adicionar_atividade(usuario_atual)
            else:
                print("Faça login primeiro.") # caso o usuário tente usar alguma funcionalidade sem ter efetuado login
        elif opcao == "4":
            clear()
            if usuario_atual:
                mostrar_atividades(usuario_atual)
            else:
                print("Faça login primeiro.")
        elif opcao == "5":
            clear()
            if usuario_atual:
                edit_delete_atividade(usuario_atual)
            else:
                print("Faça login primeiro.")
        elif opcao == "6":
            clear()
            if usuario_atual:
                marcar_concluida(usuario_atual)
            else:
                print("Faça login primeiro.")
        elif opcao == "7":
            clear()
            if usuario_atual:
                historico(usuario_atual)
            else:
                print("Faça login primeiro.")
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            clear()
            print(" *Opção inválida. Tente novamente.")

menu()
