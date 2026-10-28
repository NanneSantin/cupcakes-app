"""Camada Model (M do MVC): entidades do banco de dados."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Os imports ficam abaixo do "db" porque cada model usa o db.
# Importar aqui garante que todas as tabelas sejam criadas no db.create_all().
from app.models.usuario import Usuario  
from app.models.categoria import Categoria  
from app.models.produto import Produto  
from app.models.pedido import Pedido, ItemPedido  