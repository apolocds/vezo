veZo - Organizador de Hábitos e Tarefas

Descrição

O veZo é um organizador de hábitos e tarefas pessoais desenvolvido em Python, focado na gestão de atividades diárias com um sistema de autenticação seguro. O projeto é executado via terminal e permite o cadastro de usuários, inclusão de atividades e rastreamento de progresso de maneira simples e eficiente.

-----------------------------------------------------------------------------------------------

Funcionalidades

- Cadastro de usuário: Nome de usuário, senha segura e e-mail para autenticação.

- Login seguro: Validação por senha e autenticação de dois fatores (2FA) via e-mail.

- Gestão de atividades:
  - Adicionar tarefas e hábitos.
  - Criar checklists interativos.
  - Editar e excluir atividades.
  - Marcar atividades como concluídas.
  - Visualizar histórico de atividades.

- Notificações: Alertas no sistema para lembrar o usuário de suas tarefas.

-----------------------------------------------------------------------------------------------

 Instalação e Execução

Dependências

	Certifique-se de ter o Python instalado (versão 3.6+). Instale as dependências necessárias: pip install plyer colorama

Como Rodar

Execute o seguinte comando no terminal:

python vezo.py

-----------------------------------------------------------------------------------------------

Uso

Ao iniciar o programa, você verá o menu principal, onde pode:

1. Criar um usuário.
2. Fazer login.
3. Adicionar, editar ou excluir atividades.
4. Marcar atividades como concluídas.
5. Visualizar histórico.
6. Sair do programa.

-----------------------------------------------------------------------------------------------

Segurança

- A senha deve conter no mínimo 8 caracteres.
- O sistema usa **Autenticação de Dois Fatores (2FA)** via e-mail para maior segurança.
- O código de verificação é enviado para o e-mail cadastrado e deve ser digitado corretamente.

-----------------------------------------------------------------------------------------------

Desenvolvido por Apolo César.

