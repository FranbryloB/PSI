# Importa a função de conexão com o banco de dados
from database import get_connection

# Modelo de Produto
class Product:
    def __init__(self, id=None, name=None, description=None, price=None, stock=None):
        """
        Inicializa um novo produto
        :param id: ID do produto no banco de dados
        :param name: Nome do produto
        :param description: Descrição do produto
        :param price: Preço do produto
        :param stock: Quantidade em estoque
        """
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    def save(self):
        """
        Salva o produto no banco de dados
        :return: True se o salvamento foi bem sucedido
        """
        # Conecta ao banco de dados
        conn = get_connection()
        cursor = conn.cursor()
        
        # Insere o novo produto
        cursor.execute(
            "INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)",
            (self.name, self.description, self.price, self.stock)
        )
        
        # Confirma e fecha a conexão
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_all():
        """
        Retorna todos os produtos cadastrados
        :return: Lista de tuplas contendo os dados dos produtos
        """
        # Conecta ao banco de dados
        conn = get_connection()
        cursor = conn.cursor()
        
        # Busca todos os produtos
        products = cursor.execute("SELECT * FROM products").fetchall()
        
        # Fecha a conexão e retorna os produtos
        conn.close()
        return products