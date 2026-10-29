"""Configuração dos testes: cria a aplicação com um banco em memória."""
import pytest
from app import create_app
from config import TestConfig


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client