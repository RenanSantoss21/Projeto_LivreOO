

class Turma:

    def __init__(self, professor, semestre, avaliacao, presencial, horario, sala, capacidade):
        self.professor = professor
        self.semestre = semestre
        self.avaliacao = avaliacao # 'simples' ou 'ponderada'
        self.presencial = presencial
        self.horario = horario
        self.sala = sala if presencial else "Remota"
        self.capacidade = capacidade
        self.alunos = []
        self.notas = {}
        self.frequencias = {}

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
            "frequencias": self.frequencias,
        }

    @staticmethod
    def from_dict(data):
        t = Turma(
            data["professor"], data["semestre"], data["avaliacao"],
            data["presencial"], data["horario"],
            data.get("sala", "Remota"), data["capacidade"]
        )
        t.alunos = data.get("alunos", [])
        t.notas = data.get("notas", {})
        t.frequencias = data.get("frequencias", {})
        return t

    def calcular_media(self, matricula):
        notas = self.notas.get(matricula)
        if not notas:
            return None
        if self.avaliacao == 'simples':
            return sum([notas.get(n, 0) for n in ['P1', 'P2', 'P3', 'L', 'S']]) / 5
        else:  # ponderada
            return (
                notas.get('P1', 0) +
                notas.get('P2', 0) * 2 +
                notas.get('P3', 0) * 3 +
                notas.get('L', 0) +
                notas.get('S', 0)
            ) / 8

    def resultado_aluno(self, matricula):
        media = self.calcular_media(matricula)
        frequencia = self.frequencia.get(matricula, 0)
        if frequencia < 75:
            return "Reprovado por falta"
        elif media is not None and media >= 5:
            return "Aprovado"
        else:
            return "Reprovado por nota"

    def __str__(self):
        tipo = "Presencial" if self.presencial else "Remota"
        return f"""{self.semestre} 
        Prof: {self.professor} | {tipo} 
        Horário: {self.horario} 
        Sala: {self.sala}  
        Capacidade: {self.capacidade}"""
