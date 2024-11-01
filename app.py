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
    if request.method == 'POST':
        data = request.form['data']
        horario = request.form['horario']
        
        # Converte a data escolhida para um objeto datetime
        data_escolhida = datetime.strptime(data, '%Y-%m-%d')
        horario_inicial = int(horario.split(':')[0])  # Pega a hora inicial do horário selecionado
        data_atual = datetime.now()

        # Define o limite de 48 horas a partir da data atual
        data_limite = data_atual + timedelta(days=2)

        # Verifica se a data é no passado (considerando a hora atual)
        if data_escolhida.date() < data_atual.date():
            flash('A data não pode ser no passado.')
            return redirect(url_for('reserva'))

        # Verifica se a data está além do limite de 48 horas
        if data_escolhida.date() > data_limite.date():
            flash('A data deve ser marcada com no máximo 2 dias de antecedência. Por favor, escolha uma data válida.')
            return redirect(url_for('reserva'))

        # Verifica se a reserva é para hoje e se o horário selecionado é menor que a hora atual + 1 hora
        if data_escolhida.date() == data_atual.date():
            if horario_inicial < data_atual.hour or (horario_inicial == data_atual.hour and data_atual.minute >= 0):
                flash('Você não pode reservar para hoje com menos de 1 hora de antecedência.')
                return redirect(url_for('reserva'))

        # Verifica se já existe uma reserva nesse horário
        reserva_existente = Reserva.query.filter_by(data=data, horario=horario).first()
        if reserva_existente:
            flash('Esse horário já está reservado.')
            return redirect(url_for('reserva'))

        # Cria a nova reserva
        nova_reserva = Reserva(data=data, horario=horario, user_id=current_user.id)
        db.session.add(nova_reserva)
        db.session.commit()
        flash('Reserva realizada com sucesso!')
        return redirect(url_for('index'))

    # Obtém horários disponíveis para a data atual
    horarios = obter_horarios_disponiveis(datetime.now().strftime('%Y-%m-%d'))
    return render_template('reserva.html', horarios=horarios)





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
    data_futura = data_atual + timedelta(days=3)
    return f"A data da próxima semana será: {data_futura.strftime('%Y-%m-%d')}"

@app.route('/minhas_reservas', methods=['GET', 'POST'])
@login_required
def minhas_reservas():
    # Obtém todas as reservas do usuário atual
    reservas = Reserva.query.filter_by(user_id=current_user.id).all()
    
    return render_template('minhas_reservas.html', reservas=reservas)

@app.route('/excluir_reserva/<int:id>')
@login_required
def excluir_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    
    # Verifica se a reserva pertence ao usuário atual
    if reserva.user_id == current_user.id:
        db.session.delete(reserva)
        db.session.commit()
        flash('Reserva excluída com sucesso!')
    else:
        flash('Você não tem permissão para excluir esta reserva.')

    return redirect(url_for('minhas_reservas'))


if __name__ == '__main__':
    with app.app_context():  # Cria um contexto de aplicação
        db.create_all()  # Isso criará as tabelas definidas nos modelos
    app.run(debug=True)  # Executa o aplicativo Flask