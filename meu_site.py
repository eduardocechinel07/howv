from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Definição do modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)

# Cria todas as tabelas necessárias no banco de dados
with app.app_context():
    db.create_all()

# Usuário admin (apenas para fins de demonstração)
admin_username = "admin"
admin_password = "familia_betel"

# Verifica a autenticação
def check_auth(username, password):
    # Se o usuário for o admin e a senha estiver correta
    if username == admin_username and password == admin_password:
        return True
    
    # Verifica se existe um usuário com o nome de usuário e senha fornecidos
    user = User.query.filter_by(username=username, password=password).first()
    return user is not None

# Página de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_auth(username, password):
            # Cria uma sessão para o usuário autenticado
            session.permanent = True
            session['username'] = username
            return redirect(url_for("homepage"))
        else:
            error = "Usuário ou senha incorretos. Tente novamente."
            return render_template("login.html", error=error)
    return render_template("login.html")

# Página de cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        endereco = request.form["endereco"]
        if not User.query.filter_by(username=username).first():
            # Verifica se o usuário já existe
            new_user = User(username=username, password=password, email=email, telefone=telefone, endereco=endereco)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            error = "Este usuário já existe. Por favor, escolha outro."
            return render_template("cadastro.html", error=error)
    return render_template("cadastro.html")

# Página inicial
@app.route("/")
def homepage():
    if 'username' in session:
        # Se o usuário estiver autenticado, exiba o botão de logout
        return render_template("homepage.html", username=session['username'])
    else:
        return render_template("homepage.html")

# Página de logout
@app.route("/logout")
def logout():
    # Remova o nome de usuário da sessão se estiver presente
    session.pop('username', None)
    return redirect(url_for('homepage'))

@app.route("/alterar_escala", methods=["GET", "POST"])
def alterar_escala():
    # Se o método for GET, renderize a página HTML do formulário
    return render_template("alterar_escala.html")

# Página da escala
@app.route("/escala", methods=["GET", "POST"])
def escala():
    if 'username' not in session:
        # Se o usuário não estiver autenticado, redirecione-o para a página de login
        return redirect(url_for('login'))

    # Dados de exemplo para as escalas
    escalas_limpeza = [
        {"data": "04 de abril", "grupo": "Grupo 01"},
        {"data": "11 de abril", "grupo": "Grupo 02"},
        {"data": "18 de abril", "grupo": "Grupo 03"},
        {"data": "25 de abril", "grupo": "Grupo 04"}
    ]

    escalas_diaconato = [
        {"data": "04 de abril", "casal": "Casal 01"},
        {"data": "11 de abril", "casal": "Casal 02"},
        {"data": "18 de abril", "casal": "Casal 03"},
        {"data": "25 de abril", "casal": "Casal 04"}
    ]

    return render_template("escala.html", escalas_limpeza=escalas_limpeza, escalas_diaconato=escalas_diaconato)
    

# Página para listar usuários
@app.route("/usuarios")
def listar_usuarios():
    # Verifica se o usuário está autenticado
    if 'username' not in session:
        return redirect(url_for("login"))
    
    usuarios = User.query.all()
    return render_template("listar_usuarios.html", usuarios=usuarios)

# Rodar o aplicativo
if __name__ == "__main__":
    app.run(debug=True)
