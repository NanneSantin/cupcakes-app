"""Testes da vitrine e do detalhe do produto."""


def test_vitrine_lista_todos_os_produtos(client):
    resposta = client.get("/")
    html = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert "Chocolate Belga" in html
    assert "Red Velvet" in html


def test_filtro_por_categoria_mostra_so_a_categoria(client):
    # Categoria 1 = Clássicos (primeira criada na carga inicial)
    resposta = client.get("/?categoria=1")
    html = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert "Baunilha" in html
    assert "Pistache" not in html  # Pistache é da categoria Especiais


def test_detalhe_do_produto(client):
    resposta = client.get("/produto/1")

    assert resposta.status_code == 200
    assert "Adicionar ao carrinho" in resposta.get_data(as_text=True)


def test_produto_inexistente_retorna_404(client):
    resposta = client.get("/produto/9999")

    assert resposta.status_code == 404
    assert "Página não encontrada" in resposta.get_data(as_text=True)


def test_rota_inexistente_retorna_404(client):
    resposta = client.get("/pagina-que-nao-existe")

    assert resposta.status_code == 404
