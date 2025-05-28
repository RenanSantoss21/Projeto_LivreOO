

class GerenciadorAvaliacao:
    def __init__(self, ger_alunos, ger_disciplinas):
        self.ger_alunos = ger_alunos
        self.ger_disciplinas = ger_disciplinas

    def exibir_menu(self):

        print("\n--- Modo Avaliação/Frequência ---")

        cod = input("Digite o código da disciplina: ")
        disciplina = self.ger_disciplinas.buscar_disciplina(cod)
        if not disciplina or not disciplina.turmas:
            print("Disciplina inválida ou sem turmas.")
            return

        for i, turma in enumerate(disciplina.turmas):
            print(f"{i+1}. {turma.professor} - {turma.semestre} - {turma.horario}")
        try:
            idx = int(input("Escolha a turma: ")) - 1
            turma = disciplina.turmas[idx]
        except (ValueError, IndexError):
            print("Turma inválida.")
            return

        while True:
            print("\n1. Lançar notas")
            print("2. Lançar presença")
            print("3. Gerar boletins")
            print("4. Relatórios da turma")
            print("5. Voltar")
            op = input("Escolha: ")

            if op == "1":
                self.lancar_notas(turma)
            elif op == "2":
                self.lancar_presencas(turma)
            elif op == "3":
                self.gerar_boletins(turma)
            elif op == "4":
                self.gerar_relatorio_turma(turma)
            elif op == "5":
                break
            else:
                print("Opção inválida.")

    def lancar_notas(self, turma):

        if not turma.alunos:
            print("Não há alunos matriculados nesta turma.")
            return

        for matricula in turma.alunos:
            print(f"\nAluno {matricula}:")
            try:
                notas = {
                    "P1": float(input("P1: ")),
                    "P2": float(input("P2: ")),
                    "P3": float(input("P3: ")),
                    "L": float(input("Listas: ")),
                    "S": float(input("Seminário: "))
                }
                turma.notas[matricula] = notas
                self.ger_disciplinas.salvar("dados/disciplinas.json")
            except ValueError:
                print("Notas inválidas.")

    def lancar_presencas(self, turma):

        if not turma.alunos:
            print("Não há alunos matriculados nesta turma.")
            return

        for matricula in turma.alunos:
            try:
                freq = float(input(f"Frequência de {matricula} (%): "))
                turma.presencas[matricula] = freq
                self.ger_disciplinas.salvar("dados/disciplinas.json")
            except ValueError:
                print("Valor inválido.")

    #######

    def gerar_boletins(self, turma):

        for matricula in turma.alunos:
            print(f"DEBUG: Processando matrícula para boletim: {matricula}, Tipo: {type(matricula)}")
            aluno = None # Inicializa aluno para garantir que esteja sempre definido
            try:
                aluno = self.ger_alunos.buscar_por_matricula(matricula)
                print(f"DEBUG: Resultado de buscar_por_matricula para {matricula}: {aluno}")
            except Exception as e:
                print(f"ERRO: Exceção ao buscar aluno com matrícula {matricula}: {e}")
                continue

            if aluno:
                aluno = self.ger_alunos.buscar_por_matricula(matricula)
                media = self.calcular_media(turma.avaliacao, turma.notas.get(matricula, {}))
                freq = turma.presencas.get(matricula, 0)
                status = self.status_final(media, freq)
                print(f"\nBoletim de {aluno.nome} ({matricula})")
                print(f"Média: {media:.2f} | Frequência: {freq:.1f}% | Situação: {status}")
            else:
                print(f"Aluno com matrícula {matricula} não encontrado.")

    def gerar_relatorio_turma(self, turma):
        print(f"\nRelatório da turma - {turma.professor} ({turma.semestre})")
        for matricula in turma.alunos:
            print(f"DEBUG: Processando matrícula para relatório: {matricula}, Tipo: {type(matricula)}")
            aluno = None # Inicializa aluno para garantir que esteja sempre definido
            try:
                aluno = self.ger_alunos.buscar_por_matricula(matricula)
                print(f"DEBUG: Resultado de buscar_por_matricula para {matricula}: {aluno}")
            except Exception as e:
                print(f"ERRO: Exceção ao buscar aluno com matrícula {matricula}: {e}")
                continue # Pula para a próxima matrícula se houver um erro na busca

            if aluno:
                aluno = self.ger_alunos.buscar_por_matricula(matricula)
                media = self.calcular_media(turma.avaliacao, turma.notas.get(matricula, {}))
                freq = turma.presencas.get(matricula, 0)
                status = self.status_final(media, freq)
                print(f"{aluno.nome}: Média {media:.1f}, Frequência {freq:.1f}%, Situação: {status}")
            else:
                print(f"Aluno com matrícula {matricula} não encontrado.")

    def calcular_media(self, tipo, notas):
        if not notas:
            return 0
        p1 = notas.get("P1", 0)
        p2 = notas.get("P2", 0)
        p3 = notas.get("P3", 0)
        l = notas.get("L", 0)
        s = notas.get("S", 0)
        if tipo == "ponderada":
            return (p1 + 2*p2 + 3*p3 + l + s) / 8
        elif tipo == "simples":
            return (p1 + p2 + p3 + l + s) / 5
        else:
            raise ValueError("Tipo de avaliação inválido")

    def status_final(self, media, freq):
        if freq < 75:
            return "Reprovado por falta"
        elif media >= 5:
            return "Aprovado"
        else:
            return "Reprovado por nota"
