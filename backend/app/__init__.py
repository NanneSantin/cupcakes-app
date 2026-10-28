import os
from flask import Flask
from config import Config
from app.models import db

# Caminho da pasta frontend (dois níveis acima: backend/app -> raiz do projeto)
RAIZ_PROJETO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FRONTEND = os.path.join(RAIZ_PROJETO, "frontend")


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=os.path.join(FRONTEND, "templates"),
        static_folder=os.path.join(FRONTEND, "static"),
    )
    app.config.from_object(config_class)

    # Liga o banco de dados à aplicação
    db.init_app(app)

    # Cria as tabelas na primeira execução (se ainda não existirem)
    with app.app_context():
        db.create_all()

    # Rota provisória só para confirmar que o servidor está funcionando.
    # Será substituída pela vitrine nos próximos commits.
    @app.route("/")
    def status():
        return "Servidor Cupcakes Gourmet funcionando!"

    return app