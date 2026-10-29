"""Controller da vitrine (C do MVC): lista e detalhe dos produtos."""

from flask import Blueprint, render_template, request
from app.models import Produto, Categoria

vitrine_bp = Blueprint("vitrine", __name__)


@vitrine_bp.route("/")
def index():
    # Filtro opcional por categoria: /?categoria=2
    categoria_id = request.args.get("categoria", type=int)

    consulta = Produto.query.filter_by(ativo=True)
    if categoria_id:
        consulta = consulta.filter_by(categoria_id=categoria_id)

    produtos = consulta.order_by(Produto.nome).all()
    categorias = Categoria.query.order_by(Categoria.nome).all()

    return render_template(
        "pages/index.html",
        produtos=produtos,
        categorias=categorias,
        categoria_atual=categoria_id,
    )


@vitrine_bp.route("/produto/<int:produto_id>")
def detalhe(produto_id):
    # first_or_404: se o produto não existir, mostra a página de erro 404
    produto = Produto.query.filter_by(id=produto_id, ativo=True).first_or_404()
    return render_template("pages/produto.html", produto=produto)
