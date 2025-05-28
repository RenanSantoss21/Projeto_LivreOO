from package.disciplinas.turma import Turma


class Aluno:
    
    def __init__(self, nome, matricula, curso):
        self._nome = nome
        self._matricula = matricula
        self._curso = curso
        self._disciplinas = [] # Disciplinas que o aluno está matriculado ATUALMENTE.
        self._historico = [] # Histórico de disciplinas JÁ cursadas pelo aluno (e foi APROVADO).

    @property
    def matricula(self):
        return self._matricula

    @property
    def nome(self):
        return self._nome

    @property
    def disciplinas(self):
        return self._disciplinas

    @property
    def historico(self):
        return self._historico

    def to_dict(self):
        return {
            "tipo": "normal",
            "nome": self._nome,
            "matricula": self._matricula,
            "curso": self._curso,
            "disciplinas": self._disciplinas,
            "historico": self._historico
        }

    @classmethod
    def from_dict(cls, data):
        aluno = cls(data["nome"], data["matricula"], data["curso"])
        aluno._disciplinas = data.get("disciplinas", [])
        aluno._historico = data.get("historico", [])
        return aluno

    def __str__(self):
        return f"{self._nome} ({self._matricula}) - {self._curso}"

class AlunoEspecial(Aluno):
    def __init__(self, nome, matricula, curso):
        super().__init__(nome, matricula, curso)

    def to_dict(self):
        base = super().to_dict()
        base["tipo"] = "especial"
        return base

    def __str__(self):
        return f"{self._nome} ({self._matricula}) - {self._curso} [ESPECIAL]"
