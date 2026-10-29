import os
from flask import Flask, render_template
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

        # Insere categorias e cupcakes iniciais (só na primeira vez)
        from app.seed import popular_produtos
        popular_produtos()

    # Registra os controllers (rotas) – camada C do MVC
    from app.controllers.vitrine import vitrine_bp
    app.register_blueprint(vitrine_bp)


    # Tratamento de erros: páginas amigáveis em vez da tela padrão do servidor
    @app.errorhandler(404)
    def pagina_nao_encontrada(erro):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def erro_interno(erro):
        return render_template("errors/500.html"), 500

    return app