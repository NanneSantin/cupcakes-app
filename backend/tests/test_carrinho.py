"""Testes do carrinho de compras."""


def test_carrinho_vazio(client):
    resposta = client.get("/carrinho/")

    assert resposta.status_code == 200
    assert "Seu carrinho está vazio" in resposta.get_data(as_text=True)


def test_adicionar_produto(client):
    resposta = client.post(
        "/carrinho/adicionar/1", data={"quantidade": 2}, follow_redirects=True
    )
    html = resposta.get_data(as_text=True)

    assert "adicionado ao carrinho" in html
    assert "Baunilha" in html
    assert "R$ 19,80" in html  # 2 x R$ 9,90


def test_adicionar_o_mesmo_produto_soma_quantidade(client):
    client.post("/carrinho/adicionar/1", data={"quantidade": 1})
    resposta = client.post(
        "/carrinho/adicionar/1", data={"quantidade": 2}, follow_redirects=True
    )

    assert "R$ 29,70" in resposta.get_data(as_text=True)  # 3 x R$ 9,90


def test_quantidade_nao_passa_do_estoque(client):
    resposta = client.post(
        "/carrinho/adicionar/1", data={"quantidade": 999}, follow_redirects=True
    )

    # Estoque inicial é 50 -> 50 x R$ 9,90 = R$ 495,00
    assert "R$ 495,00" in resposta.get_data(as_text=True)


def test_atualizar_quantidade(client):
    client.post("/carrinho/adicionar/1", data={"quantidade": 1})
    resposta = client.post(
        "/carrinho/atualizar/1", data={"quantidade": 4}, follow_redirects=True
    )

    assert "R$ 39,60" in resposta.get_data(as_text=True)  # 4 x R$ 9,90


def test_remover_produto(client):
    client.post("/carrinho/adicionar/1", data={"quantidade": 1})
    resposta = client.post("/carrinho/remover/1", follow_redirects=True)

    assert "Seu carrinho está vazio" in resposta.get_data(as_text=True)


def test_total_com_varios_produtos(client):
    client.post("/carrinho/adicionar/1", data={"quantidade": 1})  # Baunilha R$ 9,90
    resposta = client.post(
        "/carrinho/adicionar/2", data={"quantidade": 1}, follow_redirects=True
    )  # Chocolate R$ 11,90

    assert "R$ 21,80" in resposta.get_data(as_text=True)


def test_adicionar_produto_inexistente_retorna_404(client):
    assert client.post("/carrinho/adicionar/9999").status_code == 404


def test_adicionar_pela_vitrine_continua_na_vitrine(client):
    resposta = client.post(
        "/carrinho/adicionar/1", data={"quantidade": 1, "proxima": "/?categoria=1"}
    )

    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/?categoria=1"


def test_vitrine_tem_botao_de_adicionar_ao_carrinho(client):
    html = client.get("/").get_data(as_text=True)

    assert 'action="/carrinho/adicionar/1"' in html


def test_redirecionamento_externo_e_ignorado(client):
    resposta = client.post(
        "/carrinho/adicionar/1",
        data={"quantidade": 1, "proxima": "//site-malicioso.com"},
    )

    assert resposta.headers["Location"] == "/carrinho/"
