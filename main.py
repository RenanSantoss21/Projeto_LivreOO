from package.alunos.cadastro import GerenciadorAlunos
from package.disciplinas.cadastro import GerenciadorDisciplinas
from package.alunos.menu_aluno import Menu_aluno
from package.avaliacao.menu_av import GerenciadorAvaliacao
from package.disciplinas.menu_disc import Menu_disciplina
import os

dados_alunos_path = "dados/alunos.json"
dados_disciplinas_path = "dados/disciplinas.json"

ger_avaliacao = GerenciadorAvaliacao(ger_alunos= None, ger_disciplinas= None)
menu_aluno = Menu_aluno(GerenciadorAlunos())
menu_disciplina = Menu_disciplina(GerenciadorDisciplinas())

def loop():
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
            menu_aluno.menu()

        elif escolha == "2":
            menu_disciplina.menu()

        elif escolha == "3":
            ger_avaliacao.exibir_menu()

        elif escolha == "4":
            print("Encerrando. Dados salvos!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    loop()
