from flask import Blueprint, request, jsonify, render_template  # Adicione render_template
from app.services import create_user, find_user_by_email, get_all_users
from app.ia import recommend_articles
import bcrypt

# Definimos um blueprint para gerenciar as rotas do usuário
user_bp = Blueprint('user_bp', __name__)

# Rota para registrar um novo usuário
@user_bp.route('/register', methods=['GET', 'POST'])
def registrar():

    if request.method == 'GET':
        # Retorna a página de login ou uma resposta simples
        return render_template('register.html')  # Certifique-se de ter um arquivo login.html
    elif request.method == 'POST':
        try:
            username = request.form.get('userName')
            email =    request.form.get('email')
            password = request.form.get('password')
            empreendimento = request.form.get('empreendimento')
            interesses = request.form.getlist('areasOfInterest') # Captura os valores dos checkboxes selecionados
            interesses_str = ','.join(interesses)
            # Verifica se o usuário já existe
            if find_user_by_email(email):
                return jsonify({"error": "email already registered"}), 400

            # Cria o novo usuário com senha hash
            create_user(username, password,email,empreendimento,interesses_str )
            return jsonify({"message": "User registered successfully"}), 201
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500

# Rota para login
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')  # Certifique-se de que o nome do campo é 'email'
            password = request.form.get('pwd')
            user = find_user_by_email(email)
            if user is None:
                return jsonify({"error": "Invalid email "}), 400
            if not (password== user['password']):
                return jsonify({"error":  "Invalid password"}), 400
            return render_template('main.html')
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500
    return render_template('login.html')    


@user_bp.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()  # Chama a função que busca todos os usuários
    return jsonify(users), 200

@user_bp.route('/main', methods=['GET'])
def main_page():
    user_id = request.args.get('user_id', default=1, type=int)  # Pode ser dinâmico, neste caso, user_id=1
    try:
        # Pega as recomendações para o user_id
        recommendations = recommend_articles(user_id)
        
        # Renderiza o template e passa as recomendações
        return render_template('main.html', recommendations=recommendations.split(';'))
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500