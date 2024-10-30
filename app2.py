
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Criação do aplicativo Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Chave secreta para sessões

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dados mockados de usuários
users = {
    'teste@teste.com': {'password': 'senha123'}
}

# Classe User
class User(UserMixin):
    def __init__(self, email):
        self.id = email

# Callback para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Rota para o login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Verificar se o usuário existe e a senha está correta
        if email in users and users[email]['password'] == password:
            user = User(email)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')

    return render_template('login.html')

# Rota protegida
@app.route('/dashboard')
@login_required
def dashboard():
    return f'Bem-vindo, {current_user.id}! <a href="/logout">Logout</a>'

# Rota para logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

# Rota inicial
@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
