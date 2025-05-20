from alunos import Aluno, AlunoEspecial
from utils.serializer import carregar_json, salvar_json


class GerenciadorAlunos:
    def __init__(self):
        self._alunos = []

    def cadastrar(self, aluno):
        if any(a.matricula == aluno.matricula for a in self._alunos):
            print("Matrícula duplicada!")
        else:
            self._alunos.append(aluno)
            print("Aluno cadastrado com sucesso.")

    def listar(self):
        if not self._alunos:
            print("Nenhum aluno cadastrado.")
        for aluno in self._alunos:
            print(aluno)

    def salvar(self, caminho):
        dados = [a.to_dict() for a in self._alunos]
        salvar_json(caminho, dados)

    def carregar(self, caminho):
        self._alunos = []
        for d in carregar_json(caminho):
            tipo = d.get("tipo", "normal")
            aluno = AlunoEspecial.from_dict(d) if tipo == "especial" else Aluno.from_dict(d)
            self._alunos.append(aluno)

    def buscar_por_matricula(self, matricula):
        for a in self._alunos:
            if a.matricula == matricula:
                return a
        return None
