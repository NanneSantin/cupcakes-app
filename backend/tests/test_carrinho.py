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


# ---------- Respostas para o JavaScript (sem recarregar a página) ----------

JS = {"X-Requested-With": "fetch"}


def test_adicionar_pelo_javascript_responde_json(client):
    resposta = client.post("/carrinho/adicionar/1", data={"quantidade": 3}, headers=JS)
    dados = resposta.get_json()

    assert resposta.status_code == 200
    assert dados["qtd_carrinho"] == 3
    assert "adicionado ao carrinho" in dados["mensagem"]


def test_atualizar_pelo_javascript_recalcula_valores(client):
    client.post("/carrinho/adicionar/1", data={"quantidade": 1})  # Baunilha R$ 9,90
    client.post("/carrinho/adicionar/2", data={"quantidade": 1})  # Chocolate R$ 11,90
    dados = client.post(
        "/carrinho/atualizar/1", data={"quantidade": 3}, headers=JS
    ).get_json()

    assert dados["quantidade"] == 3
    assert dados["subtotal"] == "R$ 29,70"  # 3 x 9,90
    assert dados["total"] == "R$ 41,60"  # 29,70 + 11,90
    assert dados["qtd_carrinho"] == 4


def test_atualizar_com_quantidade_invalida_e_recusado(client):
    client.post("/carrinho/adicionar/1", data={"quantidade": 2})
    resposta = client.post("/carrinho/atualizar/1", data={"quantidade": 0}, headers=JS)
    dados = resposta.get_json()

    assert resposta.status_code == 400
    assert "Quantidade inválida" in dados["mensagem"]
    assert dados["quantidade"] == 2  # continua com a quantidade anterior


def test_seletor_de_quantidade_aparece_na_vitrine(client):
    html = client.get("/").get_data(as_text=True)

    assert 'data-acao="diminuir"' in html
    assert 'data-acao="aumentar"' in html


# ---------- Validação da quantidade no servidor ----------


def test_adicionar_com_quantidade_invalida_e_recusado(client):
    for valor in ["0", "-5", "abc", ""]:
        resposta = client.post(
            "/carrinho/adicionar/1", data={"quantidade": valor}, headers=JS
        )

        assert resposta.status_code == 400, valor
        assert "Quantidade inválida" in resposta.get_json()["mensagem"]

    # Nada foi adicionado ao carrinho
    assert "Seu carrinho está vazio" in client.get("/carrinho/").get_data(as_text=True)


def test_adicionar_quantidade_invalida_sem_javascript_mostra_erro(client):
    resposta = client.post(
        "/carrinho/adicionar/1",
        data={"quantidade": "-5", "proxima": "/produto/1"},
        follow_redirects=True,
    )

    assert "Quantidade inválida" in resposta.get_data(as_text=True)
