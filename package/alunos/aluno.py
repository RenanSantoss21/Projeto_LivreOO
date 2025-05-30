from package.utils.serializer import Serializable


class Aluno(Serializable):
    
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
    def curso(self):
        return self._curso

    @property
    def disciplinas(self):
        return self._disciplinas

    @property
    def historico(self):
        return self._historico
    
    def pode_matricular(self, turma, ger_disciplinas):

        disciplina = ger_disciplinas.buscar_disciplina(turma.codigo_disciplina)
        if not disciplina:
            return False, "Erro interno: Disciplina da turma não encontrada."

        if disciplina.pre_requisitos:
            for pre_req_codigo in disciplina.pre_requisitos:
                if pre_req_codigo not in self.historico:
                    return False, f"Não possui o pré-requisito: {pre_req_codigo}"
        
        return True, "Pode matricular." 

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
    
    def pode_matricular(self, turma, ger_disciplinas):

        pode_matricular_base, mensagem_base = super().pode_matricular(turma, ger_disciplinas)
        if not pode_matricular_base:
            return False, mensagem_base

        disciplinas_no_semestre_da_turma = 0
        for disc_codigo_ativa in self.disciplinas:
            disc_ativa_obj = ger_disciplinas.buscar_disciplina(disc_codigo_ativa)
            if disc_ativa_obj:
                for t_ativa in disc_ativa_obj.turmas:
                    if t_ativa.semestre == turma.semestre and self.matricula in t_ativa.alunos:
                        disciplinas_no_semestre_da_turma += 1
                        break

        if disciplinas_no_semestre_da_turma >= 2:
            return False, f"Aluno especial já está matriculado em 2 disciplinas no semestre {turma.semestre}."
        
        return True, "Pode matricular."

    def to_dict(self):
        base = super().to_dict()
        base["tipo"] = "especial"
        return base

    def __str__(self):
        return f"{self._nome} ({self._matricula}) - {self._curso} [ESPECIAL]"
