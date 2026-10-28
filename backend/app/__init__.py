import os
from flask import Flask
from config import Config

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

    # Rota provisória só para confirmar que o servidor está funcionando.
    # Será substituída pela vitrine nos próximos commits.
    @app.route("/")
    def status():
        return "Servidor Cupcakes Gourmet funcionando!"

    return app