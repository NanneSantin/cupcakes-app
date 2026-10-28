from datetime import datetime
from app.models import db


class Pedido(db.Model):
    __tablename__ = "pedido"

    # Etapas possíveis do pedido (acompanhamento)
    STATUS = ["Aguardando pagamento", "Pago", "Em preparo",
              "Saiu para entrega", "Entregue", "Cancelado"]

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default="Aguardando pagamento", nullable=False)
    endereco_entrega = db.Column(db.String(255), nullable=False)
    forma_pagamento = db.Column(db.String(20))  # PIX ou CARTAO (simulado)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False, default=0)

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True,
                            cascade="all, delete-orphan")


class ItemPedido(db.Model):
    __tablename__ = "item_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(8, 2), nullable=False)

    produto = db.relationship("Produto")