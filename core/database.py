import sqlite3

# Função para obter a conexão com o banco de dados
def get_db_connection():
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Facilita o acesso às colunas pelo nome
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para inicializar o banco de dados e criar a tabela de usuários
def init_db():
    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Falha ao obter conexão com o banco de dados.")
        
        with conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS users
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT NOT NULL UNIQUE,
                          password TEXT NOT NULL)''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()
