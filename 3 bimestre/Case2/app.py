
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from models.user import User
from controllers import users, products
from database import get_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    user = cursor.execute('SELECT id, email, nome, password FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(id=user[0], email=user[1], nome=user[2], password=user[3])
    return None

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

app.register_blueprint(users.bp)
app.register_blueprint(products.bp)

@app.route('/')
def home():
    return render_template('home.html')
