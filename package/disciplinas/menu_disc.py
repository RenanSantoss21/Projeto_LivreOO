from package.disciplinas.disciplina import Disciplina
from package.disciplinas.turma import Turma
from package.disciplinas.cadastro import GerenciadorDisciplinas
ger_disciplinas = GerenciadorDisciplinas()

dados_disciplinas_path = "dados/disciplinas.json"
ger_disciplinas.carregar(dados_disciplinas_path)


class Menu_disciplina:

    def __init__(self, ger_disciplinas):
        self.ger_disciplinas = ger_disciplinas
    
    def menu(self):
        while True:
            print("\n--- Modo Disciplina/Turma ---")
            print("1. Cadastrar Disciplina")
            print("2. Criar Turma")
            print("3. Listar Disciplinas e Turmas")
            print("4. Voltar")
            opcao = input("Escolha: ")

            if opcao == "1":
                nome = input("Nome da Disciplina: ")
                codigo = input("Código: ")
                ch = int(input("Carga horária: "))
                pre = input("Pré-requisitos (códigos separados por vírgula): ").split(',')
                disciplina = Disciplina(nome, codigo, ch, [p.strip() for p in pre if p.strip()])
                ger_disciplinas.adicionar_disciplina(disciplina)
                ger_disciplinas.salvar(dados_disciplinas_path)

            elif opcao == "2":
                codigo = input("Código da disciplina: ")
                disciplina = ger_disciplinas.buscar_disciplina(codigo)
                if not disciplina:
                    print("Disciplina não encontrada.")
                    continue
                professor = input("Professor responsável: ")
                semestre = input("Semestre (ex: 2025.1): ")
                avaliacao = input("Forma de avaliação (simples/ponderada): ")
                presencial = input("Presencial? (s/n): ").lower() == 's'
                sala = input("Sala (se presencial): ") if presencial else ""
                horario = input("Horário: ")
                capacidade = int(input("Capacidade máxima: "))
                turma = Turma(professor, semestre, avaliacao, presencial, horario, sala, capacidade)
                disciplina.turmas.append(turma)
                ger_disciplinas.salvar(dados_disciplinas_path)

            elif opcao == "3":
                for d in ger_disciplinas._disciplinas:
                    print(f"\nDisciplina: {d.codigo} - {d.nome}")
                    for i, t in enumerate(d.turmas):
                        print(f"  Turma {i+1}: {t.professor} - {t.semestre} - {t.horario} - Cap: {t.capacidade}")

            elif opcao == "4":
                break
            else:
                print("Opção inválida.")