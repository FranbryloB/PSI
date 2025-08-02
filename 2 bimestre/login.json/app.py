from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RANCA TAMPA E MANDA BOI'

login_manager = LoginManager(app)
login_manager.login_view = 'login'


ARQ_PRODUTOS = 'produtos.json'
ARQ_COMPRAS = 'compras.json'
ARQ_CARRINHOS = 'carrinhos.json'  


def carregar_json(caminho, padrao):
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(padrao, f, indent=4)
        return padrao

def salvar_json(caminho, dados):
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4)


produtos_ = carregar_json(ARQ_PRODUTOS, {
    'gibao': 500,
    'bota': 1500,
    'espora': 200,
    'cavalo': 15000,
    'bezerro': 3000,
    'chapeu': 500,
    'oculos': 1500,
    'capacete': 300
})

compras = carregar_json(ARQ_COMPRAS, {})
carrinhos = carregar_json(ARQ_CARRINHOS, {})

def salvar_carrinhos():
    salvar_json(ARQ_CARRINHOS, carrinhos)


usuarios = {}


class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return User(user_id)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        if nome in usuarios and usuarios[nome] == senha:
            user = User(nome)
            login_user(user)
            carrinhos.setdefault(nome, [])
            salvar_carrinhos()  
            return redirect(url_for('produtos'))
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        if nome not in usuarios:
            usuarios[nome] = senha
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/produtos')
@login_required
def produtos():
    return render_template('produtos.html', produtos=produtos_)

@app.route('/adicionar', methods=['POST'])
@login_required
def adicionar():
    prod = request.form['prod']
    if prod in produtos_:
        carrinhos.setdefault(current_user.id, []).append(prod)
        salvar_carrinhos()  
    return redirect(url_for('carrinho'))

@app.route('/remover', methods=['POST'])
@login_required
def remover():
    prod = request.form['prod']
    carrinho = carrinhos.get(current_user.id, [])
    if prod in carrinho:
        carrinho.remove(prod)
        salvar_carrinhos() 
    return redirect(url_for('carrinho'))

@app.route('/carrinho')
@login_required
def carrinho():
    carrinho_ = carrinhos.get(current_user.id, [])
    soma = sum(produtos_[p] for p in carrinho_)
    return render_template('carrinho.html', carrinho=carrinho_, valor=soma, produtos=produtos_)

@app.route('/fechar_compra', methods=['POST'])
@login_required
def fechar_compra():
    usuario = current_user.id
    carrinho_ = carrinhos.get(usuario, [])
    if not carrinho_:
        return redirect(url_for('carrinho'))

    
    compras.setdefault(usuario, []).append({
        'itens': carrinho_,
        'total': sum(produtos_[p] for p in carrinho_)
    })

    salvar_json(ARQ_COMPRAS, compras)

    
    carrinhos[usuario] = []
    salvar_carrinhos()

    return redirect(url_for('carrinho'))

if __name__ == '__main__':
    app.run(debug=True)
