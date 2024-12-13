# dicionário que serve como banco de dados
usuarios = {}

def validar_senha(senha):
    """Função para validar a quantidade de caracteres inseridos pelo usuário"""
    return len(senha) >= 8

def cadastrar_usuario():
    """Função que insere os dados cadastrados pelo usuário no dicionário"""
    print("\n--- Cadastro de Usuário ---")
    nome = None  # inicializa o nome como None fora do loop para o código saber se o nome já foi validado ou precisa ser solicitado novamente, pra evitar repetições desnecessárias

    while True:
        if not nome:
            nome = input("Digite um nome de usuário: ").strip()
            if not nome:
                print("Nome de usuário não pode estar vazio. Insira um nome válido.")
                nome = None
                continue 
            if nome in usuarios:
                print("Nome de usuário já existe. Escolha outro.")
                nome = None
                continue
        
        senha = input("Digite uma senha (mínimo 8 caracteres): ").strip()
        if not validar_senha(senha):
            print("Senha inválida. Deve ter pelo menos 8 caracteres.")
            continue
        
        senha_confirmada = input("Confirme a senha: ").strip()
        if senha != senha_confirmada:
            print("As senhas não coincidem. Tente novamente.")
            continue

        usuarios[nome] = {"senha": senha, "atividades": []} # create
        print(f"Usuário '{nome}' cadastrado com sucesso!") # read
        break


def login():
    """Função que define o usuário atual a partir da validação dos dados inseridos com os dados cadastrados"""
    print("\n--- Login ---")
    nome = input("Nome de usuário: ").strip()
    senha = input("Senha: ").strip()
    
    if nome in usuarios and usuarios[nome]["senha"] == senha:
        print(f"Bem-vindo, {nome}!")
        return nome
    print("Credenciais inválidas. Tente novamente.")
    return None

def adicionar_atividade(usuario): # create
    """Função que adiciona uma atividade ao dicionário do usuário logado"""
    print("\n--- Adicionar Atividade ---")
    nome_atividade = input("Nome da Atividade: ").strip()
    if not nome_atividade:
        print("Nome da atividade não pode estar vazio.")
        return

    tipo = input("Frequência:\n[1] Hábito (atividade que se repete)\n[2] Tarefa (atividade única): ").strip()
    if tipo not in ("1", "2"):
        print("Opção inválida.")
        return

    frequencia = None
    dias_especificos = None
    if tipo == "1":
        frequencia = input("\nCom que frequência você deseja realizar esse hábito:\n[1] Todos os dias\n[2] Dias específicos: ").strip()
        if frequencia == "2":
            print("\nEscolha os dias da semana (exemplo: 2,4,6 para segunda, quarta e sexta):")
            dias_opcoes = ["[1] Domingo", "[2] Segunda", "[3] Terça", "[4] Quarta", 
                           "[5] Quinta", "[6] Sexta", "[7] Sábado"]
            print("\n".join(dias_opcoes))
            dias_especificos = input("Dias: ").strip().split(',')
            dias_especificos = [int(dia) for dia in dias_especificos if dia.isdigit() and 1 <= int(dia) <= 7]
            # ↑ valida a entrada do usuário garantindo que o valor recebido seja um  valor numérico, converte o valor de str para int e garante que esteja entre 1 e 7, se a entrada não for convertida a comparação não pode ser feita 

            if not dias_especificos:
                print("Opção inválida. Frequência definida como 'Todos os dias'.")
                frequencia = "1"

    usuarios[usuario]["atividades"].append({
        "nome": nome_atividade,
        "tipo": "Hábito" if tipo == "1" else "Tarefa",
        "frequencia": "Todos os dias" if frequencia == "1" else "Dias específicos" if frequencia == "2" else None,
        "dias_especificos": dias_especificos if frequencia == "2" else None,
        "historico": []
    })
    print(f"Atividade '{nome_atividade}' adicionada com sucesso!")

def listar_atividades(usuario): # read
    """Função que exibe as atividades do usuário"""
    print("\n--- Atividades Cadastradas ---")
    atividades = usuarios[usuario]["atividades"]
    if not atividades:
        print("Nenhuma atividade cadastrada.")
        return

    for i, atividade in enumerate(atividades, 1):
        print(f"[{i}] {atividade['nome']} ({atividade['tipo']})")
    # linha para printar as atividades numeradas

