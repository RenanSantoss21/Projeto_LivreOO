from package.disciplinas.disciplina import Disciplina
from package.utils.serializer import salvar_json, carregar_json


class GerenciadorDisciplinas:

    def __init__(self):
        self._disciplinas = []

    def adicionar_disciplina(self, disciplina):
        if self.buscar_disciplina(disciplina.codigo):
            print(f"Erro: Disciplina com código '{disciplina.codigo}' já existe.")
            return False
        self._disciplinas.append(disciplina)
        print("Disciplina adicionada.")
        return True
    
    def remover_disciplina(self, codigo):
        for i, disc in enumerate(self._disciplinas):
            if disc.codigo == codigo:
                if disc.turmas:
                    print(f"Erro: Não é possível remover a disciplina {disc.nome} (código {codigo}) pois ela possui turmas ativas.")
                    return False
                del self._disciplinas[i]
                print(f"Disciplina com código '{codigo}' removida com sucesso.")
                return True
        print(f"Erro: Disciplina com código '{codigo}' não encontrada.")
        return False
    
    def remover_turma(self, codigo, idx_turma):
        disc = self.buscar_disciplina(codigo)
        if disc:
            if 0 <= idx_turma < len(disc.turmas):
                turma = disc.turmas[idx_turma]
                if turma.alunos:
                    print(f"Erro: Não é possível remover a turma do professor {turma.professor} (semestre {turma.semestre}) pois ela possui alunos matriculados.")
                    return False
                del disc.turmas[idx_turma]
                print(f"Turma removida da disciplina '{codigo}'.")
                return True
            print(f"Erro: Índice de turma inválido para disciplina '{codigo}'.")
            return False
        print(f"Erro: Disciplina com código '{codigo}' não encontrada para remover turma.")
        return False
    
    def editar_disciplina(self, codigo, novos_dados):
        disc = self.buscar_disciplina(codigo)
        if disc:
            disc.nome = novos_dados.get("nome", disc.nome)
            disc.carga_horaria = novos_dados.get("carga_horaria", disc.carga_horaria)
            disc.pre_requisitos = novos_dados.get("pre_requisitos", disc.pre_requisitos)
            print(f"Disciplina '{codigo}' atualizada com sucesso.")
            return True
        print(f"Erro: Disciplina com código '{codigo}' não encontrada para edição.")
        return False
    
    def editar_turma(self, codigo, idx_turma, novos_dados):
        disc = self.buscar_disciplina(codigo)
        if disc:
            if 0 <= idx_turma < len(disc.turmas):
                turma = disc.turmas[idx_turma]
                turma.professor = novos_dados.get("professor", turma.professor)
                turma.semestre = novos_dados.get("semestre", turma.semestre)
                turma.avaliacao = novos_dados.get("avaliacao", turma.avaliacao)
                turma.presencial = novos_dados.get("presencial", turma.presencial)
                turma.horario = novos_dados.get("horario", turma.horario)
                if turma.presencial:
                    turma.sala = novos_dados.get("sala", turma.sala)
                else:
                    turma.sala = ""
                turma.capacidade = novos_dados.get("capacidade", turma.capacidade)
                print(f"Turma da disciplina '{codigo}' (índice {idx_turma}) atualizada com sucesso.")
                return True
            print(f"Erro: Índice de turma inválido para disciplina '{codigo}'.")
            return False
        print(f"Erro: Disciplina com código '{codigo}' não encontrada para editar turma.")
        return False

    def buscar_disciplina(self, codigo):
        for d, disc in enumerate(self._disciplinas):
            if disc.codigo == codigo:
                disciplina = self._disciplinas[d]
                return disciplina
        return None

    def salvar(self, caminho):
        dados = [d.to_dict() for d in self._disciplinas]
        salvar_json(caminho, dados)

    def carregar(self, caminho):
        self._disciplinas = []
        for d in carregar_json(caminho):
            self._disciplinas.append(Disciplina.from_dict(d))
