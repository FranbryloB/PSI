import sqlite3
conexao = sqlite3.connect("jogo.db")
with open('schema.sql') as f:
    conexao.executescript(f.read())
conexao.close()