from package.alunos.aluno import Aluno, AlunoEspecial
from package.disciplinas.cadastro import GerenciadorDisciplinas
from package.utils.serializer import carregar_json, salvar_json
gr_disc = GerenciadorDisciplinas()


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

    def remover(self, matricula):
        for i, aluno in enumerate(self._alunos):
            if aluno.matricula == matricula:
                del self._alunos[i]
                print("Aluno removido com sucesso.")
                return
        print("Matrícula não encontrada.")

    def matricular(self, aluno, turma):

        if len(turma.alunos) >= turma.capacidade:
            print(f"Turma cheia ({turma.capacidade} alunos).")
            return False
        
        if aluno in turma.alunos:
            print(f"Aluno {aluno.nome} já está matriculado nesta turma.")
            return False
        
        # for cod in turma.disciplina.pre_requisitos:
        #     if cod not in aluno.historico:
        #         print(f"Aluno não cursou o pré-requisito: {cod}")
        #         return False

        # if aluno.tipo:
        #     turmas_atual = [t for t in aluno.turmas if t.semestre == turma.semestre]
        #     if len(turmas_atual) >= 2:
        #         print(f"Aluno especial só pode cursar até 2 disciplinas.")
        #         return False

        turma.alunos.append(aluno)
        aluno.disciplinas.append(turma)
        turma.capacidade -= 1
        print(f"Aluno {aluno.nome} matriculado na turma.")
        return True

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
        for a, aluno in enumerate(self._alunos):
            if aluno.matricula == matricula:
                aluno = self._alunos[a]
                return aluno
        return None
