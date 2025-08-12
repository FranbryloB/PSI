flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def obter_conexao():
    conn = sqlite3.connect('jogo.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personagens/novo', methods=['GET', 'POST'])
def novo_personagem():
    if request.method == 'POST':
        nome = request.form.get('nome', '')
        jogo = request.form.get('jogo', '')
        habilidade = request.form.get('habilidade', '')

        if nome and jogo and habilidade:
            conn = obter_conexao()
            SQL = "INSERT INTO personagens (nome, jogo_origem, habilidade_principal) VALUES (?, ?, ?)"
            conn.execute(SQL, (nome, jogo, habilidade))
            conn.commit()
            conn.close()

        return redirect('/personagens')

    return render_template('novo_personagem.html')

@app.route('/personagens')


def listar_personagens():
    conn = obter_conexao()
    SQL = "SELECT * FROM personagens"
    lista = conn.execute(SQL).fetchall()
    conn.close()
    return render_template('listar_personagens.html',lista=lista)
    