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
        aluno_rem = None
        for i, aluno in enumerate(self._alunos):
            if aluno.matricula == matricula:
                aluno_rem = self._alunos.pop(i)
                if self.ger_disciplinas:
                    for disc in self.ger_disciplinas._disciplinas:
                        for turma in disc.turmas:
                            if matricula in turma.alunos:
                                turma.alunos.remove(matricula)
                                if matricula in turma.notas:
                                    del turma.notas[matricula]
                                if matricula in turma.presencas:
                                    del turma.presencas[matricula]
                                turma.capacidade += 1
                                print(f"Aluno desvinculado da turma {disc.codigo} - {turma.semestre}.")
                return True
        print("Matrícula não encontrada.")
        return False

    def matricular(self, aluno, turma):

        if len(turma.alunos) >= turma.capacidade:
            print(f"Turma cheia ({turma.capacidade} alunos).")
            return False
        
        if aluno.matricula in turma.alunos:
            print(f"Aluno {aluno.nome} já está matriculado nesta turma.")
            return False
        
        if not self.ger_disciplinas:
            print("Erro: Gerenciador de Disciplinas não configurado para verificação de pré-requisitos.")
            return False

        disciplina = self.ger_disciplinas.buscar_disciplina(turma.codigo_disciplina)
        if disciplina and disciplina.pre_requisitos:
            for pre_req_codigo in disciplina.pre_requisitos:
                if pre_req_codigo not in aluno.historico:
                    print(f"Aluno {aluno.nome} não possui o pré-requisito: {pre_req_codigo}")
                    return False
        
        # --- REGRA PARA ALUNO ESPECIAL: Limite de 2 disciplinas ativas por semestre ---
        if isinstance(aluno, AlunoEspecial):
            turmas_ativas_do_aluno = []
            for disc_codigo in aluno.disciplinas:
                disc_ativa = self.ger_disciplinas.buscar_disciplina(disc_codigo)
                if disc_ativa:
                    for t_ativa in disc_ativa.turmas:
                        if t_ativa.semestre == turma.semestre and aluno.matricula in t_ativa.alunos:
                            turmas_ativas_do_aluno.append(t_ativa)
                            break
            
            if len(turmas_ativas_do_aluno) >= 2:
                print(f"Aluno especial {aluno.nome} já está matriculado em 2 disciplinas no semestre {turma.semestre}.")
                return False
        # --- FIM DA REGRA ALUNO ESPECIAL ---


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

        if turma.codigo_disciplina in aluno.disciplinas:
            aluno.disciplinas.remove(turma.codigo_disciplina)

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
