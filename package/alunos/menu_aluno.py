from package.alunos.cadastro import GerenciadorAlunos
from package.disciplinas.cadastro import GerenciadorDisciplinas
from package.alunos.aluno import Aluno, AlunoEspecial

ger_alunos = GerenciadorAlunos()
ger_disciplinas = GerenciadorDisciplinas()


dados_alunos_path = "dados/alunos.json"
ger_alunos.carregar(dados_alunos_path)


class Menu_aluno:
    def __init__(self, ger_alunos):
        self.ger_alunos = ger_alunos

    def menu(self):
        while True:
            print("\n=== Sistema Acadêmico - Modo Aluno ===")
            print("1. Cadastrar Aluno")
            print("2. Listar Alunos")
            print("3. Remover Aluno")
            print("4. Matricular Aluno em Turma")
            print("5. Voltar")
            opcao = input("Escolha: ")

            if opcao == "1":
                nome = input("Nome: ")
                matricula = input("Matrícula: ")
                curso = input("Curso: ")
                tipo = input("Tipo (normal/especial): ")
                if tipo.lower() == "especial":
                    aluno = AlunoEspecial(nome, matricula, curso)
                else:
                    aluno = Aluno(nome, matricula, curso)
                ger_alunos.cadastrar(aluno)
                ger_alunos.salvar(dados_alunos_path)

            elif opcao == "2":
                ger_alunos.listar()

            elif opcao == "3":
                matricula = input("Digite a matrícula do aluno a ser removido: ")
                ger_alunos.remover(matricula)
                ger_alunos.salvar(dados_alunos_path)

            elif opcao == "4":
                matricula = input("Digite a matrícula do aluno: ")
                codigo = input("Digite o código da disciplina: ")
                disciplina = ger_disciplinas.buscar_disciplina(codigo)
                if not disciplina or not disciplina.turmas:
                    print("Disciplina inválida ou sem turmas.")
                    return
                try:
                    idx = int(input("Digite a turma: ")) - 1
                    turma = disciplina.turmas[idx]
                except (ValueError, IndexError):
                    print("Turma inválida.")
                    return
                aluno = ger_alunos.buscar_por_matricula(matricula)
                if aluno:
                    ger_alunos.matricular(aluno, turma)
                else:
                    print("Aluno não encontrado.")
                ger_alunos.salvar(dados_alunos_path)

            elif opcao == "5":
                
                break
            else:
                print("Opção inválida.")
