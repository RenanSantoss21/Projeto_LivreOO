import json
import os

def garantir_arquivo_json(caminho, dado_padrao=None):
    if not os.path.exists(os.path.dirname(caminho)):
        os.makedirs(os.path.dirname(caminho))

    if not os.path.exists(caminho):
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dado_padrao if dado_padrao is not None else [], f, indent=4)

def salvar_json(dado, caminho):

    garantir_arquivo_json(caminho, dado_padrao=dado)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dado, f, indent=4, ensure_ascii=False)

def carregar_json(caminho):

    garantir_arquivo_json(caminho, dado_padrao=[])
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)