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
