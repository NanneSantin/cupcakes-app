"""Controller do carrinho (C do MVC).

O carrinho fica guardado na sessão do navegador (não no banco), no formato
{"id_do_produto": quantidade}. Ele só vira pedido no banco ao finalizar a compra.

As rotas de adicionar e atualizar respondem de dois jeitos:
- Pedido normal do formulário: redireciona para outra página (funciona sem JavaScript).
- Pedido feito pelo JavaScript (fetch): responde em JSON, e a tela é atualizada
  sem recarregar (a página não "pula" para o topo).
"""

from decimal import Decimal
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
from app.models import db, Produto
from app.validacoes import ler_quantidade_valida

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


MSG_QTD_INVALIDA = "Quantidade inválida. Informe um número inteiro a partir de 1."


def responder_erro(mensagem, destino, **extras):
    """Erro de validação: JSON para o JavaScript ou mensagem + redirecionamento."""
    if pedido_do_javascript():
        return jsonify(mensagem=mensagem, tipo="danger", **extras), 400
    flash(mensagem, "danger")
    return redirect(destino)


def destino_seguro(padrao):
    """Página de onde a pessoa veio (só endereços internos, por segurança)."""
    proxima = request.form.get("proxima", "")
    if proxima.startswith("/") and not proxima.startswith("//"):
        return proxima
    return padrao


def formatar_moeda(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


def pedido_do_javascript():
    """True quando a requisição veio do JavaScript (fetch) e espera JSON."""
    return request.headers.get("X-Requested-With") == "fetch"


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

    quantidade = ler_quantidade_valida(request.form.get("quantidade"))
    if quantidade is None:
        return responder_erro(MSG_QTD_INVALIDA, destino_seguro(url_for("carrinho.ver")))

    nova_quantidade = carrinho.get(chave, 0) + quantidade
    if nova_quantidade > produto.estoque:
        nova_quantidade = produto.estoque
        mensagem, tipo = (
            f"Temos apenas {produto.estoque} unidades de {produto.nome} em estoque.",
            "warning",
        )
    else:
        mensagem, tipo = f"{produto.nome} adicionado ao carrinho!", "success"

    carrinho[chave] = nova_quantidade
    salvar_carrinho(carrinho)

    if pedido_do_javascript():
        return jsonify(
            mensagem=mensagem, tipo=tipo, qtd_carrinho=sum(carrinho.values())
        )

    flash(mensagem, tipo)
    # Volta para a página de onde a pessoa veio (vitrine ou detalhe do produto)
    return redirect(destino_seguro(url_for("carrinho.ver")))


@carrinho_bp.route("/atualizar/<int:produto_id>", methods=["POST"])
def atualizar(produto_id):
    produto = Produto.query.filter_by(id=produto_id, ativo=True).first_or_404()
    carrinho = obter_carrinho()
    chave = str(produto_id)

    if chave not in carrinho:
        if pedido_do_javascript():
            return (
                jsonify(mensagem="Item não está mais no carrinho.", tipo="warning"),
                404,
            )
        return redirect(url_for("carrinho.ver"))

    quantidade = ler_quantidade_valida(request.form.get("quantidade"))
    if quantidade is None:
        return responder_erro(
            MSG_QTD_INVALIDA, url_for("carrinho.ver"), quantidade=carrinho[chave]
        )

    aviso = None
    if quantidade > produto.estoque:
        quantidade = produto.estoque
        aviso = f"Temos apenas {produto.estoque} unidades de {produto.nome} em estoque."

    carrinho[chave] = quantidade
    salvar_carrinho(carrinho)

    if pedido_do_javascript():
        _, total = itens_do_carrinho()
        return jsonify(
            mensagem=aviso,
            tipo="warning",
            quantidade=carrinho[chave],
            subtotal=formatar_moeda(produto.preco * carrinho[chave]),
            total=formatar_moeda(total),
            qtd_carrinho=sum(carrinho.values()),
        )

    flash(aviso or "Quantidade atualizada.", "warning" if aviso else "info")
    return redirect(url_for("carrinho.ver"))


@carrinho_bp.route("/remover/<int:produto_id>", methods=["POST"])
def remover(produto_id):
    carrinho = obter_carrinho()
    if carrinho.pop(str(produto_id), None) is not None:
        salvar_carrinho(carrinho)
        flash("Item removido do carrinho.", "info")
    return redirect(url_for("carrinho.ver"))
