from flask import Flask
from flask_cors import CORS
from core.database import init_db
from app.controllers import user_bp

app = Flask(__name__)
app.secret_key = 'sansao123'
CORS(app, resources={r"/*": {"origins": "http://localhost:9000"}})

# Inicializa o banco de dados (cria a tabela se não existir)
try:
    init_db()
except Exception as e:
    print(f"Erro ao inicializar o banco de dados: {e}")

# Registra o blueprint das rotas de usuário
try:
    app.register_blueprint(user_bp)
except Exception as e:
    print(f"Erro ao registrar o blueprint: {e}")

if __name__ == "__main__":
    app.run(debug=True)
