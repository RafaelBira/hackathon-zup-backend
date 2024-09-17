import json
from llamaapi import LlamaAPI
from core.database import get_db_connection

# Inicializando a API
llama = LlamaAPI("LA-bd19861e71f94fbca02392cd04c5f369e6d48af528ca4706ad429b96a61e0c33")

# Função para buscar os interesses do usuário
def get_user_interests(user_id):
    conn = get_db_connection()
    c = conn.cursor()

    # Buscar os interesses do usuário específico na tabela `users`
    c.execute("SELECT interesses FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()

    if user and user['interesses']:
        # Retorna os interesses como lista (deserializados de JSON)
        return json.loads(user['interesses'])
    return []

# Função para buscar todos os artigos
def get_all_articles():
    conn = get_db_connection()
    c = conn.cursor()

    # Buscar todos os artigos na tabela `artigos`
    c.execute("SELECT titulo, descricao FROM artigos")
    articles = c.fetchall()
    conn.close()

    # Preparar uma lista de descrições de artigos
    return [f"{article['titulo']}: {article['descricao']}" for article in articles]

# Função para gerar recomendações de artigos baseadas nos interesses do usuário
def recommend_articles(user_id):
    # Buscar os interesses do usuário
    user_interests = get_user_interests(user_id)

    # Buscar todos os artigos
    all_articles = get_all_articles()
    print(all_articles)
    # Preparar o conteúdo para enviar à LLaMA
    interesses_str = ', '.join(user_interests)  # Convertendo interesses em uma string
    artigos_str = '. '.join(all_articles)  # Convertendo os artigos em uma string

    # Definindo o JSON de requisição para a API LLaMA
    api_request_json = {
        "messages": [
            {"role": "system", "content": f"Interesses do usuário: {interesses_str}. Artigos: {artigos_str}"},
            {"role": "user", "content": "Responda separado por Artigo em ligua portuguesa as recomendacoes que se enquadram no perfil desse usuario, apenas o nome do artigo e nada mais. Resposta deve ser em portugues separando os resultados por ';'"}
        ],
        "max_tokens": 200
    }

    # Executando a requisição na API LLaMA
    response = llama.run(api_request_json)

    # Acessando o conteúdo desejado da resposta da API
    conteudo_total = response.json()  # Converte a resposta para um dicionário
    artigos_recomendados = conteudo_total['choices'][0]['message']['content']  # Acessa o campo específico

    return artigos_recomendados  # Retorna os artigos recomendados

# Exemplo de uso: recomendando artigos para um usuário com ID 1
# user_id = 1
# recomendacoes = recommend_articles(user_id)
# print(recomendacoes)
