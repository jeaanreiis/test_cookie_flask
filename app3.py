from flask import Flask, request, redirect, url_for, make_response, flash, render_template_string

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = {
    'teste@teste.com': 'senha123'
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if user %}Dashboard{% else %}Login{% endif %}</title>
</head>
<body>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <ul>
        {% for category, message in messages %}
          <li class="{{ category }}">{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    {% if user %}
        <h1>Bem-vindo, {{ user }}!</h1>
        <a href="/logout">Logout</a>
    {% else %}
        <h1>Login</h1>
        <form method="POST" action="/login">
            <label for="email">Email:</label>
            <input type="email" name="email" required>
            <br>
            <label for="password">Senha:</label>
            <input type="password" name="password" required>
            <br>
            <button type="submit">Entrar</button>
        </form>
    {% endif %}
</body>
</html>
'''

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verificar se o usuário existe e a senha está correta
        if email in users and users[email] == password:
            # Criar um cookie com o email do usuário
            resp = make_response(render_template_string(HTML_TEMPLATE, user=email))
            resp.set_cookie('user_email', email)  # Armazena o email no cookie
            flash('Login bem-sucedido!', 'success')
            return resp
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')

    user_email = request.cookies.get('user_email')
    return render_template_string(HTML_TEMPLATE, user=user_email)

# Rota protegida (dashboard)
@app.route('/dashboard')
def dashboard():
    user_email = request.cookies.get('user_email')  # Recupera o cookie

    if user_email and user_email in users:
        return render_template_string(HTML_TEMPLATE, user=user_email)
    return redirect(url_for('login'))

# Rota para logout
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('user_email', '', expires=0)  # Remove o cookie definindo a expiração
    resp.delete_cookie('user_email')
    flash('Logout realizado com sucesso.', 'success')
    return resp

# Rota inicial
@app.route('/')
def index():
    user_email = request.cookies.get('user_email')
    return render_template_string(HTML_TEMPLATE, user=user_email)

if __name__ == '__main__':
    app.run(debug=True)
