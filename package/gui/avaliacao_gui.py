import tkinter as tk
from tkinter import messagebox, simpledialog

from package.avaliacao.menu_av import GerenciadorAvaliacao


DADOS_ALUNOS_PATH = "dados/alunos.json"
DADOS_DISCIPLINAS_PATH = "dados/disciplinas.json"

class AvaliacaoGUI(tk.Frame):
    def __init__(self, master, ger_alunos, ger_disciplinas, show_main_menu_callback, salvar_dados_callback):
        super().__init__(master)
        self.master = master
        self.ger_alunos = ger_alunos
        self.ger_disciplinas = ger_disciplinas
        self.show_main_menu_callback = show_main_menu_callback
        self.salvar_dados_callback = salvar_dados_callback

        self.ger_avaliacao = GerenciadorAvaliacao(self.ger_alunos, self.ger_disciplinas)

        self.selected_turma = None

        self.create_widgets()
        self.pack(fill="both", expand=True)

    def create_widgets(self):
        tk.Label(self, text="Modo Avaliação/Frequência", font=("Arial", 18)).pack(pady=10)

        selection_frame = tk.LabelFrame(self, text="Selecionar Turma", padx=10, pady=10)
        selection_frame.pack(pady=10, fill="x", padx=10)

        tk.Label(selection_frame, text="Código da Disciplina:").pack(side=tk.LEFT, padx=5)
        self.codigo_disc_entry = tk.Entry(selection_frame, width=15)
        self.codigo_disc_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(selection_frame, text="Buscar Turmas", command=self.buscar_turmas_para_avaliacao).pack(side=tk.LEFT, padx=5)

        self.turma_listbox = tk.Listbox(selection_frame, height=5, width=50)
        self.turma_listbox.pack(pady=5, padx=5)
        self.turma_listbox.bind("<<ListboxSelect>>", self.on_turma_select)
        
        self.turma_actions_frame = tk.LabelFrame(self, text="Ações da Turma Selecionada", padx=10, pady=10)

        tk.Button(self.turma_actions_frame, text="Lançar Notas", command=self.lancar_notas_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.turma_actions_frame, text="Lançar Presença", command=self.lancar_presencas_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.turma_actions_frame, text="Gerar Boletins", command=self.gerar_boletins_gui).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.turma_actions_frame, text="Relatório da Turma", command=self.gerar_relatorio_turma_gui).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(self, text="Voltar ao Menu Principal", command=self.go_back_to_main_menu).pack(pady=20)

    def buscar_turmas_para_avaliacao(self):
        codigo = self.codigo_disc_entry.get().strip()
        if not codigo:
            messagebox.showerror("Erro", "Por favor, insira o código da disciplina.")
            return

        disciplina = self.ger_disciplinas.buscar_disciplina(codigo)
        if not disciplina or not disciplina.turmas:
            messagebox.showerror("Erro", "Disciplina não encontrada ou sem turmas.")
            return

        self.turma_listbox.delete(0, tk.END)
        self.disciplina_turmas = disciplina.turmas
        
        for i, t in enumerate(disciplina.turmas):
            display_text = f"Turma {i+1}: Prof: {t.professor}, Sem: {t.semestre}, Horário: {t.horario} ({len(t.alunos)}/{t.capacidade} alunos)"
            self.turma_listbox.insert(tk.END, display_text)
        
        self.turma_actions_frame.pack_forget()
        self.selected_turma = None

    def on_turma_select(self, event):
        selected_indices = self.turma_listbox.curselection()
        if not selected_indices:
            return
        
        index = selected_indices[0]
        self.selected_turma = self.disciplina_turmas[index]
        messagebox.showinfo("Turma Selecionada", f"Turma '{self.selected_turma.semestre} - {self.selected_turma.professor}' selecionada.")
        self.turma_actions_frame.pack(pady=10, fill="x", padx=10)

    def lancar_notas_dialog(self):
        if not self.selected_turma:
            messagebox.showerror("Erro", "Nenhuma turma selecionada.")
            return
        
        turma = self.selected_turma
        if not turma.alunos:
            messagebox.showinfo("Info", "Esta turma não possui alunos para lançar notas.")
            return

        for matricula in turma.alunos:
            aluno_obj = self.ger_alunos.buscar_por_matricula(matricula)
            aluno_nome = aluno_obj.nome if aluno_obj else matricula
            
            notas_str = simpledialog.askstring("Lançar Notas", f"Notas para {aluno_nome} ({matricula}) - (P1,P2,P3,L,S separadas por vírgula):")
            if notas_str is None:
                continue
            
            try:
                notas_list = [float(n.strip()) for n in notas_str.split(',')]
                if len(notas_list) != 5:
                    raise ValueError("Número incorreto de notas.")
                
                notas = {
                    "P1": notas_list[0],
                    "P2": notas_list[1],
                    "P3": notas_list[2],
                    "L": notas_list[3],
                    "S": notas_list[4]
                }
                turma.notas[matricula] = notas
                messagebox.showinfo("Sucesso", f"Notas lançadas para {aluno_nome}.")
            except ValueError as e:
                messagebox.showerror("Erro de Notas", f"Formato de notas inválido para {aluno_nome}: {e}. Use P1,P2,P3,L,S com números.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro inesperado para {aluno_nome}: {e}")
        
        self.salvar_dados_callback()

    def lancar_presencas_dialog(self):
        if not self.selected_turma:
            messagebox.showerror("Erro", "Nenhuma turma selecionada.")
            return

        turma = self.selected_turma
        if not turma.alunos:
            messagebox.showinfo("Info", "Esta turma não possui alunos para lançar presenças.")
            return

        for matricula in turma.alunos:
            aluno_obj = self.ger_alunos.buscar_por_matricula(matricula)
            aluno_nome = aluno_obj.nome if aluno_obj else matricula
            
            freq_str = simpledialog.askstring("Lançar Presença", f"Frequência de {aluno_nome} ({matricula}) (%):")
            if freq_str is None:
                continue
            
            try:
                freq = float(freq_str.strip())
                if not (0 <= freq <= 100):
                    raise ValueError("Frequência deve ser entre 0 e 100.")
                turma.presencas[matricula] = freq
                messagebox.showinfo("Sucesso", f"Frequência lançada para {aluno_nome}.")
            except ValueError as e:
                messagebox.showerror("Erro de Frequência", f"Valor de frequência inválido para {aluno_nome}: {e}.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro inesperado para {aluno_nome}: {e}")
        
        self.salvar_dados_callback()

    def gerar_boletins_gui(self):
        if not self.selected_turma:
            messagebox.showerror("Erro", "Nenhuma turma selecionada.")
            return

        boletim_output = ""

        for matricula in self.selected_turma.alunos:
            aluno_obj = self.ger_alunos.buscar_por_matricula(matricula)
            if aluno_obj:
                media = self.ger_avaliacao.calcular_media(self.selected_turma.avaliacao, self.selected_turma.notas.get(matricula, {}))
                freq = self.selected_turma.presencas.get(matricula, 0)
                status = self.ger_avaliacao.status_final(media, freq)
                
                boletim_output += f"Boletim de {aluno_obj.nome} ({matricula}):\n"
                boletim_output += f"  Média: {media:.2f} | Frequência: {freq:.1f}% | Situação: {status}\n\n"

                if status == "Aprovado":
                    if self.selected_turma.codigo_disciplina and self.selected_turma.codigo_disciplina not in aluno_obj.historico:
                        aluno_obj.historico.append(self.selected_turma.codigo_disciplina)

                        self.salvar_dados_callback()
            else:
                boletim_output += f"Aluno com matrícula {matricula} não encontrado para boletim.\n\n"

        if not boletim_output:
            boletim_output = "Não há boletins a serem gerados para esta turma ou nenhum aluno encontrado."
            
        messagebox.showinfo("Boletins da Turma", boletim_output)
        
    def gerar_relatorio_turma_gui(self):
        if not self.selected_turma:
            messagebox.showerror("Erro", "Nenhuma turma selecionada.")
            return
        
        relatorio_output = f"Relatório da turma - {self.selected_turma.professor} ({self.selected_turma.semestre})\n\n"
        
        for matricula in self.selected_turma.alunos:
            aluno_obj = self.ger_alunos.buscar_por_matricula(matricula)
            if aluno_obj:
                media = self.ger_avaliacao.calcular_media(self.selected_turma.avaliacao, self.selected_turma.notas.get(matricula, {}))
                freq = self.selected_turma.presencas.get(matricula, 0)
                status = self.ger_avaliacao.status_final(media, freq)
                
                relatorio_output += f"{aluno_obj.nome} ({matricula}): Média {media:.1f}, Frequência {freq:.1f}%, Situação: {status}\n"
            else:
                relatorio_output += f"Aluno com matrícula {matricula} não encontrado para relatório.\n"
        
        if not self.selected_turma.alunos:
            relatorio_output += "Nenhum aluno matriculado nesta turma."

        messagebox.showinfo("Relatório da Turma", relatorio_output)

    def go_back_to_main_menu(self):
        self.pack_forget()
        self.salvar_dados_callback()
        self.show_main_menu_callback()