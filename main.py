from flask import Flask
from core.database import init_db
from app.controllers import user_bp

app = Flask(__name__)

# Inicializa o banco de dados (cria a tabela se não existir)
init_db()

# Registra o blueprint das rotas de usuário
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
