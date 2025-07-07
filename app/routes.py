# app/routes.py
from flask import Blueprint, jsonify, request
from .db import get_db_connection

# Cria um Blueprint para organizar as rotas
api = Blueprint('api', __name__)

# --- Endpoints para Clientes ---

@api.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes cadastrados."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM clientes;')
        clientes = cur.fetchall()
        cur.close()
        conn.close()
        # Converte o resultado para uma lista de dicionários
        return jsonify([dict(zip([desc[0] for desc in cur.description], row)) for row in clientes])
    return jsonify({"error": "Database connection failed"}), 500

@api.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    """Retorna um cliente específico pelo seu ID."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM clientes WHERE id = %s;', (id,))
        cliente = cur.fetchone()
        cur.close()
        conn.close()
        if cliente:
            return jsonify(dict(zip([desc[0] for desc in cur.description], cliente)))
        return jsonify({"message": "Cliente não encontrado"}), 404
    return jsonify({"error": "Database connection failed"}), 500

@api.route('/clientes', methods=['POST'])
def add_cliente():
    """Adiciona um novo cliente."""
    novo_cliente = request.get_json()
    # Adicione validação dos dados recebidos aqui
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO clientes (nome, endereco, gps) VALUES (%s, %s, %s) RETURNING id;',
                    (novo_cliente['nome'], novo_cliente['endereco'], novo_cliente['gps']))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Cliente adicionado com sucesso", "id": new_id}), 201
    return jsonify({"error": "Database connection failed"}), 500

# Adicione aqui os endpoints para Veículos, Entregas, Rotas e Depósito, seguindo a mesma lógica.
# Por exemplo: GET /veiculos, POST /entregas, GET /rotas/veiculo/<id_veiculo>