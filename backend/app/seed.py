"""Carga inicial do banco: categorias e cupcakes da vitrine."""

from app.models import db, Categoria, Produto

# (categoria, nome, descrição, preço, imagem)
PRODUTOS = [
    (
        "Clássicos",
        "Baunilha",
        "Massa de baunilha com cobertura de buttercream e chocolate branco.",
        9.90,
        "baunilha.jpg",
    ),
    (
        "Clássicos",
        "Chocolate Belga",
        "Massa de cacau com ganache de chocolate belga.",
        11.90,
        "chocolate-belga.jpg",
    ),
    (
        "Clássicos",
        "Red Velvet",
        "Massa aveludada com cobertura de cream cheese.",
        12.90,
        "red-velvet.jpg",
    ),
    (
        "Frutas",
        "Morango",
        "Massa e cobertura de morango com calda da fruta.",
        11.50,
        "morango.jpg",
    ),
    (
        "Frutas",
        "Limão Siciliano",
        "Massa cítrica com creme e calda de limão siciliano.",
        11.50,
        "limao-siciliano.jpg",
    ),
    (
        "Especiais",
        "Doce de Leite",
        "Cobertura cremosa de doce de leite com castanhas.",
        13.90,
        "doce-de-leite.jpg",
    ),
    (
        "Especiais",
        "Pistache",
        "Massa de pistache com cobertura de chocolate branco.",
        15.90,
        "pistache.jpg",
    ),
    (
        "Especiais",
        "Avelã",
        "Massa de chocolate com creme de avelã e avelãs picadas.",
        14.90,
        "avela.jpg",
    ),
]


def popular_produtos():
    # Se já existe algum produto, a carga já foi feita: não duplica
    if Produto.query.first():
        return

    categorias = {}
    for nome_categoria, nome, descricao, preco, imagem in PRODUTOS:
        if nome_categoria not in categorias:
            categorias[nome_categoria] = Categoria(nome=nome_categoria)
            db.session.add(categorias[nome_categoria])

        db.session.add(
            Produto(
                nome=nome,
                descricao=descricao,
                preco=preco,
                estoque=50,
                imagem=imagem,
                categoria=categorias[nome_categoria],
            )
        )

    db.session.commit()


def criar_admin():
    """Cria o usuário administrador padrão (usado para gerenciar os pedidos)."""
    from app.models import Usuario

    if Usuario.query.filter_by(is_admin=True).first():
        return

    admin = Usuario(
        nome="Administrador",
        email="admin@cupcakes.com",
        endereco="Loja Cupcakes Gourmet",
        is_admin=True,
    )
    admin.definir_senha("admin123")
    db.session.add(admin)
    db.session.commit()
