import hashlib
from package.utils.serializer import Serializable, carregar_json, salvar_json


class Usuario(Serializable):
    def __init__(self, username, password_hash, role= "default"):
        self.username = username
        self.password_hash = password_hash
        self.role = role
    
    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["password_hash"], data.get("role", "default"))
    
class GerenciadorUsuarios:
    def __init__(self, caminho):
        self.caminho = caminho
        self._usuarios = []
        self.carregar_usuarios()

    def carregar_usuarios(self):
        dados_json = carregar_json(self.caminho)
        self._usuarios = [Usuario.from_dict(d) for d in dados_json]

    def salvar_usuarios(self):
        dados_json = [u.to_dict() for u in self._usuarios]
        salvar_json(self.caminho, dados_json)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def cadastrar_usuario(self, username, password, role="default"):
        if any(u.username == username for u in self._usuarios):
            print(f"Usuário '{username}' já existe.")
            return False
        
        password_hash = self._hash_password(password)
        novo_usuario = Usuario(username, password_hash, role)
        self._usuarios.append(novo_usuario)
        self.salvar_usuarios()
        print(f"Usuário '{username}' cadastrado com sucesso.")
        return True

    def autenticar_usuario(self, username, password):
        for usuario in self._usuarios:
            if usuario.username == username:
                if usuario.password_hash == self._hash_password(password):
                    print(f"Autenticação bem-sucedida para o usuário '{username}'.")
                    return usuario # Retorna o objeto usuário autenticado
                else:
                    print("Senha incorreta.")
                    return None
        print("Usuário não encontrado.")
        return None

    def listar_usuarios(self):
        if not self._usuarios:
            print("Nenhum usuário cadastrado.")
            return
        print("\n--- Lista de Usuários ---")
        for user in self._usuarios:
            print(f"Username: {user.username}, Role: {user.role}")