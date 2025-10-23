# Importações necessárias
from flask import render_template, Blueprint, url_for, request, flash, redirect
from flask_login import login_user, logout_user, login_required  # Funções para gerenciar autenticação
from models.user import User  # Nosso modelo de usuário

# Cria um Blueprint para as rotas de usuário
# Blueprint permite organizar rotas relacionadas em um grupo
bp = Blueprint('users', __name__, url_prefix='/users')

# Rota para registro de novos usuários
@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Manipula o registro de novos usuários
    GET: Exibe o formulário de registro
    POST: Processa o formulário enviado
    """
    # Se for uma requisição POST (envio do formulário)
    if request.method == 'POST':
        # Obtém os dados do formulário
        email = request.form['email']
        nome = request.form['nome']
        password = request.form['password']

        # Validação básica
        if not email or not password:
            flash('Email e senha são obrigatórios')  # Mensagem de erro
        else:
            # Cria e salva o novo usuário
            user = User(nome=nome, email=email)
            user.set_password(password)  # Define a senha de forma segura
            user.save()
            return redirect(url_for('users.login'))  # Redireciona para o login
    
    # Se for GET, exibe o template de registro
    return render_template('users/register.html')

# Rota para login de usuários
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Manipula o login de usuários
    GET: Exibe o formulário de login
    POST: Processa a tentativa de login
    """
    # Se for uma requisição POST (envio do formulário)
    if request.method == 'POST':
        # Obtém os dados do formulário
        email = request.form['email']
        password = request.form['password']
        
        # Busca o usuário pelo email
        user = User.get_by_email(email)
        
        # Verifica se o usuário existe e a senha está correta
        if user and user.check_password(password):
            login_user(user)  # Faz o login do usuário
            return redirect(url_for('products.index'))  # Redireciona para produtos
        flash('Email ou senha inválidos')  # Mensagem de erro
    
    # Se for GET, exibe o template de login
    return render_template('users/login.html')

# Rota para logout
@bp.route('/logout')
@login_required  # Decorator que exige que o usuário esteja logado
def logout():
    """
    Realiza o logout do usuário atual
    Requer que o usuário esteja logado (@login_required)
    """
    logout_user()  # Faz o logout do usuário
    return redirect(url_for('home'))  # Redireciona para a página inicial