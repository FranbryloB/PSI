from flask import Flask, render_template, request, \
    make_response, redirect, url_for, session

app = Flask(__name__) #cria a aplicação flask

app.config['SECRET_KEY'] = 'segredodificil' #uma chave necessária para session, sem isso o flask não consegue guardar dados da sessão.

@app.route('/')
def index():
    return render_template('index.html')
    #Quando o usuário acessa /, carrega o arquivo index.html.

@app.route('/cadastro', methods=['GET', 'POST']) #GET mostrar formulário #POST enviar dados.
def register():
    if request.method == 'GET': 
        return render_template('cadastro.html')
    else:
        # 'nome' é o atributo 'name' do input
        nome = request.form['nome']
        genero = request.form['genero']

        # guardar o usuário na sessão
        session['user'] = nome
        
        response = make_response(
            redirect(  url_for('preferencia')  ))
        response.set_cookie(nome, genero, max_age=7*24*3600) #Guarda as informações (nome, genero) por 7 dias.
        
        return response
        

@app.route('/preferencia')
def preferencia():

    if 'user' in session:
        user = session.get('user')
        if user in request.cookies:
            genero = request.cookies.get(user)
            return redirect( url_for('recomendar', genero=genero) )

    return "<h1>Deu ruim</h1>"

@app.route('/recomendar')
def recomendar():
    filmes = {
        'acao' : ['Viúva Negra', 'Batman', 'Velozes e Furiosos 10', 'Os Mercenários 4'],
        'comedia' : ['O Auto da Compadecida', 'Os Farofeiros','Vai Que Cola - O Filme','Curtindo a Vida Adoidado'],
        'drama' : ['A Espera de Um Milagre', 'O Curioso Caso de Benjamin Button', 'Sete Vidas','Histórias Cruzadas'],
        'Ficção' : ['Interestelar','Matrix','Duna','Blade Runner 2049']
    }
    if 'genero' not in request.args:
        return 'GENERO não informado'
    genero = request.args.get('genero')
    if genero in filmes.keys():
        lista = filmes[genero]

    return render_template('filmes.html', filmes=lista)
