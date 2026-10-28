from app.models import db


class Produto(db.Model):
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(8, 2), nullable=False)
    estoque = db.Column(db.Integer, default=0, nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    cor = db.Column(db.String(7), default="#f8b4c8")  # cor do card na vitrine
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)