from package.utils.serializer import Serializable


class Turma(Serializable):
    def __init__(self, professor, semestre, avaliacao, presencial, horario, sala, capacidade, codigo_disciplina):
        self.professor = professor
        self.semestre = semestre
        self.avaliacao = avaliacao
        self.presencial = presencial
        self.horario = horario
        self.sala = sala if presencial else ""
        self.capacidade = capacidade
        self.codigo_disciplina = codigo_disciplina
        self.alunos = []  # lista de matrículas
        self.notas = {}  # matricula -> dict com P1, P2, P3, L, S
        self.presencas = {}  # matricula -> percentual

    def to_dict(self):
        return {
            "professor": self.professor,
            "semestre": self.semestre,
            "avaliacao": self.avaliacao,
            "presencial": self.presencial,
            "horario": self.horario,
            "sala": self.sala,
            "capacidade": self.capacidade,
            "alunos": self.alunos,
            "notas": self.notas,
            "presencas": self.presencas,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError(f"Esperado um dicionário, mas recebeu um {type(data)}")
        t = cls(data["professor"], data["semestre"], data["avaliacao"],
                data["presencial"], data["horario"], data["sala"], data["capacidade"],
                data.get("codigo_disciplina", None))
        t.alunos = data.get("alunos", [])
        t.notas = data.get("notas", {})
        t.presencas = data.get("presencas", {})
        return t