def edit_delete_atividade(usuario): # update e delete

    # o edit está sem a opção de trocar uma tarefa única para um hábito e trocar os dias específicos de um hábito 

    """Função que permite o usuário editar ou excluir atividades do dicionário"""
    listar_atividades(usuario)
    atividades = usuarios[usuario]["atividades"]
    if not atividades:
        return

    escolha = input("Escolha o número da atividade que deseja atualizar ou excluir: ").strip()
    if not escolha.isdigit() or int(escolha) not in range(1, len(atividades) + 1):
        print("Opção inválida.")
        return

    escolha = int(escolha) - 1
    print("\n[1] Editar\n[2] Excluir")
    acao = input("Escolha uma ação: ").strip()

# *as escolhas tem +1 e -1 porque pro usuário a contagem é iniciada do número 1 mas no índice de listagem por padrão a contagem começa pelo 0

    if acao == "1":
        novo_nome = input("Novo nome para a atividade: ").strip()
        if novo_nome:
            atividades[escolha]["nome"] = novo_nome
            print("Atividade atualizada com sucesso!")
        else:
            print("O nome não pode ser vazio.")
    elif acao == "2":
        atividades.pop(escolha)
        print("Atividade excluída com sucesso!")
    else:
        print("Ação inválida.")


def marcar_concluida(usuario):
    """Função que permite ao usuário marcar as atividades como concluídas"""
    listar_atividades(usuario)
    atividades = usuarios[usuario]["atividades"]
    if not atividades:
        return

    escolha = input("Escolha o número da atividade que deseja marcar como concluída: ").strip()
    if not escolha.isdigit() or int(escolha) not in range(1, len(atividades) + 1):
        print("Opção inválida.")
        return

    escolha = int(escolha) - 1
    atividade = atividades[escolha]
    data = input("Informe a data da conclusão: ").strip()
    atividade["historico"].append(data)
    print(f"Atividade '{atividade['nome']}' marcada como concluída em {data}!")

    if atividade["tipo"] == "Tarefa":
        atividades.pop(escolha)
    # ↑ linha para atividades que o usuário cadastra como únicas, depois de concluídas são apagadas do bd

def historico(usuario):
    """Função que permite o usuário visualizar quantas vezes uma atividade foi concluída"""
    listar_atividades(usuario)
    atividades = usuarios[usuario]["atividades"]
    if not atividades:
        return

    escolha = input("Escolha o número da atividade para visualizar o histórico: ").strip()
    if not escolha.isdigit() or int(escolha) not in range(1, len(atividades) + 1):
        print("Opção inválida.")
        return

    escolha = int(escolha) - 1
    historico = atividades[escolha]["historico"]
    if not historico:
        print("Nenhum histórico para esta atividade.")
        return

    print(f"\nHistórico da atividade '{atividades[escolha]['nome']}':")
    for data in historico:
        print(data)
    print(f"Total: {len(historico)} vezes concluída.")

def menu():
    """Menu Principal"""
    usuario_atual = None
    while True:
        print("\n--- Menu ---")
        print("[1] Cadastro de Usuário")
        print("[2] Login")
        print("[3] Adicionar Atividade")
        print("[4] Listar Atividades")
        print("[5] Editar ou Excluir Atividades")
        print("[6] Marcar Atividade como Concluída")
        print("[7] Visualizar Histórico")
        print("[0] Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            usuario_atual = login()
        elif opcao == "3":
            if usuario_atual:
                adicionar_atividade(usuario_atual)
            else:
                print("Faça login primeiro.") # caso o usuário tente usar alguma funcionalidade sem ter efetuado login
        elif opcao == "4":
            if usuario_atual:
                listar_atividades(usuario_atual)
            else:
                print("Faça login primeiro.")
        elif opcao == "5":
            if usuario_atual:
                edit_delete_atividade(usuario_atual)
            else:
                print("Faça login primeiro.")
        elif opcao == "6":
            if usuario_atual:
                marcar_concluida(usuario_atual)
            else:
                print("Faça login primeiro.")
        elif opcao == "7":
            if usuario_atual:
                historico(usuario_atual)
            else:
                print("Faça login primeiro.")
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()
