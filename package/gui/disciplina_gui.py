import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from package.disciplinas.disciplina import Disciplina
from package.disciplinas.turma import Turma

DADOS_DISCIPLINAS_PATH = "dados/disciplinas.json"

class DisciplinaGUI(tk.Frame):
    def __init__(self, master, ger_disciplinas, show_main_menu_callback, salvar_dados_callback):
        super().__init__(master)
        self.master = master
        self.ger_disciplinas = ger_disciplinas
        self.show_main_menu_callback = show_main_menu_callback
        self.salvar_dados_callback = salvar_dados_callback

        self.create_widgets()
        self.pack(fill="both", expand=True)

    def create_widgets(self):

        tk.Label(self, text="Modo Disciplina/Turma", font=("Arial", 18)).pack(pady=10)

        discipline_button_frame = tk.LabelFrame(self, text="Ações de Disciplina", padx=10, pady=10)
        discipline_button_frame.pack(pady=5)

        tk.Button(discipline_button_frame, text="Cadastrar Disciplina", command=self.cadastrar_disciplina_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(discipline_button_frame, text="Editar Disciplina", command=self.editar_disciplina_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(discipline_button_frame, text="Remover Disciplina", command=self.remover_disciplina_dialog).pack(side=tk.LEFT, padx=5, pady=5)


        turma_button_frame = tk.LabelFrame(self, text="Ações de Turma", padx=10, pady=10)
        turma_button_frame.pack(pady=5)

        tk.Button(turma_button_frame, text="Criar Turma", command=self.criar_turma_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(turma_button_frame, text="Editar Turma", command=self.editar_turma_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(turma_button_frame, text="Remover Turma", command=self.remover_turma_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        

        tk.Button(self, text="Voltar ao Menu Principal", command=self.go_back_to_main_menu).pack(pady=20)


        self.tree = ttk.Treeview(self, columns=("Código", "Nome", "Carga Horária", "Pré-requisitos", "Turmas"), show="headings")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Carga Horária", text="Carga Horária")
        self.tree.heading("Pré-requisitos", text="Pré-requisitos")
        self.tree.heading("Turmas", text="Turmas")

        self.tree.column("Código", width=80)
        self.tree.column("Nome", width=180)
        self.tree.column("Carga Horária", width=100)
        self.tree.column("Pré-requisitos", width=150)
        self.tree.column("Turmas", width=250)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.listar_disciplinas_e_turmas()

    def listar_disciplinas_e_turmas(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        if not self.ger_disciplinas._disciplinas:
            self.tree.insert("", "end", values=("", "Nenhuma disciplina cadastrada.", "", "", ""))
            return

        for disciplina in self.ger_disciplinas._disciplinas:
            pre_req_str = ", ".join(disciplina.pre_requisitos) if disciplina.pre_requisitos else "Nenhum"
            turmas_info = []
            for i, t in enumerate(disciplina.turmas):
                turmas_info.append(f"T{i+1}: {t.professor} ({t.semestre}) - {t.capacidade} Vagas disponíveis")
            turmas_str = "\n".join(turmas_info) if turmas_info else "Nenhuma"
            
            self.tree.insert("", "end", values=(disciplina.codigo, disciplina.nome, disciplina.carga_horaria, pre_req_str, turmas_str))

    def cadastrar_disciplina_dialog(self):
        nome = simpledialog.askstring("Cadastrar Disciplina", "Nome da Disciplina:")
        if not nome: return

        codigo = simpledialog.askstring("Cadastrar Disciplina", "Código:")
        if not codigo: return

        try:
            carga_horaria = simpledialog.askinteger("Cadastrar Disciplina", "Carga horária:")
            if carga_horaria is None: return
            if carga_horaria <= 0:
                messagebox.showerror("Erro", "Carga horária deve ser um número positivo.")
                return
        except Exception:
            messagebox.showerror("Erro", "Carga horária inválida.")
            return

        pre_requisitos_str = simpledialog.askstring("Cadastrar Disciplina", "Pré-requisitos (códigos separados por vírgula):", initialvalue="")
        pre_requisitos = [p.strip() for p in pre_requisitos_str.split(',') if p.strip()] if pre_requisitos_str else []

        disciplina = Disciplina(nome, codigo, carga_horaria, pre_requisitos)
        
        if self.ger_disciplinas.adicionar_disciplina(disciplina):
            messagebox.showinfo("Sucesso", f"Disciplina '{nome}' cadastrada!")
            self.salvar_dados_callback()
            self.listar_disciplinas_e_turmas()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar disciplina (código já existe?).")

    def editar_disciplina_dialog(self):
        selected_item = self.tree.focus() # Obtém o ID do item selecionado
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma disciplina na lista para editar.")
            return
        
        codigo_disciplina_selecionada = self.tree.item(selected_item, 'values')[0] # Obtém o código da disciplina

        disciplina_obj = self.ger_disciplinas.buscar_disciplina(codigo_disciplina_selecionada)
        if not disciplina_obj:
            messagebox.showerror("Erro", "Disciplina não encontrada (erro interno).")
            return

        # Popula os campos com os dados atuais
        novo_nome = simpledialog.askstring("Editar Disciplina", "Novo Nome:", initialvalue=disciplina_obj.nome)
        if novo_nome is None: return

        nova_carga_horaria_str = simpledialog.askstring("Editar Disciplina", "Nova Carga Horária:", initialvalue=str(disciplina_obj.carga_horaria))
        if nova_carga_horaria_str is None: return
        try:
            nova_carga_horaria = int(nova_carga_horaria_str)
            if nova_carga_horaria <= 0:
                messagebox.showerror("Erro", "Carga horária deve ser um número positivo.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Carga horária inválida.")
            return

        novos_pre_requisitos_str = simpledialog.askstring("Editar Disciplina", "Novos Pré-requisitos (códigos separados por vírgula):", initialvalue=", ".join(disciplina_obj.pre_requisitos))
        novos_pre_requisitos = [p.strip() for p in novos_pre_requisitos_str.split(',') if p.strip()] if novos_pre_requisitos_str else []

        novos_dados = {
            "nome": novo_nome,
            "carga_horaria": nova_carga_horaria,
            "pre_requisitos": novos_pre_requisitos
        }

        if self.ger_disciplinas.editar_disciplina(codigo_disciplina_selecionada, novos_dados):
            messagebox.showinfo("Sucesso", f"Disciplina '{codigo_disciplina_selecionada}' atualizada!")
            self.salvar_dados_callback()
            self.listar_disciplinas_e_turmas()
        else:
            messagebox.showerror("Erro", "Falha ao editar disciplina (verifique console para detalhes).")

    def remover_disciplina_dialog(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma disciplina na lista para remover.")
            return

        codigo_disciplina = self.tree.item(selected_item, 'values')[0]
        disciplina_obj = self.ger_disciplinas.buscar_disciplina(codigo_disciplina)

        if disciplina_obj and disciplina_obj.turmas:
            messagebox.showerror("Erro", f"Não é possível remover a disciplina '{disciplina_obj.nome}' pois ela possui turmas ativas. Remova as turmas primeiro.")
            return

        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover a disciplina '{codigo_disciplina}'?"):
            if self.ger_disciplinas.remover_disciplina(codigo_disciplina):
                messagebox.showinfo("Sucesso", f"Disciplina '{codigo_disciplina}' removida.")
                self.salvar_dados_callback()
                self.listar_disciplinas_e_turmas()
            else:
                messagebox.showerror("Erro", "Falha ao remover disciplina (não encontrada?).")
    
    def criar_turma_dialog(self):
        codigo_disciplina = simpledialog.askstring("Criar Turma", "Código da Disciplina para a Turma:")
        if not codigo_disciplina: return

        disciplina = self.ger_disciplinas.buscar_disciplina(codigo_disciplina)
        if not disciplina:
            messagebox.showerror("Erro", "Disciplina não encontrada.")
            return
        
        professor = simpledialog.askstring("Criar Turma", "Professor Responsável:")
        if not professor: return

        semestre = simpledialog.askstring("Criar Turma", "Semestre (ex: 2025.1):")
        if not semestre: return

        avaliacao = simpledialog.askstring("Criar Turma", "Forma de avaliação (simples/ponderada):", initialvalue="simples")
        if not avaliacao or avaliacao.lower() not in ["simples", "ponderada"]:
            messagebox.showerror("Erro", "Forma de avaliação inválida. Use 'simples' ou 'ponderada'.")
            return

        presencial_str = simpledialog.askstring("Criar Turma", "Presencial? (s/n):", initialvalue="s").lower()
        presencial = (presencial_str == 's')

        sala = ""
        if presencial:
            sala = simpledialog.askstring("Criar Turma", "Sala:")
            if not sala: return

        horario = simpledialog.askstring("Criar Turma", "Horário:")
        if not horario: return

        try:
            capacidade = simpledialog.askinteger("Criar Turma", "Capacidade máxima:")
            if capacidade is None: return
            if capacidade <= 0:
                messagebox.showerror("Erro", "Capacidade deve ser um número positivo.")
                return
        except Exception:
            messagebox.showerror("Erro", "Capacidade inválida.")
            return

        turma = Turma(professor, semestre, avaliacao, presencial, horario, sala, capacidade, codigo_disciplina)
        
        disciplina.turmas.append(turma)
        messagebox.showinfo("Sucesso", f"Turma criada para a disciplina '{disciplina.nome}'.")
        self.salvar_dados_callback()
        self.listar_disciplinas_e_turmas()

    def editar_turma_dialog(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione a disciplina da turma na lista para editar a turma.")
            return
        
        codigo_disciplina = self.tree.item(selected_item, 'values')[0]
        disciplina_obj = self.ger_disciplinas.buscar_disciplina(codigo_disciplina)
        if not disciplina_obj:
            messagebox.showerror("Erro", "Disciplina não encontrada (erro interno).")
            return
        
        if not disciplina_obj.turmas:
            messagebox.showinfo("Info", "Esta disciplina não possui turmas para editar.")
            return

        # Exibir turmas disponíveis e permitir seleção da turma
        turmas_display = [f"{i+1}. Prof: {t.professor} ({t.semestre}) - {t.horario}" for i, t in enumerate(disciplina_obj.turmas)]
        turma_idx_str = simpledialog.askstring("Editar Turma", f"Turmas da disciplina '{disciplina_obj.nome}':\n" + "\n".join(turmas_display) + "\n\nDigite o número da turma para editar:")
        
        if not turma_idx_str: return
        try:
            indice_turma = int(turma_idx_str) - 1
            if not (0 <= indice_turma < len(disciplina_obj.turmas)):
                raise IndexError
            turma_original = disciplina_obj.turmas[indice_turma]
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Número de turma inválido.")
            return
        
        # Coletar novos dados da turma
        novo_professor = simpledialog.askstring("Editar Turma", "Novo Professor:", initialvalue=turma_original.professor)
        if novo_professor is None: return

        novo_semestre = simpledialog.askstring("Editar Turma", "Novo Semestre:", initialvalue=turma_original.semestre)
        if novo_semestre is None: return

        nova_avaliacao = simpledialog.askstring("Editar Turma", "Nova Forma de Avaliação (simples/ponderada):", initialvalue=turma_original.avaliacao)
        if nova_avaliacao is None or nova_avaliacao.lower() not in ["simples", "ponderada"]:
            messagebox.showerror("Erro", "Forma de avaliação inválida. Use 'simples' ou 'ponderada'.")
            return

        novo_presencial_str = simpledialog.askstring("Editar Turma", "Presencial? (s/n):", initialvalue='s' if turma_original.presencial else 'n').lower()
        novo_presencial = (novo_presencial_str == 's')

        nova_sala = ""
        if novo_presencial:
            nova_sala = simpledialog.askstring("Editar Turma", "Nova Sala:", initialvalue=turma_original.sala)
            if nova_sala is None: return

        novo_horario = simpledialog.askstring("Editar Turma", "Novo Horário:", initialvalue=turma_original.horario)
        if novo_horario is None: return

        nova_capacidade_str = simpledialog.askstring("Editar Turma", "Nova Capacidade Máxima:", initialvalue=str(turma_original.capacidade))
        if nova_capacidade_str is None: return
        try:
            nova_capacidade = int(nova_capacidade_str)
            if nova_capacidade <= 0:
                messagebox.showerror("Erro", "Capacidade deve ser um número positivo.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Capacidade inválida.")
            return

        novos_dados_turma = {
            "professor": novo_professor,
            "semestre": novo_semestre,
            "avaliacao": nova_avaliacao,
            "presencial": novo_presencial,
            "horario": novo_horario,
            "sala": nova_sala,
            "capacidade": nova_capacidade
        }
        
        if self.ger_disciplinas.editar_turma(codigo_disciplina, indice_turma, novos_dados_turma):
            messagebox.showinfo("Sucesso", f"Turma {indice_turma+1} da disciplina '{codigo_disciplina}' atualizada!")
            self.salvar_dados_callback()
            self.listar_disciplinas_e_turmas()
        else:
            messagebox.showerror("Erro", "Falha ao editar turma (verifique console).")

    def remover_turma_dialog(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione a disciplina da turma na lista para remover a turma.")
            return
        
        codigo_disciplina = self.tree.item(selected_item, 'values')[0]
        disciplina_obj = self.ger_disciplinas.buscar_disciplina(codigo_disciplina)
        if not disciplina_obj:
            messagebox.showerror("Erro", "Disciplina não encontrada (erro interno).")
            return
        
        if not disciplina_obj.turmas:
            messagebox.showinfo("Info", "Esta disciplina não possui turmas para remover.")
            return

        turmas_display = [f"{i+1}. Prof: {t.professor} ({t.semestre}) - {t.horario}" for i, t in enumerate(disciplina_obj.turmas)]
        turma_idx_str = simpledialog.askstring("Remover Turma", f"Turmas da disciplina '{disciplina_obj.nome}':\n" + "\n".join(turmas_display) + "\n\nDigite o número da turma para remover:")
        
        if not turma_idx_str: return
        try:
            indice_turma = int(turma_idx_str) - 1
            if not (0 <= indice_turma < len(disciplina_obj.turmas)):
                raise IndexError
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Número de turma inválido.")
            return
        
        turma_a_remover = disciplina_obj.turmas[indice_turma]
        if turma_a_remover.alunos:
            messagebox.showerror("Erro", f"Não é possível remover a turma do professor {turma_a_remover.professor} (semestre {turma_a_remover.semestre}) pois ela possui alunos matriculados. Desmatricule os alunos primeiro.")
            return

        if messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover a turma {indice_turma+1} da disciplina '{codigo_disciplina}'?"):
            if self.ger_disciplinas.remover_turma(codigo_disciplina, indice_turma):
                messagebox.showinfo("Sucesso", f"Turma removida da disciplina '{codigo_disciplina}'.")
                self.salvar_dados_callback()
                self.listar_disciplinas_e_turmas()
            else:
                messagebox.showerror("Erro", "Falha ao remover turma (verifique console).")



    def go_back_to_main_menu(self):
        self.pack_forget()
        self.salvar_dados_callback()
        self.show_main_menu_callback()