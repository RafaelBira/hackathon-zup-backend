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

            selected_interests = []
            checkboxes = request.form.getlist('areasOfInterest') # Captura os valores dos checkboxes selecionados
            for checkbox in checkboxes:
                selected_interests.append(checkbox)
            
            data = request.get_json()
            username = data['username']
            email =    data['email']
            password = data['password']
            empreendimento = data['empreendimento']
            interesse = data[selected_interests]

            # Verifica se o usuário já existe
            if find_user_by_email(email):
                return jsonify({"error": "email already registered"}), 400

            # Cria o novo usuário com senha hash
            create_user(username, password,email,empreendimento,interesse )
            return jsonify({"message": "User registered successfully"}), 201
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500

# Rota para login
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Retorna a página de login ou uma resposta simples
        return render_template('login.html')  # Certifique-se de ter um arquivo login.html
    elif request.method == 'POST':
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']
            # Busca o usuário no banco de dados
            user = find_user_by_email(email)
            if user is None:
                return jsonify({"error": "Invalid email or password"}), 400
            # Verifica a senha usando bcrypt
            if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
                return jsonify({"error": "Invalid email or password"}), 400
            return jsonify({"message": "Login successful"}), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500

# Rota para recomendação
@user_bp.route('/recomendacoes', methods=['GET'])
def recomendacoes():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "Parâmetro `user_id` é obrigatório."}), 400

    try:
        recommendations = recommend_articles(user_id)
        return jsonify({"recomendations": recommendations}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()  # Chama a função que busca todos os usuários
    return jsonify(users), 200