from flask import Blueprint, request, jsonify
from app.services import create_user, find_user_by_username, get_all_users
from app.ia import recommend_articles
import bcrypt

# Definimos um blueprint para gerenciar as rotas do usuário
user_bp = Blueprint('user_bp', __name__)

# Rota para registrar um novo usuário
@user_bp.route('/registrar', methods=['POST'])
def registrar():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Verifica se o usuário já existe
        if find_user_by_username(username):
            return jsonify({"error": "Username already registered"}), 400

        # Cria o novo usuário com senha hash
        create_user(username, password)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

# Rota para login
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Busca o usuário no banco de dados
        user = find_user_by_username(username)
        if user is None:
            return jsonify({"error": "Invalid username or password"}), 400

        # Verifica a senha usando bcrypt
        if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return jsonify({"error": "Invalid username or password"}), 400

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
