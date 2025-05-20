

def menu_avaliacao(ger_alunos, ger_disciplinas):
    print("\n--- Modo Avaliação/Frequência ---")

    cod = input("Digite o código da disciplina: ")
    disciplina = ger_disciplinas.buscar_disciplina(cod)
    if not disciplina:
        print("Disciplina não encontrada.")
        return

    if not disciplina.turmas:
        print("Disciplina não possui turmas.")
        return

    for i, turma in enumerate(disciplina.turmas):
        print(f"{i+1}. {turma.professor} - {turma.semestre} - {turma.horario}")
    idx = int(input("Escolha a turma: ")) - 1

    if idx < 0 or idx >= len(disciplina.turmas):
        print("Turma inválida.")
        return

    turma = disciplina.turmas[idx]

    while True:
        print("\n1. Lançar notas")
        print("2. Lançar presença")
        print("3. Gerar boletins")
        print("4. Relatórios")
        print("5. Voltar")
        op = input("Escolha: ")

        if op == "1":
            for matricula in turma.alunos:
                print(f"\nAluno {matricula}:")
                p1 = float(input("P1: "))
                p2 = float(input("P2: "))
                p3 = float(input("P3: "))
                l = float(input("Listas: "))
                s = float(input("Seminário: "))
                turma.notas[matricula] = {"P1": p1, "P2": p2, "P3": p3, "L": l, "S": s}

        elif op == "2":
            for matricula in turma.alunos:
                freq = float(input(f"Frequência do aluno {matricula} (%): "))
                turma.presencas[matricula] = freq

        elif op == "3":
            for matricula in turma.alunos:
                notas = turma.notas.get(matricula, {})
                freq = turma.presencas.get(matricula, 0)
                media = calcular_media(turma.avaliacao, notas)
                status = status_final(media, freq)
                aluno = ger_alunos.buscar_por_matricula(matricula)
                print(f"\nBoletim: {aluno.nome}")
                print(f"Média: {media:.2f} | Frequência: {freq:.1f}% | Situação: {status}")

        elif op == "4":
            print(f"\nRelatório da turma {turma.professor} - {turma.semestre}")
            for matricula in turma.alunos:
                aluno = ger_alunos.buscar_por_matricula(matricula)
                notas = turma.notas.get(matricula, {})
                freq = turma.presencas.get(matricula, 0)
                media = calcular_media(turma.avaliacao, notas)
                status = status_final(media, freq)
                print(f"{aluno.nome} - Média: {media:.1f} - Freq: {freq:.1f}% - {status}")

        elif op == "5":
            break
        else:
            print("Opção inválida.")

def calcular_media(tipo, notas):
    if not notas:
        return 0
    p1 = notas.get("P1", 0)
    p2 = notas.get("P2", 0)
    p3 = notas.get("P3", 0)
    l = notas.get("L", 0)
    s = notas.get("S", 0)
    if tipo == "ponderada":
        return (p1 + 2*p2 + 3*p3 + l + s) / 8
    else:
        return (p1 + p2 + p3 + l + s) / 5

def status_final(media, frequencia):
    if frequencia < 75:
        return "Reprovado por falta"
    elif media >= 5:
        return "Aprovado"
    else:
        return "Reprovado por nota"
