"""Carga inicial do banco: categorias e cupcakes da vitrine."""
from app.models import db, Categoria, Produto

# (categoria, nome, descrição, preço, cor do card)
PRODUTOS = [
    ("Clássicos", "Baunilha", "Massa de baunilha com cobertura de buttercream.", 9.90, "#f9e4b7"),
    ("Clássicos", "Chocolate Belga", "Massa de cacau com ganache de chocolate belga.", 11.90, "#a47551"),
    ("Clássicos", "Red Velvet", "Massa aveludada com cream cheese.", 12.90, "#c94c4c"),
    ("Frutas", "Morango", "Recheio de geleia de morango e chantilly.", 11.50, "#f8b4c8"),
    ("Frutas", "Limão Siciliano", "Massa cítrica com merengue maçaricado.", 11.50, "#f3f0a1"),
    ("Especiais", "Doce de Leite", "Recheio cremoso de doce de leite artesanal.", 13.90, "#d9a066"),
    ("Especiais", "Pistache", "Massa de pistache com cobertura de chocolate branco.", 15.90, "#b5d99c"),
    ("Especiais", "Nutella", "Recheado e coberto com creme de avelã.", 14.90, "#7b4b2a"),
]


def popular_produtos():
    # Se já existe algum produto, a carga já foi feita: não duplica
    if Produto.query.first():
        return

    categorias = {}
    for nome_categoria, nome, descricao, preco, cor in PRODUTOS:
        if nome_categoria not in categorias:
            categorias[nome_categoria] = Categoria(nome=nome_categoria)
            db.session.add(categorias[nome_categoria])

        db.session.add(Produto(
            nome=nome, descricao=descricao, preco=preco,
            estoque=50, cor=cor, categoria=categorias[nome_categoria],
        ))

    db.session.commit()