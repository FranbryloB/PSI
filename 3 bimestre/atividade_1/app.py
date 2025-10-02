from flask import render_template_string, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

#times (N:N)
@app.route('/associar', methods=['GET', 'POST'])
def associar_usuario_time():
    usuarios = Usuario.query.all()
    times = Time.query.all()
    if request.method == 'POST':
        usuario_id = int(request.form['usuario_id'])
        times_ids = request.form.getlist('times')
        usuario = Usuario.query.get(usuario_id)
        usuario.times = [Time.query.get(int(tid)) for tid in times_ids]
        db.session.commit()
        return redirect(url_for('associar'))
    return render_template('associar.html', usuarios=usuarios, times=times)

@app.route('/usuarios', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        usuario = Usuario(nome=nome)
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('cadastrar_usuario'))
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/times', methods=['GET', 'POST'])
def cadastrar_time():
    if request.method == 'POST':
        nome = request.form['nome']
        time = Time(nome=nome)
        db.session.add(time)
        db.session.commit()
        return redirect(url_for('cadastrar_time'))
    times = Time.query.all()
    return render_template('times.html', times=times)

@app.route('/vinculados', methods=['GET', 'POST'])
def cadastrar_vinculado():
    times = Time.query.all()
    if request.method == 'POST':
        nome = request.form['nome']
        time_id = request.form['time_id']
        vinculado = Vinculado(nome=nome, time_id=time_id)
        db.session.add(vinculado)
        db.session.commit()
        return redirect(url_for('cadastrar_vinculado'))
    vinculados = Vinculado.query.all()
    return render_template('vinculados.html', times=times, vinculados=vinculados)

usuarios_times = db.Table(
    'usuarios_times',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('time_id', db.Integer, db.ForeignKey('time.id'), primary_key=True)
)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    times = db.relationship('Time', secondary=usuarios_times, back_populates='usuarios')

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) 
    usuarios = db.relationship('Usuario', secondary=usuarios_times, back_populates='times')
    vinculados = db.relationship('Vinculado', backref='time', lazy=True)

class Vinculado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey('time.id'), nullable=False)

with app.app_context():
    db.create_all()
    app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)