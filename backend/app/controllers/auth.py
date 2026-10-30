"""Controller de autenticação (C do MVC): cadastro, login e logout."""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Usuario
from app.validacoes import EMAIL_VALIDO, validar_nome, validar_endereco

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for("vitrine.index"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefone = request.form.get("telefone", "").strip()
        endereco = request.form.get("endereco", "").strip()
        senha = request.form.get("senha", "")
        confirmacao = request.form.get("confirmacao", "")

        # Validações: todas as mensagens de erro são mostradas de uma vez
        erros = []
        if not nome or not email or not endereco or not senha:
            erros.append("Preencha todos os campos obrigatórios.")
        if nome and validar_nome(nome):
            erros.append(validar_nome(nome))
        if endereco and validar_endereco(endereco):
            erros.append(validar_endereco(endereco))
        if email and not EMAIL_VALIDO.match(email):
            erros.append("Informe um e-mail válido.")
        if senha and len(senha) < 6:
            erros.append("A senha deve ter pelo menos 6 caracteres.")
        if senha != confirmacao:
            erros.append("A confirmação de senha não confere.")
        if email and Usuario.query.filter_by(email=email).first():
            erros.append("Este e-mail já está cadastrado.")

        if erros:
            for erro in erros:
                flash(erro, "danger")
            # Devolve o formulário com o que a pessoa já tinha digitado
            return render_template("pages/cadastro.html", dados=request.form), 400

        usuario = Usuario(nome=nome, email=email, telefone=telefone, endereco=endereco)
        usuario.definir_senha(senha)
        db.session.add(usuario)
        db.session.commit()

        login_user(usuario)
        flash(
            f"Bem-vindo(a), {usuario.nome}! Cadastro realizado com sucesso.", "success"
        )
        return redirect(url_for("vitrine.index"))

    return render_template("pages/cadastro.html", dados={})


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("vitrine.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = Usuario.query.filter_by(email=email).first()

        # Mensagem genérica: não revela se o e-mail existe ou não (segurança)
        if not usuario or not usuario.verificar_senha(senha):
            flash("E-mail ou senha incorretos.", "danger")
            return render_template("pages/login.html", email=email), 401

        login_user(usuario)
        flash(f"Olá, {usuario.nome}!", "success")

        # Se a pessoa tentou acessar uma página protegida, volta para ela
        proxima = request.args.get("next")
        if proxima and proxima.startswith("/"):
            return redirect(proxima)
        return redirect(url_for("vitrine.index"))

    return render_template("pages/login.html", email="")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("vitrine.index"))
