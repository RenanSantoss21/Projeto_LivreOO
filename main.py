from package.alunos.cadastro import GerenciadorAlunos
from package.disciplinas.cadastro import GerenciadorDisciplinas
from package.alunos.aluno import Aluno, AlunoEspecial
from package.disciplinas.disciplina import Disciplina
from package.disciplinas.turma import Turma
from package.menu_av import menu_avaliacao
import os

dados_alunos_path = "dados/alunos.json"
dados_disciplinas_path = "dados/disciplinas.json"

def menu_aluno(ger_alunos):
    while True:
        print("\n--- Modo Aluno ---")
        print("1. Cadastrar Aluno")
        print("2. Listar Alunos")
        print("3. Voltar")
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

        elif opcao == "2":
            ger_alunos.listar()

        elif opcao == "3":
            break
        else:
            print("Opção inválida.")

def menu_disciplina(ger_disciplinas):
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

        elif opcao == "3":
            for d in ger_disciplinas._disciplinas:
                print(f"\nDisciplina: {d.codigo} - {d.nome}")
                for i, t in enumerate(d.turmas):
                    print(f"  Turma {i+1}: {t.professor} - {t.semestre} - {t.horario} - Cap: {t.capacidade}")

        elif opcao == "4":
            break
        else:
            print("Opção inválida.")

def main():
    ger_alunos = GerenciadorAlunos()
    ger_disciplinas = GerenciadorDisciplinas()

    os.makedirs("dados", exist_ok=True)
    ger_alunos.carregar(dados_alunos_path)
    ger_disciplinas.carregar(dados_disciplinas_path)

    while True:
        print("\n=== Sistema Acadêmico - FCTE ===")
        print("1. Modo Aluno")
        print("2. Modo Disciplina/Turma")
        print("3. Modo Avaliação/Frequência")
        print("4. Sair")
        escolha = input("Escolha: ")

        if escolha == "1":
            menu_aluno(ger_alunos)

        elif escolha == "2":
            menu_disciplina(ger_disciplinas)

        elif escolha == "3":
            menu_avaliacao(ger_alunos, ger_disciplinas)

        elif escolha == "4":
            ger_alunos.salvar(dados_alunos_path)
            ger_disciplinas.salvar(dados_disciplinas_path)
            print("Encerrando com segurança. Dados salvos!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
