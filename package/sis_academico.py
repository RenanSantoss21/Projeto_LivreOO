from package.alunos.cadastro import GerenciadorAlunos
from package.disciplinas.cadastro import GerenciadorDisciplinas
from package.alunos.menu_aluno import Menu_aluno
from package.avaliacao.menu_av import GerenciadorAvaliacao
from package.disciplinas.menu_disc import Menu_disciplina
from package.usuarios.cadastro_usuario import GerenciadorUsuarios
import os

DADOS_ALUNOS_PATH = "dados/alunos.json"
DADOS_DISCIPLINAS_PATH = "dados/disciplinas.json"
DADOS_USUARIOS_PATH = "dados/usuarios.json"


class SistemaAcademico:
    def __init__(self):
        os.makedirs("dados", exist_ok=True)

        self._ger_usuarios = GerenciadorUsuarios(DADOS_USUARIOS_PATH)
        self._ger_disciplinas = GerenciadorDisciplinas()
        self._ger_alunos = GerenciadorAlunos(ger_disciplinas=self._ger_disciplinas)

        self._ger_alunos.carregar(DADOS_ALUNOS_PATH)
        self._ger_disciplinas.carregar(DADOS_DISCIPLINAS_PATH)

        self._menu_avaliacao = GerenciadorAvaliacao(
            ger_alunos=self._ger_alunos,
            ger_disciplinas=self._ger_disciplinas
        )
        self._menu_aluno = Menu_aluno(
            ger_alunos=self._ger_alunos,
            ger_disciplinas=self._ger_disciplinas
        )
        self._menu_disciplina = Menu_disciplina(
            ger_disciplinas=self._ger_disciplinas
        )
        self._usuario_aut = None

    def _exibir_menu(self):
        print("\n=== Sistema Acadêmico - FCTE ===")
        print("1. Modo Aluno")
        print("2. Modo Disciplina/Turma")
        print("3. Modo Avaliação/Frequência")
        print("4. Sair")
        return input("Escolha: ")
    
    def _iniciar_menus(self, escolha):
        if escolha == "1":
            self._menu_aluno.menu()
        elif escolha == "2":
            self._menu_disciplina.menu()
        elif escolha == "3":
            self._menu_avaliacao.menu()

        elif escolha == "4":
            print("Encerrando. Dados salvos!")
            self._salvar_dados()
            return True
        else:
            print("Opção inválida.")
        return False
    
    def _salvar_dados(self):
        self._ger_alunos.salvar(DADOS_ALUNOS_PATH)
        self._ger_disciplinas.salvar(DADOS_DISCIPLINAS_PATH)
        self._ger_usuarios.salvar_usuarios()

    def _autenticar_usuario(self):
        if not self._ger_usuarios._usuarios:
            print("\nNenhum usuário encontrado. Cadastrando usuário administrador padrão.")
            self._ger_usuarios.cadastrar_usuario("admin", "admin123", "admin")

        tentativas = 0
        max_tentativas = 3

        while self._usuario_aut is None and tentativas < max_tentativas:
            print("\n--- Tela de Login ---")
            username = input("Usuário: ")
            password = input("Senha: ")

            self._usuario_aut = self._ger_usuarios.autenticar_usuario(username, password)
            if self._usuario_aut:
                print(f"Bem-vindo(a), {self._usuario_aut.username}!")
                return True
            else:
                tentativas += 1
                print(f"Tentativas restantes: {max_tentativas - tentativas}")
                if tentativas == max_tentativas:
                    print("Número máximo de tentativas excedido. Encerrando o sistema.")
                    return False
        return False
    
    def loop(self):
        if not self._autenticar_usuario():
            return 

        sair_do_programa = False
        while not sair_do_programa:
            escolha = self._exibir_menu()
            sair_do_programa = self._iniciar_menus(escolha)
