from flask import Flask
from core.database import init_db
from app.controllers import user_bp

app = Flask(__name__)

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
