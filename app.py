from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelos de Usuário e Reserva
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10), nullable=False)  # Formato 'YYYY-MM-DD'
    horario = db.Column(db.String(5), nullable=False)  # Formato 'HH:MM-HH:MM'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    user = db.relationship('User', backref='reservas')  # Adicionando o relacionamento

def obter_horarios_disponiveis(data_atual):
    horarios = []
    for h in range(8, 24):  # De 08:00 a 23:00
        horario = f"{h:02d}:00-{h + 1:02d}:00"
        reservas_existentes = Reserva.query.filter_by(data=data_atual, horario=horario).all()
        if not reservas_existentes:  # Se não houver reservas, adicione à lista
            horarios.append(horario)
    return horarios

# Funções de login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # Alterado para usar Session.get()

# Rotas
@app.route('/')
def index():
    return render_template('index.html', datetime=datetime, timedelta=timedelta, Reserva=Reserva)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        password = request.form['password']
        user = User.query.filter_by(cpf=cpf).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('CPF ou senha incorretos')
    return render_template('login.html')

@app.route('/reserva', methods=['GET', 'POST'])
@login_required
def reserva():
    data_atual = datetime.now().strftime('%Y-%m-%d')  # Obtém a data atual
    if request.method == 'POST':
        horario = request.form['horario']
        nova_reserva = Reserva(data=data_atual, horario=horario, user_id=current_user.id)
        db.session.add(nova_reserva)
        db.session.commit()
        flash('Reserva realizada com sucesso!')
        return redirect(url_for('index'))
    
    horarios_disponiveis = obter_horarios_disponiveis(data_atual)
    return render_template('reserva.html', horarios=horarios_disponiveis)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cpf = request.form['cpf']
        nome = request.form['nome']
        password = request.form['password']
        
        # Verifique se o CPF já está cadastrado
        if User.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado. Tente outro.')
            return redirect(url_for('register'))
        
        # Criação do novo usuário
        novo_usuario = User(cpf=cpf, nome=nome, password=password)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('login'))  # Redireciona para a página de login após o registro

    return render_template('register.html')  # Retorna o template de registro

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.')
    return redirect(url_for('index'))

@app.route('/proxima_semana')
@login_required
def proxima_semana():
    data_atual = datetime.now()
    data_futura = data_atual + timedelta(weeks=1)
    return f"A data da próxima semana será: {data_futura.strftime('%Y-%m-%d')}"

if __name__ == '__main__':
    with app.app_context():  # Cria um contexto de aplicação
        db.create_all()  # Isso criará as tabelas definidas nos modelos
    app.run(debug=True)  # Executa o aplicativo Flask
