
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chavesecreta'
db = SQLAlchemy(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
	mensagem = None
	if request.method == 'POST':
		email = request.form.get('email')
		senha = request.form.get('senha')
		usuario = User.query.filter_by(email=email, senha=senha).first()
		if usuario:
			session['usuario_id'] = usuario.id
			session['usuario_nome'] = usuario.nome
			return redirect(url_for('index'))
		else:
			mensagem = 'E-mail ou senha inválidos!'
	return render_template('login.html', mensagem=mensagem)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	senha = db.Column(db.String(100), nullable=False)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=True)

@app.route('/produtos')
def listar_produtos():
    if 'usuario_id' not in session:  
        return redirect(url_for('login'))

    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@app.route('/produtos/novo', methods=['GET', 'POST'])
def novo_produto():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    mensagem = None
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        descricao = request.form.get('descricao')

        try:
            preco = float(preco)
            novo = Produto(nome=nome, preco=preco, descricao=descricao)
            db.session.add(novo)
            db.session.commit()
            return redirect(url_for('listar_produtos'))
        except ValueError:
            mensagem = "Preço inválido! Use apenas números."

    return render_template('cadastro_produto.html', mensagem=mensagem)

@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        produto.nome = request.form.get('nome')
        produto.preco = float(request.form.get('preco'))
        produto.descricao = request.form.get('descricao')
        db.session.commit()
        return redirect(url_for('listar_produtos'))

    return render_template('editar_produto.html', produto=produto)

@app.route('/produtos/excluir/<int:id>')
def excluir_produto(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('listar_produtos'))

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    mensagem = None
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if User.query.filter_by(email=email).first():
            mensagem = 'E-mail já cadastrado!'
            return render_template('cadastro.html', mensagem=mensagem)
        else:
            novo_usuario = User(nome=nome, email=email, senha=senha)
            db.session.add(novo_usuario)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('cadastro.html', mensagem=mensagem)

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run(debug=True)