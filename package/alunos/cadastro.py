from package.alunos.aluno import Aluno, AlunoEspecial
from package.utils.serializer import carregar_json, salvar_json


class GerenciadorAlunos:
    def __init__(self, ger_disciplinas= None):
        self.ger_disciplinas = ger_disciplinas
        self._alunos = []

    def cadastrar(self, aluno):
        if any(a.matricula == aluno.matricula for a in self._alunos):
            print("Matrícula duplicada!")
        else:
            self._alunos.append(aluno)
            print("Aluno cadastrado com sucesso.")

    def listar(self):
        if not self._alunos:
            print("Nenhum aluno cadastrado.")
        for aluno in self._alunos:
            disciplinas_str = ", ".join(aluno.disciplinas) if aluno.disciplinas else "Nenhuma"
            historico_str = ", ".join(aluno.historico) if aluno.historico else "Nenhum"
            print(f"{aluno} - Disciplinas: {disciplinas_str} - Histórico Matérias: {historico_str}")

    def remover(self, matricula):
        for i, aluno in enumerate(self._alunos):
            if aluno.matricula == matricula:
                del self._alunos[i]
                print("Aluno removido com sucesso.")
                return
        print("Matrícula não encontrada.")

    def matricular(self, aluno, turma):

        if len(turma.alunos) == turma.capacidade:
            print(f"Turma cheia ({turma.capacidade} alunos).")
            return False
        
        if aluno.matricula in turma.alunos:
            print(f"Aluno {aluno.nome} já está matriculado nesta turma.")
            return False
        
        # --- LÓGICA DE PRÉ-REQUISITO ---
        # Acessamos a disciplina para obter seus pré-requisitos
        if not self.ger_disciplinas:
            print("Erro: Gerenciador de Disciplinas não configurado para verificação de pré-requisitos.")
            return False

        disciplina = self.ger_disciplinas.buscar_disciplina(turma.codigo_disciplina)
        if disciplina and disciplina.pre_requisitos:
            for pre_req_codigo in disciplina.pre_requisitos:
                if pre_req_codigo not in aluno.historico:
                    print(f"Aluno {aluno.nome} não possui o pré-requisito: {pre_req_codigo}")
                    return False
        # --- FIM DA LÓGICA DE PRÉ-REQUISITO ---

        # if aluno.tipo:
        #     turmas_atual = [t for t in aluno.turmas if t.semestre == turma.semestre]
        #     if len(turmas_atual) >= 2:
        #         print(f"Aluno especial só pode cursar até 2 disciplinas.")
        #         return False

        turma.alunos.append(aluno.matricula)
        aluno.disciplinas.append(turma.codigo_disciplina)
        turma.capacidade -= 1
        print(f"Aluno {aluno.nome} matriculado na turma ({turma.codigo_disciplina}).")
        return True
    
    def trancar_matricula(self, aluno, turma):

        if aluno.matricula not in turma.alunos:
            print(f"Aluno {aluno.nome} não está matriculado nesta turma.")
            return False

        turma.alunos.remove(aluno.matricula)
        
        # print(f"DEBUG: Tentando remover disciplina {turma.codigo_disciplina} do aluno {aluno.nome}'s disciplinas.")
        if turma.codigo_disciplina in aluno.disciplinas:
            aluno.disciplinas.remove(turma.codigo_disciplina)
            # print(f"DEBUG: Disciplina {turma.codigo_disciplina} removida do histórico do aluno.")
        else:
            # print(f"DEBUG: Disciplina {turma.codigo_disciplina} NÃO encontrada no histórico do aluno (já removida ou código diferente).")
            pass

        if aluno.matricula in turma.notas:
            del turma.notas[aluno.matricula]
        if aluno.matricula in turma.presencas:
            del turma.presencas[aluno.matricula]

        turma.capacidade += 1
        print(f"Matrícula de {aluno.nome} na turma '{turma.codigo_disciplina}' trancada com sucesso.")
        return True

    def buscar_por_matricula(self, matricula):
        for a, aluno in enumerate(self._alunos):
            if aluno.matricula == matricula:
                aluno = self._alunos[a]
                return aluno
        return None


    def salvar(self, caminho):
        dados = [a.to_dict() for a in self._alunos]
        salvar_json(caminho, dados)

    def carregar(self, caminho):
        self._alunos = []
        for d in carregar_json(caminho):
            tipo = d.get("tipo", "normal")
            aluno = AlunoEspecial.from_dict(d) if tipo == "especial" else Aluno.from_dict(d)
            self._alunos.append(aluno)
