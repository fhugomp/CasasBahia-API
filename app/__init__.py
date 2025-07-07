from flask import Flask

def create_app():
    """Cria e configura uma instância do aplicativo Flask."""
    app = Flask(__name__)

    # Registra o Blueprint que contém as rotas da API
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app