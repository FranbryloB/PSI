# Importações necessárias
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required  # Para proteger rotas que exigem login
from models.product import Product  # Nosso modelo de produto

# Cria um Blueprint para as rotas de produtos
# Blueprint permite organizar rotas relacionadas em um grupo
bp = Blueprint('products', __name__, url_prefix='/products')

# Rota para listar todos os produtos
@bp.route('/')
def index():
    """
    Lista todos os produtos cadastrados
    Esta rota é pública - não requer login
    """
    # Busca todos os produtos do banco de dados
    products = Product.get_all()
    
    # Renderiza o template passando a lista de produtos
    return render_template('products/index.html', products=products)

# Rota para criar um novo produto
@bp.route('/new', methods=['GET', 'POST'])
@login_required  # Decorator que exige que o usuário esteja logado
def create():
    """
    Manipula a criação de novos produtos
    GET: Exibe o formulário de cadastro
    POST: Processa o formulário enviado
    Requer que o usuário esteja logado (@login_required)
    """
    # Se for uma requisição POST (envio do formulário)
    if request.method == 'POST':
        # Cria um novo produto com os dados do formulário
        product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),  # Converte para float
            stock=int(request.form['stock'])     # Converte para inteiro
        )
        # Salva o produto no banco de dados
        product.save()
        
        # Redireciona para a lista de produtos
        return redirect(url_for('products.index'))
    
    # Se for GET, exibe o template de cadastro
    return render_template('products/register.html')