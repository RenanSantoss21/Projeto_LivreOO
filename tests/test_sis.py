import unittest
import os
import shutil
from unittest.mock import patch, mock_open

from package.alunos.aluno import Aluno, AlunoEspecial
from package.alunos.cadastro import GerenciadorAlunos
from package.disciplinas.disciplina import Disciplina
from package.disciplinas.turma import Turma
from package.disciplinas.cadastro import GerenciadorDisciplinas
from package.avaliacao.menu_av import GerenciadorAvaliacao
from package.usuarios.cadastro_usuario import Usuario, GerenciadorUsuarios
from package.utils.serializer import salvar_json, carregar_json


class TestSistemaAcademico(unittest.TestCase):

    def setUp(self):

        self.test_dir = "test_dados"
        os.makedirs(self.test_dir, exist_ok=True)

        self.alunos_path = os.path.join(self.test_dir, "alunos.json")
        self.disciplinas_path = os.path.join(self.test_dir, "disciplinas.json")
        self.usuarios_path = os.path.join(self.test_dir, "usuarios.json")

        self.ger_disciplinas = GerenciadorDisciplinas()
        self.ger_alunos = GerenciadorAlunos(ger_disciplinas=self.ger_disciplinas)
        self.ger_avaliacao = GerenciadorAvaliacao(self.ger_alunos, self.ger_disciplinas)
        self.ger_usuarios = GerenciadorUsuarios(self.usuarios_path)

        for path in [self.alunos_path, self.disciplinas_path, self.usuarios_path]:
            if os.path.exists(path):
                os.remove(path)

    def tearDown(self):

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    # --- Testes para package/utils/serializer.py ---
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_salvar_json(self, mock_json_dump, mock_file_open):
        dados = [{"a": 1}, {"b": 2}]
        salvar_json("teste.json", dados)
        mock_file_open.assert_called_once_with("teste.json", "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(dados, mock_file_open(), indent=4, ensure_ascii=False)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"a": 1}]')
    @patch('json.load', return_value=[{"a": 1}])
    @patch('os.path.exists', return_value=True)
    def test_carregar_json_existente(self, mock_exists, mock_json_load, mock_file_open):
        dados = carregar_json("teste.json")
        mock_exists.assert_called_once_with("teste.json")
        mock_file_open.assert_called_once_with("teste.json", "r", encoding="utf-8")
        mock_json_load.assert_called_once_with(mock_file_open())
        self.assertEqual(dados, [{"a": 1}])

    @patch('os.path.exists', return_value=False)
    def test_carregar_json_nao_existente(self, mock_exists):
        dados = carregar_json("nao_existe.json")
        mock_exists.assert_called_once_with("nao_existe.json")
        self.assertEqual(dados, [])

    # --- Testes para Aluno e AlunoEspecial ---
    def test_aluno_criacao(self):
        aluno = Aluno("Joao", "123", "Comp")
        self.assertEqual(aluno.nome, "Joao")
        self.assertEqual(aluno.matricula, "123")
        self.assertEqual(aluno.curso, "Comp")
        self.assertEqual(aluno.disciplinas, [])
        self.assertEqual(aluno.historico, [])
        self.assertEqual(aluno.to_dict()["tipo"], "normal")

    def test_aluno_especial_criacao(self):
        aluno_esp = AlunoEspecial("Maria", "456", "Eng")
        self.assertEqual(aluno_esp.nome, "Maria")
        self.assertEqual(aluno_esp.matricula, "456")
        self.assertEqual(aluno_esp.to_dict()["tipo"], "especial")
    
    def test_aluno_to_dict_from_dict(self):
        aluno_original = Aluno("Carlos", "789", "Mat")
        aluno_original.disciplinas.append("POO101")
        aluno_original.historico.append("CAL001")
        
        aluno_dict = aluno_original.to_dict()
        aluno_reconstituido = Aluno.from_dict(aluno_dict)

        self.assertEqual(aluno_original.nome, aluno_reconstituido.nome)
        self.assertEqual(aluno_original.matricula, aluno_reconstituido.matricula)
        self.assertEqual(aluno_original.disciplinas, aluno_reconstituido.disciplinas)
        self.assertEqual(aluno_original.historico, aluno_reconstituido.historico)

    # --- Testes para GerenciadorAlunos ---
    def test_gerenciador_alunos_cadastrar_listar(self):
        aluno1 = Aluno("Joao", "111", "Comp")
        aluno2 = Aluno("Maria", "222", "Eng")
        
        self.ger_alunos.cadastrar(aluno1)
        self.ger_alunos.cadastrar(aluno2)
        
        self.assertEqual(len(self.ger_alunos._alunos), 2)
        self.assertEqual(self.ger_alunos.buscar_por_matricula("111").nome, "Joao")

    def test_gerenciador_alunos_matricula_duplicada(self):
        aluno1 = Aluno("Joao", "111", "Comp")
        self.ger_alunos.cadastrar(aluno1)
        
        aluno_duplicado = Aluno("Joao D", "111", "Comp")
        self.assertFalse(self.ger_alunos.cadastrar(aluno_duplicado)) # retorna False

    def test_gerenciador_alunos_remover(self):
        aluno1 = Aluno("Joao", "111", "Comp")
        self.ger_alunos.cadastrar(aluno1)
        
        self.assertTrue(self.ger_alunos.remover("111"))
        self.assertIsNone(self.ger_alunos.buscar_por_matricula("111"))
        self.assertEqual(len(self.ger_alunos._alunos), 0)

        self.assertFalse(self.ger_alunos.remover("999")) # matrícula inexistente

    # --- Testes de Matrícula e Pré-requisitos ---
    def test_matricular_aluno_normal_sem_prereq(self):
        aluno = Aluno("Teste", "MAT1", "Curso")
        self.ger_alunos.cadastrar(aluno)
        
        disciplina = Disciplina("Disc A", "D001", 60)
        self.ger_disciplinas.adicionar_disciplina(disciplina)
        turma = Turma("Prof X", "2025.1", "simples", True, "8h", "S1", 10, "D001")
        disciplina.turmas.append(turma)

        self.assertTrue(self.ger_alunos.matricular(aluno, turma))
        self.assertIn("MAT1", turma.alunos)
        self.assertIn("D001", aluno.disciplinas)

    def test_matricular_aluno_com_prereq_satisfeito(self):
        aluno = Aluno("Teste P", "MAT2", "Curso")
        aluno.historico.append("PREREQ01")
        self.ger_alunos.cadastrar(aluno)

        disciplina = Disciplina("Disc B", "D002", 60, ["PREREQ01"])
        self.ger_disciplinas.adicionar_disciplina(disciplina)
        turma = Turma("Prof Y", "2025.1", "simples", True, "9h", "S2", 10, "D002")
        disciplina.turmas.append(turma)

        self.assertTrue(self.ger_alunos.matricular(aluno, turma))

    def test_matricular_aluno_com_prereq_nao_satisfeito(self):
        aluno = Aluno("Teste P2", "MAT3", "Curso")
        self.ger_alunos.cadastrar(aluno)

        disciplina = Disciplina("Disc C", "D003", 60, ["PREREQ02"])
        self.ger_disciplinas.adicionar_disciplina(disciplina)
        turma = Turma("Prof Z", "2025.1", "simples", True, "10h", "S3", 10, "D003")
        disciplina.turmas.append(turma)

        self.assertFalse(self.ger_alunos.matricular(aluno, turma))
        self.assertNotIn("MAT3", turma.alunos)
        self.assertNotIn("D003", aluno.disciplinas)

    def test_matricular_aluno_especial_limite_semestre(self):
        aluno_esp = AlunoEspecial("Esp", "MAT4", "Curso")
        self.ger_alunos.cadastrar(aluno_esp)

        # 1ª disciplina no 2025.1
        disc1 = Disciplina("Disc E1", "D004", 60)
        self.ger_disciplinas.adicionar_disciplina(disc1)
        turma1 = Turma("Prof A", "2025.1", "simples", True, "11h", "S4", 1, "D004")
        disc1.turmas.append(turma1)
        self.assertTrue(self.ger_alunos.matricular(aluno_esp, turma1))
        
        # 2ª disciplina no 2025.1
        disc2 = Disciplina("Disc E2", "D005", 60)
        self.ger_disciplinas.adicionar_disciplina(disc2)
        turma2 = Turma("Prof B", "2025.1", "simples", True, "12h", "S5", 1, "D005")
        disc2.turmas.append(turma2)
        self.assertTrue(self.ger_alunos.matricular(aluno_esp, turma2))

        # 3ª disciplina no 2025.1 (deve falhar)
        disc3 = Disciplina("Disc E3", "D006", 60)
        self.ger_disciplinas.adicionar_disciplina(disc3)
        turma3 = Turma("Prof C", "2025.1", "simples", True, "13h", "S6", 1, "D006")
        disc3.turmas.append(turma3)
        self.assertFalse(self.ger_alunos.matricular(aluno_esp, turma3))

        # Uma disciplina em outro semestre (deve funcionar)
        disc4 = Disciplina("Disc E4", "D007", 60)
        self.ger_disciplinas.adicionar_disciplina(disc4)
        turma4 = Turma("Prof D", "2025.2", "simples", True, "14h", "S7", 1, "D007")
        disc4.turmas.append(turma4)
        self.assertTrue(self.ger_alunos.matricular(aluno_esp, turma4)) # Deve matricular no semestre diferente

    def test_matricular_turma_cheia(self):
        aluno = Aluno("Teste", "MAT5", "Curso")
        self.ger_alunos.cadastrar(aluno)
        
        disciplina = Disciplina("Disc F", "D008", 60)
        self.ger_disciplinas.adicionar_disciplina(disciplina)
        turma = Turma("Prof F", "2025.1", "simples", True, "15h", "S8", 0, "D008") # Capacidade 0
        disciplina.turmas.append(turma)

        self.assertFalse(self.ger_alunos.matricular(aluno, turma))

    def test_matricular_aluno_ja_matriculado(self):
        aluno = Aluno("Teste", "MAT6", "Curso")
        self.ger_alunos.cadastrar(aluno)
        
        disciplina = Disciplina("Disc G", "D009", 60)
        self.ger_disciplinas.adicionar_disciplina(disciplina)
        turma = Turma("Prof G", "2025.1", "simples", True, "16h", "S9", 10, "D009")
        disciplina.turmas.append(turma)

        self.ger_alunos.matricular(aluno, turma)
        self.assertFalse(self.ger_alunos.matricular(aluno, turma)) # matrícula na mesma turma

    # --- Testes para GerenciadorDisciplinas ---
    def test_gerenciador_disciplinas_adicionar_buscar(self):
        disc = Disciplina("Prog OO", "POO101", 60)
        self.assertTrue(self.ger_disciplinas.adicionar_disciplina(disc))
        self.assertEqual(len(self.ger_disciplinas._disciplinas), 1)
        self.assertEqual(self.ger_disciplinas.buscar_disciplina("POO101").nome, "Prog OO")

        self.assertFalse(self.ger_disciplinas.adicionar_disciplina(disc))

    def test_gerenciador_disciplinas_remover(self):
        disc = Disciplina("Prog OO", "POO101", 60)
        self.ger_disciplinas.adicionar_disciplina(disc)
        
        self.assertTrue(self.ger_disciplinas.remover_disciplina("POO101"))
        self.assertIsNone(self.ger_disciplinas.buscar_disciplina("POO101"))
        self.assertEqual(len(self.ger_disciplinas._disciplinas), 0)

        self.assertFalse(self.ger_disciplinas.remover_disciplina("NAO_EXISTE"))

    def test_gerenciador_disciplinas_remover_com_turmas(self):
        disc = Disciplina("BD", "BD202", 60)
        self.ger_disciplinas.adicionar_disciplina(disc)
        turma = Turma("Prof B", "2025.1", "simples", True, "10h", "S10", 10, "BD202")
        disc.turmas.append(turma)

        self.assertFalse(self.ger_disciplinas.remover_disciplina("BD202")) # Deve falhar

    def test_gerenciador_disciplinas_editar(self):
        disc = Disciplina("Prog OO", "POO101", 60)
        self.ger_disciplinas.adicionar_disciplina(disc)
        
        novos_dados = {"nome": "Programacao Orientada a Objetos II", "carga_horaria": 90, "pre_requisitos": ["CAL001"]}
        self.assertTrue(self.ger_disciplinas.editar_disciplina("POO101", novos_dados))
        
        disc_editada = self.ger_disciplinas.buscar_disciplina("POO101")
        self.assertEqual(disc_editada.nome, "Programacao Orientada a Objetos II")
        self.assertEqual(disc_editada.carga_horaria, 90)
        self.assertEqual(disc_editada.pre_requisitos, ["CAL001"])

    def test_gerenciador_disciplinas_criar_turma(self):
        disc = Disciplina("Teste Disc", "TD001", 40)
        self.ger_disciplinas.adicionar_disciplina(disc)
        
        turma = Turma("Prof T", "2025.1", "simples", True, "10h", "S11", 20, "TD001")
        disc.turmas.append(turma)
        
        self.assertEqual(len(disc.turmas), 1)
        self.assertEqual(disc.turmas[0].professor, "Prof T")

    def test_gerenciador_disciplinas_remover_turma(self):
        disc = Disciplina("Teste Rem Turma", "TRT01", 40)
        self.ger_disciplinas.adicionar_disciplina(disc)
        turma1 = Turma("Prof X", "2025.1", "simples", True, "9h", "S12", 10, "TRT01")
        turma2 = Turma("Prof Y", "2025.1", "simples", True, "10h", "S13", 10, "TRT01")
        disc.turmas.append(turma1)
        disc.turmas.append(turma2)
        
        self.assertTrue(self.ger_disciplinas.remover_turma("TRT01", 0)) # Remove a primeira turma (indice 0)
        self.assertEqual(len(disc.turmas), 1)
        self.assertEqual(disc.turmas[0].professor, "Prof Y") # A segunda turma agora é a primeira

        self.assertFalse(self.ger_disciplinas.remover_turma("TRT01", 5)) # Índice inválido

    def test_gerenciador_disciplinas_remover_turma_com_alunos(self):
        disc = Disciplina("Teste Rem Turma Aluno", "TRTA1", 40)
        self.ger_disciplinas.adicionar_disciplina(disc)
        turma = Turma("Prof A", "2025.1", "simples", True, "9h", "S14", 10, "TRTA1")
        turma.alunos.append("ALUNO1")
        disc.turmas.append(turma)

        self.assertFalse(self.ger_disciplinas.remover_turma("TRTA1", 0)) # Deve falhar

    # --- Testes para GerenciadorAvaliacao ---
    def test_gerenciador_avaliacao_calcular_media_simples(self):
        notas = {"P1": 7, "P2": 8, "P3": 6, "L": 9, "S": 7}
        media = self.ger_avaliacao.calcular_media("simples", notas)
        self.assertAlmostEqual(media, (7+8+6+9+7)/5)

    def test_gerenciador_avaliacao_calcular_media_ponderada(self):
        notas = {"P1": 7, "P2": 8, "P3": 6, "L": 9, "S": 7}
        media = self.ger_avaliacao.calcular_media("ponderada", notas)
        self.assertAlmostEqual(media, (7 + 2*8 + 3*6 + 9 + 7)/8)

    def test_gerenciador_avaliacao_status_final(self):
        self.assertEqual(self.ger_avaliacao.status_final(7, 80), "Aprovado")
        self.assertEqual(self.ger_avaliacao.status_final(4, 80), "Reprovado por nota")
        self.assertEqual(self.ger_avaliacao.status_final(7, 70), "Reprovado por falta")
        self.assertEqual(self.ger_avaliacao.status_final(4, 70), "Reprovado por falta") # Frequencia tem precedencia

     # --- Testes para GerenciadorUsuarios E classe Usuario ---
    def test_usuario_criacao(self):
        user = Usuario("testuser", "hashed_password", "admin")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password_hash, "hashed_password")
        self.assertEqual(user.role, "admin")

    def test_gerenciador_usuarios_cadastro_autenticacao(self):
        self.assertTrue(self.ger_usuarios.cadastrar_usuario("testuser", "testpass"))
        
        user_autenticado = self.ger_usuarios.autenticar_usuario("testuser", "testpass")
        self.assertIsNotNone(user_autenticado)
        self.assertEqual(user_autenticado.username, "testuser")

        self.assertIsNone(self.ger_usuarios.autenticar_usuario("testuser", "wrongpass"))

        self.assertIsNone(self.ger_usuarios.autenticar_usuario("nonexistent", "anypass"))

        self.assertFalse(self.ger_usuarios.cadastrar_usuario("testuser", "anotherpass"))

    def test_gerenciador_usuarios_carregar_salvar(self):
        self.ger_usuarios.cadastrar_usuario("user1", "pass1")
        self.ger_usuarios.cadastrar_usuario("user2", "pass2", "admin")
        self.ger_usuarios.salvar_usuarios()

        novo_ger_usuarios = GerenciadorUsuarios(self.usuarios_path)

        self.assertEqual(len(novo_ger_usuarios._usuarios), 2)

        self.assertIsNotNone(novo_ger_usuarios.autenticar_usuario("user1", "pass1"))
        user2_loaded = novo_ger_usuarios.autenticar_usuario("user2", "pass2")
        self.assertIsNotNone(user2_loaded)
        self.assertEqual(user2_loaded.role, "admin")

    def test_gerenciador_usuarios_hash_password(self):
        password = "mysecretpassword"
        hashed_pass = self.ger_usuarios._hash_password(password)
        self.assertIsInstance(hashed_pass, str)
        self.assertEqual(len(hashed_pass), 64)

        self.assertEqual(hashed_pass, self.ger_usuarios._hash_password(password))

        self.assertNotEqual(hashed_pass, self.ger_usuarios._hash_password("anotherpassword"))


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)