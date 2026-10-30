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


def test_atualizar_nao_aceita_quantidade_menor_que_1(client):
    client.post("/carrinho/adicionar/1", data={"quantidade": 2})
    dados = client.post(
        "/carrinho/atualizar/1", data={"quantidade": 0}, headers=JS
    ).get_json()

    assert dados["quantidade"] == 1


def test_seletor_de_quantidade_aparece_na_vitrine(client):
    html = client.get("/").get_data(as_text=True)

    assert 'data-acao="diminuir"' in html
    assert 'data-acao="aumentar"' in html
