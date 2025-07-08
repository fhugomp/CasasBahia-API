# run.py
from app import create_app

# Cria a instância da nossa aplicação Flask usando a função que definimos em app/__init__.py
app = create_app()

# Esta linha garante que o servidor só vai rodar quando o script for executado diretamente
if __name__ == '__main__':
    # Inicia o servidor em modo de depuração (debug=True),
    # o que ajuda a ver erros e reinicia o servidor automaticamente quando você altera o código.
    app.run(debug=True)