

class Aluno:
    
    def __init__(self, nome, matricula, curso):
        self._nome = nome
        self._matricula = matricula
        self._curso = curso
        self._disciplinas = []

    @property
    def matricula(self):
        return self._matricula

    @property
    def nome(self):
        return self._nome

    def to_dict(self):
        return {
            "tipo": "normal",
            "nome": self._nome,
            "matricula": self._matricula,
            "curso": self._curso,
            "disciplinas": self._disciplinas,
        }

    @classmethod
    def from_dict(cls, data):
        aluno = cls(data["nome"], data["matricula"], data["curso"])
        aluno._disciplinas = data.get("disciplinas", [])
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
