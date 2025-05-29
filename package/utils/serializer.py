import json
import os


class Serializable:

    def get_serializable_attributes(self):
        attrs = {}
        for key in dir(self):
            if not key.startswith('_') and not callable(getattr(self, key)):
                value = getattr(self, key)
                if hasattr(value, 'to_dict') and callable(value.to_dict):
                    attrs[key] = value.to_dict()
                elif isinstance(value, list) and all(hasattr(item, 'to_dict') for item in value):
                    attrs[key] = [item.to_dict() for item in value]
                else:
                    attrs[key] = value
        return attrs

    @classmethod
    def _validate_dict_data(cls, data, required_keys):
        """Valida se o dicionário possui todas as chaves necessárias."""
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Chave '{key}' ausente nos dados de serialização para {cls.__name__}.")
        return True

def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_json(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
