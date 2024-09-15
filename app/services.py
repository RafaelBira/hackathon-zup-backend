from core.database import get_db_connection

# Função para criar um novo usuário
def create_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Função para buscar um usuário pelo nome de usuário
def find_user_by_username(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user
