import bcrypt
import json
from core.database import get_db_connection


# Função para criar um novo usuário com senha hash
def create_user(username, email, password, businessName, interests):
    try:
        conn = get_db_connection()
        c = conn.cursor()

        c.execute(
            """
            INSERT INTO users (username, email,  password, business, interests) 
            VALUES (?, ?, ?, ?, ?)
        """,
            (username, email, password, businessName, json.dumps(interests)),
        )

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
        # Retornar o usuário (sem expor a senha diretamente)
        if user:
            return {
                "id": user["id"],
                "email": user["email"],
                "password": user[
                    "password"
                ],  # Certifique-se de não expor isso em respostas de API
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
        interests = []
        if user["interests"]:
            try:
                interests = json.loads(
                    user["interests"]
                )  # Tenta carregar os interesses como
            except json.JSONDecodeError as e:
                print(
                    f"Erro ao decodificar JSON em `interesses` para o usuário {user['username']}: {e}"
                )
        result.append(
            {
                "id": user["id"],
                "username": user["username"],
                "interests": interests,
            }
        )

    conn.close()
    return result
