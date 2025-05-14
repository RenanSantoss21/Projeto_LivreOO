from disciplinas.turma import Turma


class Disciplina:
    def __init__(self, nome, codigo, carga_horaria, pre_requisitos=None):
        self.nome = nome
        self.codigo = codigo
        self.carga_horaria = carga_horaria
        self.pre_requisitos = pre_requisitos or []
        self.turmas = []

    def to_dict(self):
        return {
            "nome": self.nome,
            "codigo": self.codigo,
            "carga_horaria": self.carga_horaria,
            "pre_requisitos": self.pre_requisitos,
            "turmas": [turma.to_dict() for turma in self.turmas]
        }

    @staticmethod
    def from_dict(data):
        d = Disciplina(data["nome"], data["codigo"], data["carga_horaria"], data["pre_requisitos"])
        d.turmas = [Turma.from_dict(t) for t in data.get("turmas", [])]
        return d

    def __str__(self):
        return f"{self.nome} ({self.codigo}) - {self.carga_horaria}h"
