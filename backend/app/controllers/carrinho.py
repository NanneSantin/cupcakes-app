"""Controller do carrinho (C do MVC).

O carrinho fica guardado na sessão do navegador (não no banco), no formato
{"id_do_produto": quantidade}. Ele só vira pedido no banco ao finalizar a compra.
"""

from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Produto

carrinho_bp = Blueprint("carrinho", __name__, url_prefix="/carrinho")


def obter_carrinho():
    return session.get("carrinho", {})


def salvar_carrinho(carrinho):
    session["carrinho"] = carrinho
    session.modified = True


def itens_do_carrinho():
    """Monta a lista de itens com produto, quantidade e subtotal, e o total geral."""
    itens = []
    total = Decimal("0.00")
    for produto_id, quantidade in obter_carrinho().items():
        produto = db.session.get(Produto, int(produto_id))
        if not produto or not produto.ativo:
            continue
        subtotal = produto.preco * quantidade
        total += subtotal
        itens.append(
            {"produto": produto, "quantidade": quantidade, "subtotal": subtotal}
        )
    return itens, total


def ler_quantidade(produto):
    """Lê a quantidade do formulário e garante que fique entre 1 e o estoque."""
    quantidade = request.form.get("quantidade", type=int) or 1
    return max(1, min(quantidade, produto.estoque))


@carrinho_bp.app_context_processor
def quantidade_no_carrinho():
    # Disponibiliza o total de itens para todas as telas (ícone do menu)
    return {"qtd_carrinho": sum(obter_carrinho().values())}


@carrinho_bp.route("/")
def ver():
    itens, total = itens_do_carrinho()
    return render_template("pages/carrinho.html", itens=itens, total=total)


@carrinho_bp.route("/adicionar/<int:produto_id>", methods=["POST"])
def adicionar(produto_id):
    produto = Produto.query.filter_by(id=produto_id, ativo=True).first_or_404()
    carrinho = obter_carrinho()
    chave = str(produto_id)

    nova_quantidade = carrinho.get(chave, 0) + ler_quantidade(produto)
    if nova_quantidade > produto.estoque:
        nova_quantidade = produto.estoque
        flash(
            f"Temos apenas {produto.estoque} unidades de {produto.nome} em estoque.",
            "warning",
        )
    else:
        flash(f"{produto.nome} adicionado ao carrinho!", "success")

    carrinho[chave] = nova_quantidade
    salvar_carrinho(carrinho)

    proxima = request.form.get("proxima", "")
    if proxima.startswith("/") and not proxima.startswith("//"):
        return redirect(proxima)
    return redirect(url_for("carrinho.ver"))


@carrinho_bp.route("/atualizar/<int:produto_id>", methods=["POST"])
def atualizar(produto_id):
    produto = Produto.query.filter_by(id=produto_id, ativo=True).first_or_404()
    carrinho = obter_carrinho()
    if str(produto_id) in carrinho:
        carrinho[str(produto_id)] = ler_quantidade(produto)
        salvar_carrinho(carrinho)
        flash("Quantidade atualizada.", "info")
    return redirect(url_for("carrinho.ver"))


@carrinho_bp.route("/remover/<int:produto_id>", methods=["POST"])
def remover(produto_id):
    carrinho = obter_carrinho()
    if carrinho.pop(str(produto_id), None) is not None:
        salvar_carrinho(carrinho)
        flash("Item removido do carrinho.", "info")
    return redirect(url_for("carrinho.ver"))
