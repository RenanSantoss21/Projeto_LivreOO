import json
from disciplinas.disciplina import Disciplina


class GerenciadorDisciplinas:
    def __init__(self):
        self.disciplinas = []

    def cadastrar_disciplina(self, disciplina):
        if not any(d.codigo == disciplina.codigo for d in self.disciplinas):
            self.disciplinas.append(disciplina)
        else:
            print("Erro: Código de disciplina já cadastrado.")

    def listar_disciplinas(self):
        for d in self.disciplinas:
            print(d)

    def buscar_disciplina(self, codigo):
        return next((d for d in self.disciplinas if d.codigo == codigo), None)

    def criar_turma(self, codigo_disciplina, turma):
        disciplina = self.buscar_disciplina(codigo_disciplina)
        if disciplina:
            if all(t.horario != turma.horario for t in disciplina.turmas):
                disciplina.turmas.append(turma)
            else:
                print("Erro: Já existe uma turma nesse horário.")
        else:
            print("Disciplina não encontrada.")

    def listar_turmas(self):
        for d in self.disciplinas:
            print(f"\nDisciplina: {d.nome} ({d.codigo})")
            for i, turma in enumerate(d.turmas, start=1):
                print(f"  Turma {i}: {turma}")
                print(f"    Alunos matriculados: {len(turma.alunos)}")

    def salvar(self, caminho):
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump([d.to_dict() for d in self.disciplinas], f, ensure_ascii=False, indent=4)

    def carregar(self, caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            self.disciplinas = [Disciplina.from_dict(d) for d in dados]
        except FileNotFoundError:
            self.disciplinas = []
