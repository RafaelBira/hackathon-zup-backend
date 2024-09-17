import bcrypt
import json
from core.database import get_db_connection

# Função para criar um novo usuário com senha hash
def create_user(username, email, password,  empreendimento, interesse):
    print(f'username: {username}, email: {email}, password: {password}, interesses: {interesse}')
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        
       
        c.execute("""
            INSERT INTO users (username, email,  password, empreendimento, interesses) 
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, password,  empreendimento, json.dumps(interesse)))
        
        conn.commit()
    except Exception as e:
        # Logar o erro em vez de apenas imprimir
        print(f"Erro ao criar usuário: {e}")
    finally:
        conn.close()

# Função para buscar um usuário pelo email do usuario
def find_user_by_email(email):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Buscar o usuário pelo nome de usuário
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        print(user)
        # Retornar o usuário (sem expor a senha diretamente)
        if user:
            return {
                "id": user["id"],
                "email": user["email"],
                "password": user["password"]  # Certifique-se de não expor isso em respostas de API
            }
        return None
    except Exception as e:
        # Logar o erro em vez de apenas imprimir
        print(f"Erro ao buscar usuário: {e}")
        return None
    finally:
        conn.close()

def get_all_users():
    conn = get_db_connection()
    c = conn.cursor()

    # Busca todos os usuários na tabela `users`
    c.execute("SELECT * FROM users")
    users = c.fetchall()

    # Para cada usuário, buscar seus interesses na tabela `interesses`
    result = []
    for user in users:
        interesses = []
        if user['interesses']:
            try:
                interesses = json.loads(user['interesses'])  # Tenta carregar os interesses como 
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON em `interesses` para o usuário {user['username']}: {e}")
#        c.execute("SELECT interesse FROM interesses WHERE user_id = ?", (user["id"],))
#        interesses = [row["interesse"] for row in c.fetchall()]

        result.append({
            "id": user["id"],
            "username": user["username"],
#            "email": user["email"],
#            "password": user["password"],
            "interesses": interesses
        })

    conn.close()
    return result
