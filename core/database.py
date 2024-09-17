import sqlite3
import json


# Função para obter a conexão com o banco de dados
def get_db_connection():
    try:
        conn = sqlite3.connect("database.db")
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
            c.execute(
                """CREATE TABLE IF NOT EXISTS users
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT NOT NULL UNIQUE,
                          email TEXT NOT NULL UNIQUE,
                          password TEXT NOT NULL,
                          businessName TEXT NOT NULL,
                  interests TEXT)"""
            )

            c.execute(
                """CREATE TABLE IF NOT EXISTS artigos
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      titulo TEXT NOT NULL,
                      descricao TEXT NOT NULL,
                      link TEXT NOT NULL)"""
            )

            users = [
                (
                    "rafael",
                    "rafa@gmail.com",
                    "password123",
                    "loja de doce",
                    json.dumps(["tecnologia"]),
                ),
                (
                    "marcos",
                    "marcos@gmail.com",
                    "password456",
                    "Bar",
                    json.dumps(["gastronomia", "tecnologia"]),
                ),
                (
                    "alice",
                    "ali@gmail.com",
                    "password789",
                    "Taberna",
                    json.dumps(["comercio", "gastronomia"]),
                ),
            ]

            # Insere cada usuário no banco
            c.executemany(
                """INSERT INTO users (username, email, password,empreendimento, interesses)
                             VALUES (?, ?, ?,?,?)""",
                users,
            )
            print("Usuários inseridos com sucesso!")

            artigos = [
                (
                    "Tendências em Inteligência Artificial",
                    "Explorando as principais tendências e inovações em IA para o futuro.",
                    "https://exemplo.com/ia",
                ),
                (
                    "E-commerce: Como Iniciar Seu Negócio",
                    "Dicas e passos para quem deseja abrir uma loja online.",
                    "https://exemplo.com/ecommerce",
                ),
                (
                    "SEO para Negócios Locais",
                    "Como aplicar SEO em negócios locais e aumentar a visibilidade.",
                    "https://exemplo.com/seo-negocios-locais",
                ),
                (
                    "Inovações em Gastronomia Molecular",
                    "As últimas inovações da gastronomia molecular e como isso impacta o mercado.",
                    "https://exemplo.com/gastronomia-molecular",
                ),
                (
                    "Destinos Turísticos em Alta para 2024",
                    "Principais destinos turísticos que estarão em alta no próximo ano.",
                    "https://exemplo.com/destinos-2024",
                ),
                (
                    "Marketing Cultural: Atraindo Novos Públicos",
                    "Como o marketing cultural pode atrair novos públicos e fomentar a cultura.",
                    "https://exemplo.com/marketing-cultural",
                ),
                (
                    "O Futuro da Internet das Coisas",
                    "O impacto e o futuro da Internet das Coisas nas empresas e na sociedade.",
                    "https://exemplo.com/iot-futuro",
                ),
            ]

            c.executemany(
                """INSERT INTO artigos (titulo, descricao, link) 
                             VALUES (?, ?, ?)""",
                artigos,
            )
            print("Artigos inseridos com sucesso!")

            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()
