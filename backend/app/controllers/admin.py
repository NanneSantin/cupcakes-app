"""Controller do administrador (C do MVC): gerenciamento dos pedidos."""

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import db, Pedido
from app.validacoes import endereco_interno

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_obrigatorio(funcao):
    """Só deixa passar usuários administradores (os demais recebem erro 403)."""

    @wraps(funcao)
    @login_required
    def verificar(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return funcao(*args, **kwargs)

    return verificar


@admin_bp.route("/pedidos")
@admin_obrigatorio
def pedidos():
    status_filtro = request.args.get("status", "")
    consulta = Pedido.query
    if status_filtro in Pedido.STATUS:
        consulta = consulta.filter_by(status=status_filtro)
    lista = consulta.order_by(Pedido.data_pedido.desc()).all()
    return render_template(
        "admin/pedidos.html",
        pedidos=lista,
        status_lista=Pedido.STATUS,
        status_filtro=status_filtro,
    )


@admin_bp.route("/pedidos/<int:pedido_id>/status", methods=["POST"])
@admin_obrigatorio
def alterar_status(pedido_id):
    pedido = db.session.get(Pedido, pedido_id) or abort(404)
    novo_status = request.form.get("status", "")

    # Depois de salvar, volta para a mesma tela do painel (com o filtro que estava aplicado).
    # Não usamos o "Referer" do navegador, porque alguns navegadores não o enviam.
    proxima = request.form.get("proxima", "")
    destino = proxima if endereco_interno(proxima) else url_for("admin.pedidos")

    if novo_status not in Pedido.STATUS:
        flash("Status inválido.", "danger")
    elif novo_status != pedido.status:
        # Ao cancelar, os produtos voltam para o estoque
        if novo_status == "Cancelado":
            for item in pedido.itens:
                item.produto.estoque += item.quantidade
        elif pedido.status == "Cancelado":
            flash("Um pedido cancelado não pode ser reaberto.", "warning")
            return redirect(destino)

        pedido.status = novo_status
        db.session.commit()
        flash(f'Pedido #{pedido.id} atualizado para "{novo_status}".', "success")

    return redirect(destino)
