from flask import Blueprint, request, jsonify
from app.services import create_user, find_user_by_username

# Definimos um blueprint para gerenciar as rotas do usuário
user_bp = Blueprint('user_bp', __name__)

# Rota para registrar um novo usuário
@user_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Verifica se o usuário já existe
    if find_user_by_username(username):
        return jsonify({"error": "Username already registered"}), 400
    
    # Cria o novo usuário
    create_user(username, password)
    return jsonify({"message": "User registered successfully"}), 201

# Rota para login
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Busca o usuário no banco de dados
    user = find_user_by_username(username)
    if user is None or user['password'] != password:
        return jsonify({"error": "Invalid username or password"}), 400

    return jsonify({"message": "Login successful"}), 200

# Rota para recomendação
@user_bp.route('/recomendacoes', methods=['GET'])
def recomendacoes():
    recommendations = [
        {"recommendation": "Recomendação 1"},
        {"recommendation": "Recomendação 2"},
        {"recommendation": "Recomendação 3"},
    ]
    return jsonify(recommendations), 200
