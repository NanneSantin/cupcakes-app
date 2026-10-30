"""Testes do painel do administrador."""

from app.models import db, Produto, Pedido

CLIENTE = {
    "nome": "Maria Teste",
    "email": "maria@teste.com",
    "telefone": "",
    "endereco": "Rua das Flores, 100 - Centro, Curitiba",
    "senha": "segredo123",
    "confirmacao": "segredo123",
}


def cliente_faz_pedido(client):
    client.post("/cadastro", data=CLIENTE)
    client.post("/carrinho/adicionar/1", data={"quantidade": 2})
    client.post(
        "/pedidos/checkout",
        data={
            "endereco": "Rua das Flores, 100 - Centro, Curitiba",
            "forma_pagamento": "PIX",
        },
    )
    client.post("/pedidos/1/pagamento")
    client.get("/logout")


def entrar_como_admin(client):
    client.post("/login", data={"email": "admin@cupcakes.com", "senha": "admin123"})


def test_painel_exige_login(client):
    resposta = client.get("/admin/pedidos")

    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_cliente_comum_nao_acessa_painel(client):
    client.post("/cadastro", data=CLIENTE)
    resposta = client.get("/admin/pedidos")

    assert resposta.status_code == 403
    assert "Acesso negado" in resposta.get_data(as_text=True)


def test_admin_ve_todos_os_pedidos(client):
    cliente_faz_pedido(client)
    entrar_como_admin(client)
    html = client.get("/admin/pedidos").get_data(as_text=True)

    assert "#1" in html
    assert "Maria Teste" in html


def test_admin_altera_status_e_cliente_ve_a_mudanca(client):
    cliente_faz_pedido(client)
    entrar_como_admin(client)
    client.post("/admin/pedidos/1/status", data={"status": "Saiu para entrega"})
    client.get("/logout")

    client.post("/login", data={"email": CLIENTE["email"], "senha": CLIENTE["senha"]})
    html = client.get("/pedidos/").get_data(as_text=True)
    assert "Saiu para entrega" in html


def test_status_invalido_e_recusado(client):
    cliente_faz_pedido(client)
    entrar_como_admin(client)
    resposta = client.post(
        "/admin/pedidos/1/status", data={"status": "Inventado"}, follow_redirects=True
    )

    assert "Status inválido" in resposta.get_data(as_text=True)


def test_cancelar_devolve_produtos_ao_estoque(client):
    cliente_faz_pedido(client)  # 2 unidades -> estoque 48
    entrar_como_admin(client)
    client.post("/admin/pedidos/1/status", data={"status": "Cancelado"})

    with client.application.app_context():
        assert db.session.get(Produto, 1).estoque == 50
        assert db.session.get(Pedido, 1).status == "Cancelado"


def test_pedido_cancelado_nao_pode_ser_reaberto(client):
    cliente_faz_pedido(client)
    entrar_como_admin(client)
    client.post("/admin/pedidos/1/status", data={"status": "Cancelado"})
    client.post("/admin/pedidos/1/status", data={"status": "Pago"})

    with client.application.app_context():
        assert db.session.get(Pedido, 1).status == "Cancelado"
        assert db.session.get(Produto, 1).estoque == 50  # não mexeu no estoque de novo


def test_alterar_status_volta_para_o_painel_com_o_filtro(client):
    cliente_faz_pedido(client)
    entrar_como_admin(client)
    resposta = client.post(
        "/admin/pedidos/1/status",
        data={"status": "Em preparo", "proxima": "/admin/pedidos?status=Pago"},
    )

    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/admin/pedidos?status=Pago"


def test_alterar_status_sem_destino_volta_para_o_painel(client):
    cliente_faz_pedido(client)
    entrar_como_admin(client)
    resposta = client.post("/admin/pedidos/1/status", data={"status": "Em preparo"})

    assert resposta.headers["Location"] == "/admin/pedidos"
