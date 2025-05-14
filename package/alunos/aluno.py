

class Aluno:
    def __init__(self, nome, matricula, curso):
        self.nome = nome
        self.matricula = matricula
        self.curso = curso
        self.disciplinas = []

    def to_dict(self):
        return {
            "tipo": "normal",
            "nome": self.nome,
            "matricula": self.matricula,
            "curso": self.curso,
            "matriculas": self.disciplinas,
        }

    @staticmethod
    def from_dict(data):
        aluno = Aluno(data["nome"], data["matricula"], data["curso"])
        aluno.disciplinas = data.get("disciplinas", [])
        return aluno

    def __str__(self):
        return f"{self.nome} - {self.matricula} - {self.curso}"


class AlunoEspecial(Aluno):
    def __init__(self, nome, matricula, curso, lim_matriculas):
        super().__init__(nome, matricula, curso)
        self.lim_matriculas = 2
        self.disciplinas = []

    def PodeAdicionarDisciplina(self, disciplina):
        if len(self.disciplinas) <= self.lim_matriculas:
            self.disciplinas.append(disciplina)
            return True
        else:
            return False

    def to_dict(self):
        base = super().to_dict()
        base["tipo"] = "especial"
        return base

    @staticmethod
    def from_dict(data):
        aluno = AlunoEspecial(data["nome"], data["matricula"], data["curso"])
        aluno.disciplinas = data.get("disciplinas", [])
        return aluno
