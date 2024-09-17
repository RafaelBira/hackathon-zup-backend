from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    session,
    redirect,
    url_for,
    flash,
)  # Adicione session e redirect
from app.services import create_user, find_user_by_email, get_all_users
from app.ia import recommend_articles
import bcrypt

# Definimos um blueprint para gerenciar as rotas do usuário
user_bp = Blueprint("user_bp", __name__)

# Defina uma chave secreta para a sessão (faça isso no arquivo principal da sua aplicação)
# app.secret_key = 'sua_chave_secreta_aqui'


# Rota para registrar um novo usuário
@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        # Retorna a página de registro
        return render_template("register.html")
    elif request.method == "POST":
        try:
            username = request.form.get("userName")
            email = request.form.get("email")
            password = request.form.get("password")
            businessName = request.form.get("business")
            interests = request.form.getlist(
                "areasOfInterest"
            )  # Captura os valores dos checkboxes selecionados

            # Verifica se o usuário já existe
            if find_user_by_email(email):
                flash("O e-mail já está registrado. Tente outro e-mail.", "error")
                return redirect(url_for("user_bp.register"))

            # Cria o novo usuário com senha hash
            create_user(username, email, password, businessName, interests)
            return redirect(url_for("user_bp.register_successfully"))

        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500


@user_bp.route("/sucessregister")
def register_successfully():
    # Exibe a mensagem de sucesso e redireciona automaticamente para o login
    return render_template("register_successfully.html")


# Rota para login
@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            password = request.form.get("pwd")
            user = find_user_by_email(email)
            print(password)
            print(user)
            if user is None:
                return jsonify({"error": "Invalid email"}), 400

            if not (password == user["password"]):
                return jsonify({"error": "Invalid password"}), 400

            # Salva o ID do usuário na sessão
            session["user_id"] = user["id"]

            # Redireciona para a página principal
            return redirect(url_for("user_bp.main_page"))
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500
    return render_template("login.html")


@user_bp.route("/")
def login_redirect():
    return redirect(url_for("user_bp.login"))


# Rota para obter todos os usuários
@user_bp.route("/users", methods=["GET"])
def get_users():
    users = get_all_users()  # Chama a função que busca todos os usuários
    print(users)
    return jsonify(users), 200


# Rota para a página principal
@user_bp.route("/main", methods=["GET"])
def main_page():
    # Resgata o ID do usuário da sessão
    user_id = session.get("user_id")

    if not user_id:
        return redirect(
            url_for("user_bp.login")
        )  # Redireciona para o login se o usuário não estiver logado

    try:
        # Pega as recomendações para o user_id
        recommendations = recommend_articles(user_id)

        # Renderiza o template e passa as recomendações
        return render_template("main.html", recommendations=recommendations.split(";"))
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
