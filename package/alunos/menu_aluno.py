from package.alunos.aluno import Aluno, AlunoEspecial

dados_alunos_path = "dados/alunos.json"
dados_disciplinas_path = "dados/disciplinas.json"


class Menu_aluno:
    def __init__(self, ger_alunos, ger_disciplinas):
        self.ger_disciplinas = ger_disciplinas
        self.ger_alunos = ger_alunos

    def menu(self):
        while True:
            print("\n=== Sistema Acadêmico - Modo Aluno ===")
            print("1. Cadastrar Aluno")
            print("2. Listar Alunos")
            print("3. Remover Aluno")
            print("4. Matricular Aluno em Turma")
            print("5. Trancamento de matricula")
            print("6. Voltar")
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
                self.ger_alunos.cadastrar(aluno)
                self.ger_alunos.salvar(dados_alunos_path)

            elif opcao == "2":
                self.ger_alunos.listar()

            elif opcao == "3":
                matricula = input("Digite a matrícula do aluno a ser removido: ")
                self.ger_alunos.remover(matricula)
                self.ger_alunos.salvar(dados_alunos_path)

            elif opcao == "4":
                matricula = input("Digite a matrícula do aluno: ")
                codigo = input("Digite o código da disciplina: ")
                disciplina = self.ger_disciplinas.buscar_disciplina(codigo)
                if not disciplina or not disciplina.turmas:
                    print("Disciplina inválida ou sem turmas.")
                    continue
                print("Turmas disponíveis:")
                for i, turma in enumerate(disciplina.turmas):
                    print(f"{i + 1}. {turma}")
                try:
                    idx = int(input("Digite a turma: ")) - 1
                    turma = disciplina.turmas[idx]
                except (ValueError, IndexError):
                    print("Turma inválida.")
                    continue

                aluno = self.ger_alunos.buscar_por_matricula(matricula)
                if aluno:
                    self.ger_alunos.matricular(aluno, turma)
                    self.ger_alunos.salvar(dados_alunos_path)
                    self.ger_disciplinas.salvar(dados_disciplinas_path)
                else:
                    print("Aluno não encontrado.")
                self.ger_alunos.salvar(dados_alunos_path)

            elif opcao == "5":
                matricula = input("Digite a matrícula do aluno: ")
                codigo = input("Digite o código da disciplina: ")

                disciplina = self.ger_disciplinas.buscar_disciplina(codigo)
                if not disciplina or not disciplina.turmas:
                    print("Disciplina inválida ou sem turmas.")
                    continue

                aluno = self.ger_alunos.buscar_por_matricula(matricula)
                if not aluno:
                    print("Aluno não encontrado.")
                    continue

                turma_encontrada = None
                for turma_aluno in disciplina.turmas:
                    if matricula in turma_aluno.alunos:
                        turma_encontrada = turma_aluno
                        break
                
                if turma_encontrada:
                    self.ger_alunos.trancar_matricula(aluno, turma_encontrada)
                    self.ger_alunos.salvar(dados_alunos_path)
                    self.ger_disciplinas.salvar(dados_disciplinas_path)
                else:
                    print(f"Aluno {aluno.nome} não encontrado em nenhuma turma da disciplina {turma.codigo_disciplina}.")

            elif opcao == "6":
                break
            else:
                print("Opção inválida.")
