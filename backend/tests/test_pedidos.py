"""Testes do checkout, pagamento simulado e acompanhamento de pedidos."""

from app.models import db, Produto

CLIENTE = {
    "nome": "Maria Teste",
    "email": "maria@teste.com",
    "telefone": "",
    "endereco": "Rua das Flores, 100",
    "senha": "segredo123",
    "confirmacao": "segredo123",
}
CARTAO_VALIDO = {
    "numero": "4111 1111 1111 1111",
    "nome": "MARIA TESTE",
    "validade": "12/30",
    "cvv": "123",
}


def logar_cliente(client, **dados):
    client.post("/cadastro", data={**CLIENTE, **dados})


def fazer_pedido(client, forma="PIX"):
    client.post("/carrinho/adicionar/1", data={"quantidade": 2})  # 2 x Baunilha R$ 9,90
    return client.post(
        "/pedidos/checkout",
        data={"endereco": "Rua das Flores, 100", "forma_pagamento": forma},
    )


def test_checkout_exige_login(client):
    resposta = client.get("/pedidos/checkout")

    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_checkout_com_carrinho_vazio_volta_ao_carrinho(client):
    logar_cliente(client)
    resposta = client.get("/pedidos/checkout")

    assert resposta.status_code == 302
    assert "/carrinho" in resposta.headers["Location"]


def test_checkout_sem_forma_de_pagamento_e_recusado(client):
    logar_cliente(client)
    client.post("/carrinho/adicionar/1", data={"quantidade": 1})
    resposta = client.post(
        "/pedidos/checkout", data={"endereco": "Rua A, 1", "forma_pagamento": ""}
    )

    assert resposta.status_code == 400
    assert "Escolha a forma de pagamento" in resposta.get_data(as_text=True)


def test_checkout_cria_pedido_esvazia_carrinho_e_baixa_estoque(client):
    logar_cliente(client)
    resposta = fazer_pedido(client)

    assert resposta.status_code == 302
    assert "/pedidos/1/pagamento" in resposta.headers["Location"]
    assert "Seu carrinho está vazio" in client.get("/carrinho/").get_data(as_text=True)
    with client.application.app_context():
        assert db.session.get(Produto, 1).estoque == 48  # 50 - 2


def test_pagamento_pix_aprova_pedido(client):
    logar_cliente(client)
    fazer_pedido(client, "PIX")
    resposta = client.post("/pedidos/1/pagamento", follow_redirects=True)
    html = resposta.get_data(as_text=True)

    assert "Pagamento aprovado" in html
    assert "R$ 19,80" in html


def test_pagamento_cartao_valido_aprova_pedido(client):
    logar_cliente(client)
    fazer_pedido(client, "CARTAO")
    resposta = client.post(
        "/pedidos/1/pagamento", data=CARTAO_VALIDO, follow_redirects=True
    )

    assert "Pagamento aprovado" in resposta.get_data(as_text=True)


def test_pagamento_cartao_com_dados_invalidos(client):
    logar_cliente(client)
    fazer_pedido(client, "CARTAO")
    resposta = client.post(
        "/pedidos/1/pagamento",
        data={**CARTAO_VALIDO, "numero": "1234", "validade": "13/30"},
    )
    html = resposta.get_data(as_text=True)

    assert resposta.status_code == 400
    assert "16 dígitos" in html
    assert "MM/AA" in html


def test_pagamento_cartao_recusado(client):
    logar_cliente(client)
    fazer_pedido(client, "CARTAO")
    resposta = client.post(
        "/pedidos/1/pagamento", data={**CARTAO_VALIDO, "numero": "4111111111110000"}
    )

    assert resposta.status_code == 402
    assert "Pagamento recusado" in resposta.get_data(as_text=True)


def test_meus_pedidos_lista_o_pedido(client):
    logar_cliente(client)
    fazer_pedido(client)
    html = client.get("/pedidos/").get_data(as_text=True)

    assert "Pedido #1" in html
    assert "Aguardando pagamento" in html


def test_cliente_nao_ve_pedido_de_outro_cliente(client):
    logar_cliente(client)
    fazer_pedido(client)
    client.get("/logout")
    logar_cliente(client, email="outra@teste.com")

    assert client.get("/pedidos/1").status_code == 404
