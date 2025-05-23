from package.disciplinas.disciplina import Disciplina
from package.utils.serializer import salvar_json, carregar_json


class GerenciadorDisciplinas:

    def __init__(self):
        self._disciplinas = []

    def adicionar_disciplina(self, disciplina):
        self._disciplinas.append(disciplina)
        print("Disciplina adicionada.")

    def buscar_disciplina(self, codigo):
        for d, disc in enumerate(self._disciplinas):
            if disc.codigo == codigo:
                disciplina = self._disciplinas[d]
                print(f"A disciplina {disciplina.nome} foi encontrada")
                return disciplina
        return None

    def salvar(self, caminho):
        dados = [d.to_dict() for d in self._disciplinas]
        salvar_json(caminho, dados)

    def carregar(self, caminho):
        self._disciplinas = []
        for d in carregar_json(caminho):
            self._disciplinas.append(Disciplina.from_dict(d))
