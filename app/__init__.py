from flask import Flask, redirect, url_for

def create_app():
    """Cria e configura uma instância do aplicativo Flask."""
    app = Flask(__name__)

    # Registra o Blueprint que contém as rotas da API
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    # --- ROTA DE REDIRECIONAMENTO ---
    # Esta rota captura acessos à raiz do site (ex: https://casasbahia-api.onrender.com/)
    @app.route('/')
    def index_redirect():
        # E redireciona para a página home da sua API ('/api/')
        # url_for('api.home') encontra dinamicamente o link para a função 'home'
        # dentro do blueprint 'api'.
        return redirect(url_for('api.home'))
    # --------------------------------

    return app