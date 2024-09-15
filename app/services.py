import bcrypt
from core.database import get_db_connection

# Função para criar um novo usuário com senha hash
def create_user(username, password):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Gerar o hash da senha
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Inserir o usuário no banco de dados
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except Exception as e:
        # Logar o erro em vez de apenas imprimir
        print(f"Erro ao criar usuário: {e}")
    finally:
        conn.close()

# Função para buscar um usuário pelo nome de usuário
def find_user_by_username(username):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Buscar o usuário pelo nome de usuário
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        
        # Retornar o usuário (sem expor a senha diretamente)
        if user:
            return {
                "id": user["id"],
                "username": user["username"],
                "password": user["password"]  # Certifique-se de não expor isso em respostas de API
            }
        return None
    except Exception as e:
        # Logar o erro em vez de apenas imprimir
        print(f"Erro ao buscar usuário: {e}")
        return None
    finally:
        conn.close()