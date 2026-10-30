"""Testes da proteção CSRF (com o token ligado, como no site publicado)."""

import pytest
from app import create_app
from config import TestConfig


class ConfigComCSRF(TestConfig):
    WTF_CSRF_ENABLED = True


@pytest.fixture
def client_csrf():
    app = create_app(ConfigComCSRF)
    with app.test_client() as client:
        yield client


def test_formulario_sem_token_csrf_e_bloqueado(client_csrf):
    resposta = client_csrf.post(
        "/carrinho/adicionar/1", data={"quantidade": 1}, follow_redirects=True
    )
    html = resposta.get_data(as_text=True)

    assert "formulário é inválido" in html
    assert "Seu carrinho está vazio" in client_csrf.get("/carrinho/").get_data(
        as_text=True
    )


def test_paginas_com_formulario_enviam_token_csrf(client_csrf):
    for pagina in ["/", "/produto/1", "/login", "/cadastro"]:
        html = client_csrf.get(pagina).get_data(as_text=True)
        assert 'name="csrf_token"' in html, pagina


def test_https_sem_referer_com_token_valido_e_aceito(client_csrf):
    """Simula um navegador que não envia o cabeçalho Referer em HTTPS."""
    import re

    html = client_csrf.get("/", base_url="https://localhost").get_data(as_text=True)
    token = re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)

    resposta = client_csrf.post(
        "/carrinho/adicionar/1",
        base_url="https://localhost",
        data={"quantidade": 1, "csrf_token": token, "proxima": "/"},
    )

    assert resposta.status_code == 302
    assert resposta.headers["Location"] == "/"
    html = client_csrf.get("/carrinho/", base_url="https://localhost").get_data(
        as_text=True
    )
    assert "Baunilha" in html
