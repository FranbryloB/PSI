import sqlite3
import os

# Caminho para o diretório database
db_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database')
# Caminho para o arquivo SQL
sql_file = os.path.join(db_dir, 'database.sql')
# Caminho para o banco de dados
db_file = os.path.join(db_dir, 'database.db')

def init_db():
    # Remover o banco de dados existente se houver
    if os.path.exists(db_file):
        os.remove(db_file)
    
    # Criar novo banco de dados e executar o script SQL
    with open(sql_file, 'r') as f:
        sql_script = f.read()
        
    conn = sqlite3.connect(db_file)
    conn.executescript(sql_script)
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    init_db()