

class Disciplina:
    def __init__(self, nome, codigo, carga_horaria, pre_requisitos=None):
        self.nome = nome
        self.codigo = codigo
        self.carga_horaria = carga_horaria
        self.pre_requisitos = pre_requisitos if pre_requisitos else []
        self.turmas = []

    def to_dict(self):
        return {
            "nome": self.nome,
            "codigo": self.codigo,
            "carga_horaria": self.carga_horaria,
            "pre_requisitos": self.pre_requisitos,
            "turmas": [t.to_dict() for t in self.turmas],
        }

    @classmethod
    def from_dict(cls, data):
        from .turma import Turma
        d = cls(data["nome"], data["codigo"], data["carga_horaria"], data.get("pre_requisitos", []))
        d.turmas = [Turma.from_dict(td) for td in data.get("turmas", [])]
        return d

