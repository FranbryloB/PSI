# Importações necessárias
from flask_login import UserMixin  # Classe base que fornece implementações padrão para o modelo de usuário
from database import get_connection  # Nossa função de conexão com o banco de dados
from werkzeug.security import generate_password_hash, check_password_hash  # Funções para hash de senha

# Modelo de Usuário
class User(UserMixin):  # UserMixin fornece implementações padrão necessárias para o Flask-Login
    def __init__(self, id=None, nome=None, email=None, password=None):
        """
        Inicializa um novo usuário
        :param id: ID do usuário no banco de dados
        :param nome: Nome do usuário
        :param email: Email do usuário
        :param password: Senha já hashada do usuário
        """
        self.id = id
        self.nome = nome
        self.email = email
        self.password_hash = password

    def set_password(self, password):
        """
        Define a senha do usuário de forma segura
        Converte a senha em texto puro para uma hash segura
        :param password: Senha em texto puro
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica se a senha está correta
        :param password: Senha em texto puro para verificar
        :return: True se a senha está correta, False caso contrário
        """
        return check_password_hash(self.password_hash, password)
        
    def save(self):
        """
        Salva o usuário no banco de dados
        :return: True se o salvamento foi bem sucedido
        """
        # Conecta ao banco de dados
        conn = get_connection()
        cursor = conn.cursor()
        
        # Insere o novo usuário
        cursor.execute(
            "INSERT INTO users(email, nome, password) VALUES (?, ?, ?)", 
            (self.email, self.nome, self.password_hash)
        )
        
        # Confirma e fecha a conexão
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def get_by_email(email):
        """
        Busca um usuário pelo email
        :param email: Email do usuário a ser buscado
        :return: Objeto User se encontrado, None caso contrário
        """
        # Conecta ao banco de dados
        conn = get_connection()
        cursor = conn.cursor()
        
        # Busca o usuário
        user = cursor.execute(
            "SELECT id, email, nome, password FROM users WHERE email = ?", 
            (email,)
        ).fetchone()
        conn.close()
        
        # Se encontrou o usuário, retorna um objeto User
        if user:
            return User(id=user[0], email=user[1], nome=user[2], password=user[3])
        return None

    def get_id(self):
        """
        Retorna o ID do usuário como string
        Método requerido pelo Flask-Login
        :return: ID do usuário como string
        """
        return str(self.id)