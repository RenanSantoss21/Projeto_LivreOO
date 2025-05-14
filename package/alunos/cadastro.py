from package.utils.serializer import salvar_json, carregar_json


class GerenciadorAlunos:
    def __init__(self):
        self.alunos = []

    def cadastrar_aluno(self, aluno):
        if not any(a.matricula == aluno.matricula for a in self.alunos):
            self.alunos.append(aluno)
        else:
            print("Erro: Matrícula já cadastrada.")

    def listar_alunos(self):
        for aluno in self.alunos:
            print(aluno)

    def buscar_aluno_por_matricula(self, matricula):
        return next((a for a in self.alunos if a.matricula == matricula), None)

    def salvar(self, caminho):
        salvar_json(caminho, self.alunos)

    def carregar(self, caminho):
        self.alunos = carregar_json(caminho)
