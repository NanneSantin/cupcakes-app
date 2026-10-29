"""Testes de cadastro, login e logout."""

DADOS_VALIDOS = {
    "nome": "Maria Teste",
    "email": "maria@teste.com",
    "telefone": "(41) 99999-0000",
    "endereco": "Rua das Flores, 100 - Curitiba",
    "senha": "segredo123",
    "confirmacao": "segredo123",
}


def cadastrar(client, **alteracoes):
    dados = {**DADOS_VALIDOS, **alteracoes}
    return client.post("/cadastro", data=dados, follow_redirects=True)


def test_pagina_de_cadastro_abre(client):
    assert client.get("/cadastro").status_code == 200


def test_cadastro_valido_cria_conta_e_faz_login(client):
    resposta = cadastrar(client)
    html = resposta.get_data(as_text=True)

    assert "Cadastro realizado com sucesso" in html
    assert "Sair" in html  # menu mostra a opção de sair


def test_cadastro_com_email_repetido_e_recusado(client):
    cadastrar(client)
    client.get("/logout")
    resposta = cadastrar(client)

    assert resposta.status_code == 400
    assert "já está cadastrado" in resposta.get_data(as_text=True)


def test_cadastro_com_senha_curta_e_recusado(client):
    resposta = cadastrar(client, senha="123", confirmacao="123")

    assert resposta.status_code == 400
    assert "pelo menos 6 caracteres" in resposta.get_data(as_text=True)


def test_cadastro_com_confirmacao_diferente_e_recusado(client):
    resposta = cadastrar(client, confirmacao="outrasenha")

    assert resposta.status_code == 400
    assert "não confere" in resposta.get_data(as_text=True)


def test_cadastro_sem_campos_obrigatorios_e_recusado(client):
    resposta = cadastrar(client, nome="", endereco="")

    assert resposta.status_code == 400
    assert "campos obrigatórios" in resposta.get_data(as_text=True)


def test_login_com_dados_corretos(client):
    cadastrar(client)
    client.get("/logout")
    resposta = client.post(
        "/login",
        data={"email": "maria@teste.com", "senha": "segredo123"},
        follow_redirects=True,
    )

    assert "Olá, Maria Teste" in resposta.get_data(as_text=True)


def test_login_com_senha_errada(client):
    cadastrar(client)
    client.get("/logout")
    resposta = client.post(
        "/login", data={"email": "maria@teste.com", "senha": "errada"}
    )

    assert resposta.status_code == 401
    assert "E-mail ou senha incorretos" in resposta.get_data(as_text=True)


def test_logout(client):
    cadastrar(client)
    resposta = client.get("/logout", follow_redirects=True)

    assert "Você saiu da sua conta" in resposta.get_data(as_text=True)


def test_admin_padrao_consegue_entrar(client):
    resposta = client.post(
        "/login",
        data={"email": "admin@cupcakes.com", "senha": "admin123"},
        follow_redirects=True,
    )

    assert "Olá, Administrador" in resposta.get_data(as_text=True)
