"""Controller de pedidos (C do MVC): checkout, pagamento simulado e acompanhamento."""

import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import db, Pedido, ItemPedido
from app.controllers.carrinho import itens_do_carrinho, salvar_carrinho

pedidos_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")

FORMAS_PAGAMENTO = {"PIX": "Pix", "CARTAO": "Cartão de crédito"}


def buscar_pedido_do_cliente(pedido_id):
    """Retorna o pedido só se ele for do usuário logado; senão, erro 404."""
    pedido = db.session.get(Pedido, pedido_id)
    if not pedido or pedido.usuario_id != current_user.id:
        abort(404)
    return pedido


@pedidos_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    itens, total = itens_do_carrinho()
    if not itens:
        flash("Seu carrinho está vazio.", "warning")
        return redirect(url_for("carrinho.ver"))

    if request.method == "POST":
        endereco = request.form.get("endereco", "").strip()
        forma = request.form.get("forma_pagamento", "")

        erros = []
        if not endereco:
            erros.append("Informe o endereço de entrega.")
        if forma not in FORMAS_PAGAMENTO:
            erros.append("Escolha a forma de pagamento.")
        for item in itens:
            if item["quantidade"] > item["produto"].estoque:
                erros.append(f"Estoque insuficiente de {item['produto'].nome}.")

        if erros:
            for erro in erros:
                flash(erro, "danger")
            return (
                render_template(
                    "pages/checkout.html",
                    itens=itens,
                    total=total,
                    endereco=endereco,
                    forma=forma,
                    formas=FORMAS_PAGAMENTO,
                ),
                400,
            )

        # Cria o pedido e os itens (o preço é copiado para o item, para o
        # pedido não mudar se o preço do produto for alterado depois)
        pedido = Pedido(
            cliente=current_user,
            endereco_entrega=endereco,
            forma_pagamento=forma,
            valor_total=total,
        )
        for item in itens:
            produto = item["produto"]
            pedido.itens.append(
                ItemPedido(
                    produto=produto,
                    quantidade=item["quantidade"],
                    preco_unitario=produto.preco,
                )
            )
            produto.estoque -= item["quantidade"]

        db.session.add(pedido)
        db.session.commit()
        salvar_carrinho({})  # esvazia o carrinho

        return redirect(url_for("pedidos.pagamento", pedido_id=pedido.id))

    return render_template(
        "pages/checkout.html",
        itens=itens,
        total=total,
        endereco=current_user.endereco or "",
        forma="PIX",
        formas=FORMAS_PAGAMENTO,
    )


@pedidos_bp.route("/<int:pedido_id>/pagamento", methods=["GET", "POST"])
@login_required
def pagamento(pedido_id):
    """Pagamento SIMULADO: nenhum valor é cobrado e os dados do cartão não são gravados."""
    pedido = buscar_pedido_do_cliente(pedido_id)

    if pedido.status != "Aguardando pagamento":
        flash("Este pedido já foi pago.", "info")
        return redirect(url_for("pedidos.detalhe", pedido_id=pedido.id))

    if request.method == "POST":
        if pedido.forma_pagamento == "CARTAO":
            numero = re.sub(r"\D", "", request.form.get("numero", ""))
            validade = request.form.get("validade", "").strip()
            cvv = request.form.get("cvv", "").strip()
            nome = request.form.get("nome", "").strip()

            erros = []
            if len(numero) != 16:
                erros.append("O número do cartão deve ter 16 dígitos.")
            if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", validade):
                erros.append("Informe a validade no formato MM/AA.")
            if not re.fullmatch(r"\d{3}", cvv):
                erros.append("O CVV deve ter 3 dígitos.")
            if not nome:
                erros.append("Informe o nome impresso no cartão.")
            if erros:
                for erro in erros:
                    flash(erro, "danger")
                return render_template("pages/pagamento.html", pedido=pedido), 400

            # Regra da simulação: cartão terminado em 0000 é recusado
            if numero.endswith("0000"):
                flash(
                    "Pagamento recusado pela operadora (simulação). Tente outro cartão.",
                    "danger",
                )
                return render_template("pages/pagamento.html", pedido=pedido), 402

        pedido.status = "Pago"
        db.session.commit()
        flash("Pagamento aprovado! Seu pedido já está na fila de preparo.", "success")
        return redirect(url_for("pedidos.detalhe", pedido_id=pedido.id))

    return render_template("pages/pagamento.html", pedido=pedido)


@pedidos_bp.route("/")
@login_required
def listar():
    pedidos = (
        Pedido.query.filter_by(usuario_id=current_user.id)
        .order_by(Pedido.data_pedido.desc())
        .all()
    )
    return render_template("pages/meus_pedidos.html", pedidos=pedidos)


@pedidos_bp.route("/<int:pedido_id>")
@login_required
def detalhe(pedido_id):
    pedido = buscar_pedido_do_cliente(pedido_id)
    return render_template("pages/pedido.html", pedido=pedido, formas=FORMAS_PAGAMENTO)
