from sqlalchemy import create_engine, text
# pip install sqlalchemy

SQLITE = "sqlite:///database.db"
engine = create_engine(SQLITE)

# conexao = engine.connect()
with engine.connect() as conexao:
    SQL = text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)
    conexao.execute(SQL)
    conexao.commit()


# pip install mysqlclient
MYSQL = 'mysql://root:@localhost/flask'
engine = create_engine(MYSQL)
with engine.connect() as conn:
    SQL = text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL
        )
    """)
    conn.execute(SQL)
    conn.commit()

# inserção de dados
conexao = engine.connect()
SQL = "INSERT INTO users(nome) values (:nome)"
nome = 'romerito'
conexao.execute(text(SQL), {'nome': nome})
conexao.commit()
conexao.close()