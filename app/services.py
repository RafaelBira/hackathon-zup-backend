import bcrypt
from core.database import get_db_connection

# Função para criar um novo usuário com senha hash
def create_user(username, password):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Gerar o hash da senha
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
    finally:
        conn.close()

# Função para buscar um usuário pelo nome de usuário
def find_user_by_username(username):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        return user
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None
    finally:
        conn.close()
