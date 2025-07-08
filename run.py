from app import create_app

# Cria a instância da aplicação 
app = create_app()

if __name__ == '__main__':
    # Inicia o servidor em modo de depuração (debug=True),
    # o que ajuda a ver erros e reinicia o servidor automaticamente quando você altera o código.
    app.run(debug=True)