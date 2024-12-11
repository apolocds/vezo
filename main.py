# Dicionário que serve como banco de dados
usuarios = {}

# Função para validar a quantidade de caracteres da senha
def validar_senha(senha):
    return len(senha) >= 8

# Cadastro de usuário
def cadastrar_usuario():
    print("\n--- Cadastro de Usuário ---")
    nome = None  # Inicializa o nome como None

    while True:
        # Solicita o nome de usuário apenas se ainda não for válido
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
        
        # Solicita a senha
        senha = input("Digite uma senha (mínimo 8 caracteres): ").strip()
        if not validar_senha(senha):
            print("Senha inválida. Deve ter pelo menos 8 caracteres.")
            continue
        
        # Confirmação da senha
        senha_confirmada = input("Confirme a senha: ").strip()
        if senha != senha_confirmada:
            print("As senhas não coincidem. Tente novamente.")
            continue

        # Caso final: entrada válida
        usuarios[nome] = {"senha": senha}
        print(f"Usuário '{nome}' cadastrado com sucesso!")
        break

def login():
    print("\n--- Login ---")
    nome = input("Nome de usuário: ").strip()
    senha = input("Senha: ").strip()
    
    if nome in usuarios and usuarios[nome]["senha"] == senha:
        print(f"Bem-vindo, {nome}!")
        return nome
    print("Credenciais inválidas. Tente novamente.")
    return None

# Menu principal
def menu():
    while True:
        print("\n--- Menu ---")
        print("[1] Cadastro de Usuário")
        print("[2] Login")
        print("[0] Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            usuario_atual = login()
            if usuario_atual:
                print(f"Você está logado como {usuario_atual}.")
        elif opcao == "0":
            print("Encerrando o programa. Até mais!")
            break
        else:
            print("Opção inválida.")

menu()
