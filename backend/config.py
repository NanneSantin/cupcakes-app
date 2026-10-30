import os

# Pasta do backend (onde este arquivo está)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "cupcakes.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Em HTTPS, o Flask-WTF exige por padrão que o navegador envie o cabeçalho
    # "Referer". Alguns navegadores e configurações de privacidade não enviam,
    # e o formulário era recusado. O token CSRF continua protegendo os formulários.
    WTF_CSRF_SSL_STRICT = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False  # nos testes automáticos o token CSRF é dispensado
