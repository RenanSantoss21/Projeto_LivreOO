import tkinter as tk
from tkinter import messagebox, simpledialog

from package.alunos.cadastro import GerenciadorAlunos
from package.disciplinas.cadastro import GerenciadorDisciplinas
from package.usuarios.cadastro_usuario import GerenciadorUsuarios

from package.gui.aluno_gui import AlunoGUI
from package.gui.disciplina_gui import DisciplinaGUI
from package.gui.avaliacao_gui import AvaliacaoGUI

DADOS_ALUNOS_PATH = "dados/alunos.json"
DADOS_DISCIPLINAS_PATH = "dados/disciplinas.json"
DADOS_USUARIOS_PATH = "dados/usuarios.json"


class SistemaAcademicoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sistema Acadêmico FCTE")
        master.geometry("800x600")

        import os
        os.makedirs("dados", exist_ok=True)

        self._ger_usuarios = GerenciadorUsuarios(DADOS_USUARIOS_PATH)
        self._ger_disciplinas = GerenciadorDisciplinas()
        self._ger_alunos = GerenciadorAlunos(ger_disciplinas=self._ger_disciplinas)

        self._ger_alunos.carregar(DADOS_ALUNOS_PATH)
        self._ger_disciplinas.carregar(DADOS_DISCIPLINAS_PATH)

        self._usuario_autenticado = None

        self.current_frame = None

        if not self._ger_usuarios._usuarios:
            messagebox.showinfo("Primeiro Acesso", "Nenhum usuário encontrado. Cadastre um usuário administrador padrão.")
            username = simpledialog.askstring("Cadastro Admin", "Novo Usuário Admin:", parent=master)
            password = simpledialog.askstring("Cadastro Admin", "Senha Admin:", show='*', parent=master)
            if username and password:
                self._ger_usuarios.cadastrar_usuario(username, password, "admin")
            else:
                messagebox.showerror("Erro", "Nome de usuário ou senha vazios. O sistema não pode ser iniciado.")
                master.destroy()
                return
        
        self.show_login_frame()

    def show_frame(self, frame_class, *args, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self.master, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def show_login_frame(self):
        self.show_frame(LoginFrame, self.attempt_login)

    def attempt_login(self, username, password):
        self._usuario_autenticado = self._ger_usuarios.autenticar_usuario(username, password)
        if self._usuario_autenticado:
            messagebox.showinfo("Login", f"Bem-vindo(a), {self._usuario_autenticado.username}!")
            self.show_main_menu_frame()
            return True
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
            return False

    def show_main_menu_frame(self):
        self.show_frame(MainMenuFrame, self.show_aluno_mode, self.show_disciplina_mode, self.show_avaliacao_mode, self.on_closing)

    def show_aluno_mode(self):
        self.show_frame(AlunoGUI, self._ger_alunos, self._ger_disciplinas, self.show_main_menu_frame, self._salvar_dados_e_notificar)

    def show_disciplina_mode(self):
        self.show_frame(DisciplinaGUI, self._ger_disciplinas, self.show_main_menu_frame, self._salvar_dados_e_notificar)

    def show_avaliacao_mode(self):
        self.show_frame(AvaliacaoGUI, self._ger_alunos, self._ger_disciplinas, self.show_main_menu_frame, self._salvar_dados_e_notificar) # Futuramente

    def on_closing(self):
        if messagebox.askyesno("Sair", "Deseja salvar os dados e sair do sistema?"):
            self._salvar_dados_e_notificar(show_success=True)
            self.master.destroy()
        else:
            self.master.destroy()

    def _salvar_dados(self):
        self._ger_alunos.salvar(DADOS_ALUNOS_PATH)
        self._ger_disciplinas.salvar(DADOS_DISCIPLINAS_PATH)
        self._ger_usuarios.salvar_usuarios()

    def _salvar_dados_e_notificar(self, show_success=False):
        try:
            self._salvar_dados()
            if show_success:
                messagebox.showinfo("Salvando", "Dados salvos com sucesso!")
            return True
        except Exception as e:
            messagebox.showerror("Erro de Salvamento", f"Ocorreu um erro ao salvar os dados: {e}")
            return False

# --- Classes de Frames Separados ---

class LoginFrame(tk.Frame):
    def __init__(self, master, attempt_login_callback):
        super().__init__(master)
        self.attempt_login_callback = attempt_login_callback
        self.create_widgets()

    def create_widgets(self):
        self.pack(expand=True)
        tk.Label(self, text="Sistema Acadêmico - Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Usuário:").pack(anchor="w")
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Senha:").pack(anchor="w")
        self.password_entry = tk.Entry(self, width=30, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self, text="Entrar", command=self._on_login_button_click)
        self.login_button.pack(pady=10)

    def _on_login_button_click(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.attempt_login_callback(username, password)

class MainMenuFrame(tk.Frame):
    def __init__(self, master, show_aluno_mode_callback, show_disciplina_mode_callback, show_avaliacao_mode_callback, on_closing_callback):
        super().__init__(master)
        self.show_aluno_mode_callback = show_aluno_mode_callback
        self.show_disciplina_mode_callback = show_disciplina_mode_callback
        self.show_avaliacao_mode_callback = show_avaliacao_mode_callback
        self.on_closing_callback = on_closing_callback
        self.create_widgets()

    def create_widgets(self):
        self.pack(expand=True)
        tk.Label(self, text="Menu Principal", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Modo Aluno", command=self.show_aluno_mode_callback).pack(pady=5)
        tk.Button(self, text="Modo Disciplina/Turma", command=self.show_disciplina_mode_callback).pack(pady=5) # Habilitado
        tk.Button(self, text="Modo Avaliação/Frequência", command=self.show_avaliacao_mode_callback).pack(pady=5) # Habilitado com mensagem
        
        tk.Button(self, text="Sair", command=self.on_closing_callback).pack(pady=20)