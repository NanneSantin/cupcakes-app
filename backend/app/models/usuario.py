from datetime import datetime
from app.models import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    pedidos = db.relationship("Pedido", backref="cliente", lazy=True)