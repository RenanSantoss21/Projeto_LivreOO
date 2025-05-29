import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from package.alunos.aluno import Aluno, AlunoEspecial

DADOS_ALUNOS_PATH = "dados/alunos.json"
DADOS_DISCIPLINAS_PATH = "dados/disciplinas.json"

class AlunoGUI(tk.Frame):
    def __init__(self, master, ger_alunos, ger_disciplinas, show_main_menu_callback, salvar_dados_callback):
        super().__init__(master)
        self.master = master
        self.ger_alunos = ger_alunos
        self.ger_disciplinas = ger_disciplinas
        self.show_main_menu_callback = show_main_menu_callback
        self.salvar_dados_callback = salvar_dados_callback

        self.create_widgets()
        self.pack(fill="both", expand=True)

    def create_widgets(self):
        tk.Label(self, text="Modo Aluno", font=("Arial", 18)).pack(pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Cadastrar Aluno", command=self.cadastrar_aluno_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Listar Alunos", command=self.listar_alunos).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Remover Aluno", command=self.remover_aluno_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Matricular Aluno", command=self.matricular_aluno_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(button_frame, text="Trancar Matrícula", command=self.trancar_matricula_dialog).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(self, text="Voltar ao Menu Principal", command=self.go_back_to_main_menu).pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("Matrícula", "Nome", "Curso", "Tipo", "Disciplinas Ativas", "Histórico Aprovado"), show="headings")
        self.tree.heading("Matrícula", text="Matrícula")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Curso", text="Curso")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Disciplinas Ativas", text="Disciplinas Ativas")
        self.tree.heading("Histórico Aprovado", text="Histórico Aprovado")

        self.tree.column("Matrícula", width=80)
        self.tree.column("Nome", width=150)
        self.tree.column("Curso", width=120)
        self.tree.column("Tipo", width=60)
        self.tree.column("Disciplinas Ativas", width=150)
        self.tree.column("Histórico Aprovado", width=150)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.listar_alunos()

    def cadastrar_aluno_dialog(self):
        nome = simpledialog.askstring("Cadastrar Aluno", "Nome do Aluno:")
        if not nome: return

        matricula = simpledialog.askstring("Cadastrar Aluno", "Matrícula:")
        if not matricula: return

        curso = simpledialog.askstring("Cadastrar Aluno", "Curso:")
        if not curso: return

        tipo = simpledialog.askstring("Cadastrar Aluno", "Tipo (normal/especial):", initialvalue="normal")
        if not tipo: return

        if tipo.lower() == "especial":
            aluno = AlunoEspecial(nome, matricula, curso)
        else:
            aluno = Aluno(nome, matricula, curso)
        
        if self.ger_alunos.cadastrar(aluno):
            messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado!")
            self.salvar_dados_callback()
            self.listar_alunos()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar aluno. Matrícula duplicada?")

    def listar_alunos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        if not self.ger_alunos._alunos:
            self.tree.insert("", "end", values=("", "Nenhum aluno cadastrado.", "", "", "", ""))
            return

        for aluno in self.ger_alunos._alunos:
            disciplinas_str = ", ".join(aluno.disciplinas) if aluno.disciplinas else "Nenhuma"
            historico_str = ", ".join(aluno.historico) if aluno.historico else "Nenhum"
            aluno_tipo = "Especial" if isinstance(aluno, AlunoEspecial) else "Normal"
            self.tree.insert("", "end", values=(aluno.matricula, aluno.nome, aluno.curso, aluno_tipo, disciplinas_str, historico_str))

    def remover_aluno_dialog(self):
        matricula = simpledialog.askstring("Remover Aluno", "Digite a matrícula do aluno a ser removido:")
        if not matricula: return

        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover o aluno com matrícula {matricula}?"):
            if self.ger_alunos.remover(matricula):
                messagebox.showinfo("Sucesso", f"Aluno com matrícula {matricula} removido.")
                self.salvar_dados_callback()
                self.listar_alunos()
            else:
                messagebox.showerror("Erro", "Matrícula não encontrada.")

    def matricular_aluno_dialog(self):
        matricula = simpledialog.askstring("Matricular Aluno", "Digite a matrícula do aluno:")
        if not matricula: return
        
        aluno = self.ger_alunos.buscar_por_matricula(matricula)
        if not aluno:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            return

        codigo_disciplina = simpledialog.askstring("Matricular Aluno", "Digite o código da disciplina:")
        if not codigo_disciplina: return
        
        disciplina = self.ger_disciplinas.buscar_disciplina(codigo_disciplina)
        if not disciplina or not disciplina.turmas:
            messagebox.showerror("Erro", "Disciplina inválida ou sem turmas.")
            return
        
        turmas_str = "\n".join([f"{i+1}. Prof: {t.professor}, Sem: {t.semestre}, Horário: {t.horario}, Cap: {t.capacidade - len(t.alunos)}" for i, t in enumerate(disciplina.turmas)])
        turma_idx_str = simpledialog.askstring("Matricular Aluno", f"Turmas disponíveis para {disciplina.nome}:\n{turmas_str}\n\nDigite o número da turma:")
        
        if not turma_idx_str: return
        try:
            turma_idx = int(turma_idx_str) - 1
            turma = disciplina.turmas[turma_idx]
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Turma inválida.")
            return

        if self.ger_alunos.matricular(aluno, turma):
            messagebox.showinfo("Sucesso", f"Aluno {aluno.nome} matriculado na turma {disciplina.codigo}.")
            self.salvar_dados_callback()
            self.listar_alunos()
        else:
            messagebox.showerror("Erro", "Falha ao matricular aluno (verifique o console para mais detalhes sobre pré-requisitos/capacidade).")

    def trancar_matricula_dialog(self):
        matricula = simpledialog.askstring("Trancar Matrícula", "Digite a matrícula do aluno:")
        if not matricula: return

        aluno = self.ger_alunos.buscar_por_matricula(matricula)
        if not aluno:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            return

        codigo_disciplina = simpledialog.askstring("Trancar Matrícula", "Digite o código da disciplina da turma a ser trancada:")
        if not codigo_disciplina: return
        
        disciplina = self.ger_disciplinas.buscar_disciplina(codigo_disciplina)
        if not disciplina or not disciplina.turmas:
            messagebox.showerror("Erro", "Disciplina inválida ou sem turmas.")
            return
        
        turma_encontrada = None
        for turma_obj in disciplina.turmas:
            if aluno.matricula in turma_obj.alunos:
                turma_encontrada = turma_obj
                break
        
        if turma_encontrada:
            if messagebox.askyesno("Confirmar Trancamento", f"Confirmar trancamento de matrícula de {aluno.nome} na turma {turma_encontrada.codigo_disciplina}?"):
                if self.ger_alunos.trancar_matricula(aluno, turma_encontrada):
                    messagebox.showinfo("Sucesso", f"Matrícula de {aluno.nome} na turma {turma_encontrada.codigo_disciplina} trancada.")
                    self.salvar_dados_callback()
                    self.listar_alunos()
                else:
                    messagebox.showerror("Erro", "Falha ao trancar matrícula (verifique o console).")
            else:
                messagebox.showinfo("Cancelado", "Trancamento cancelado.")
        else:
            messagebox.showerror("Erro", f"Aluno {aluno.nome} não está matriculado em nenhuma turma da disciplina {codigo_disciplina}.")

    def go_back_to_main_menu(self):
        self.pack_forget()
        self.salvar_dados_callback()
        self.show_main_menu_callback()