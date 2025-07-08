from flask import Blueprint, jsonify, request
from .db import get_db_connection
from datetime import date, time, datetime
from decimal import Decimal

# Cria um Blueprint para organizar as rotas
api = Blueprint('api', __name__)


# --- Endpoint para a Página Home da API ---

@api.route('/', methods=['GET'])
def home():
    """Página inicial da API que lista os recursos disponíveis."""
    doc = {
        "message": "Bem-vindo à API do Projeto de Entregas (PCV)",
        "description": "Esta API gerencia clientes, veículos, rotas e entregas.",
        "recursos_disponiveis": {
            "clientes": "/api/clientes",
            "veiculos": "/api/veiculos",
            "motoristas": "/api/motoristas",
            "depositos": "/api/depositos",
            "rotas": "/api/rotas",
            "entregas": "/api/entregas"
        }
    }
    return jsonify(doc)


# --- Endpoints para Clientes ---

@api.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes cadastrados."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM cadeiraextensao.clientes;')
    
    colunas = [desc[0] for desc in cur.description]
    clientes_com_objetos = [dict(zip(colunas, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()

    # Conversão manual para o tipo Decimal do GPS para evitar erros
    clientes_serializaveis = []
    for cliente in clientes_com_objetos:
        for key, value in cliente.items():
            if isinstance(value, Decimal):
                cliente[key] = float(value)
        clientes_serializaveis.append(cliente)
    
    return jsonify(clientes_serializaveis)


@api.route('/clientes', methods=['POST'])
def add_cliente():
    """Adiciona um novo cliente."""
    novo_cliente = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadeiraextensao.clientes (nome_cliente, endereco_cliente, gps_latitude_cliente, gps_longitude_cliente, telefone_cliente, email_cliente) VALUES (%s, %s, %s, %s, %s, %s) RETURNING cliente_id;',
        (novo_cliente['nome_cliente'], novo_cliente['endereco_cliente'], novo_cliente['gps_latitude_cliente'], novo_cliente['gps_longitude_cliente'], novo_cliente.get('telefone_cliente'), novo_cliente.get('email_cliente'))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Cliente adicionado com sucesso", "id": new_id}), 201

@api.route('/clientes/<int:cliente_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_cliente(cliente_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cur = conn.cursor()

    # --- LÓGICA PARA O MÉTODO GET ---
    if request.method == 'GET':
        cur.execute('SELECT * FROM cadeiraextensao.clientes WHERE cliente_id = %s;', (cliente_id,))
        cliente_obj = cur.fetchone()
        cur.close()
        conn.close()

        if cliente_obj:
            colunas = [desc[0] for desc in cur.description]
            cliente_dict = dict(zip(colunas, cliente_obj))
            for key, value in cliente_dict.items():
                if isinstance(value, Decimal):
                    cliente_dict[key] = float(value)
            return jsonify(cliente_dict)
        else:
            return jsonify({"message": "Cliente não encontrado"}), 404

    # --- LÓGICA PARA O MÉTODO PUT ---
    elif request.method == 'PUT':
        dados_cliente = request.get_json()
        cur.execute(
            """
            UPDATE cadeiraextensao.clientes 
            SET nome_cliente = %s, endereco_cliente = %s, gps_latitude_cliente = %s,
                gps_longitude_cliente = %s, telefone_cliente = %s, email_cliente = %s
            WHERE cliente_id = %s;
            """,
            (
                dados_cliente['nome_cliente'], dados_cliente['endereco_cliente'],
                dados_cliente['gps_latitude_cliente'], dados_cliente['gps_longitude_cliente'],
                dados_cliente['telefone_cliente'], dados_cliente['email_cliente'],
                cliente_id
            )
        )
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()

        if updated_rows > 0:
            return jsonify({"message": f"Cliente {cliente_id} atualizado com sucesso."})
        else:
            return jsonify({"message": "Cliente não encontrado"}), 404

    # --- LÓGICA PARA O MÉTODO DELETE ---
    elif request.method == 'DELETE':
        # Primeiro, apaga as entregas associadas
        cur.execute('DELETE FROM cadeiraextensao.entregas WHERE cliente_id = %s;', (cliente_id,))
        # Em seguida, apaga o cliente
        cur.execute('DELETE FROM cadeiraextensao.clientes WHERE cliente_id = %s;', (cliente_id,))
        
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()

        if updated_rows > 0:
            return jsonify({"message": f"Cliente {cliente_id} e suas dependências foram apagados."})
        else:
            return jsonify({"message": "Cliente não encontrado"}), 404


# --- Endpoints para Depósitos ---

@api.route('/depositos', methods=['GET'])
def get_depositos():
    """Retorna todos os depósitos."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM cadeiraextensao.depositos;')
    
    colunas = [desc[0] for desc in cur.description]
    depositos_com_objetos = [dict(zip(colunas, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()

    # Conversão manual para tipos de dados não-padrão (como Decimal do GPS)
    depositos_serializaveis = []
    for deposito in depositos_com_objetos:
        for key, value in deposito.items():
            if isinstance(value, Decimal):
                deposito[key] = float(value)
        depositos_serializaveis.append(deposito)
    
    return jsonify(depositos_serializaveis)


@api.route('/depositos/<int:deposito_id>', methods=['GET'])
def get_deposito(deposito_id):
    """Retorna um depósito específico."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM cadeiraextensao.depositos WHERE deposito_id = %s;', (deposito_id,))
    
    colunas = [desc[0] for desc in cur.description]
    deposito_obj = cur.fetchone()
    cur.close()
    conn.close()

    if deposito_obj:
        deposito_dict = dict(zip(colunas, deposito_obj))
        # Conversão manual para o tipo Decimal do GPS
        for key, value in deposito_dict.items():
            if isinstance(value, Decimal):
                deposito_dict[key] = float(value)
        return jsonify(deposito_dict)
        
    return jsonify({"message": "Depósito não encontrado"}), 404


@api.route('/depositos', methods=['POST'])
def add_deposito():
    """Adiciona um novo depósito."""
    novo_deposito = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadeiraextensao.depositos (nome_deposito, endereco_deposito, gps_latitude_deposito, gps_longitude_deposito) VALUES (%s, %s, %s, %s) RETURNING deposito_id;',
        (novo_deposito['nome_deposito'], novo_deposito['endereco_deposito'], novo_deposito['gps_latitude_deposito'], novo_deposito['gps_longitude_deposito'])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Depósito adicionado com sucesso", "id": new_id}), 201


@api.route('/depositos/<int:deposito_id>', methods=['PUT'])
def update_deposito(deposito_id):
    """Atualiza os dados de um depósito existente."""
    dados_deposito = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        """
        UPDATE cadeiraextensao.depositos 
        SET nome_deposito = %s, 
            endereco_deposito = %s, 
            gps_latitude_deposito = %s,
            gps_longitude_deposito = %s
        WHERE deposito_id = %s;
        """,
        (
            dados_deposito['nome_deposito'], 
            dados_deposito['endereco_deposito'],
            dados_deposito['gps_latitude_deposito'],
            dados_deposito['gps_longitude_deposito'],
            deposito_id
        )
    )
    
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if updated_rows > 0:
        return jsonify({"message": f"Depósito {deposito_id} atualizado com sucesso."})
    return jsonify({"message": "Depósito não encontrado"}), 404


@api.route('/depositos/<int:deposito_id>', methods=['DELETE'])
def delete_deposito(deposito_id):
    """Apaga um depósito. AVISO: Falhará se o depósito estiver em uso."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    
    # NOTA: Esta operação irá falhar se qualquer veículo ou rota estiver
    # associado a este depósito, devido às restrições de chave estrangeira.
    # Uma implementação mais robusta exigiria primeiro reassociar ou apagar
    # os veículos e rotas dependentes.
    cur.execute('DELETE FROM cadeiraextensao.depositos WHERE deposito_id = %s;', (deposito_id,))
    
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if updated_rows > 0:
        return jsonify({"message": f"Depósito {deposito_id} apagado com sucesso."})
    return jsonify({"message": "Depósito não encontrado ou em uso"}), 404


# --- Endpoints para Veículos ---

@api.route('/veiculos', methods=['GET'])
def get_veiculos():
    """Retorna todos os veículos."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM cadeiraextensao.veiculos;')
    
    # Como não há tipos complexos (data/hora), a conversão direta funciona bem.
    colunas = [desc[0] for desc in cur.description]
    veiculos = [dict(zip(colunas, row)) for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    return jsonify(veiculos)


@api.route('/veiculos/<int:veiculo_id>', methods=['GET'])
def get_veiculo(veiculo_id):
    """Retorna um veículo específico."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM cadeiraextensao.veiculos WHERE veiculo_id = %s;', (veiculo_id,))
    
    veiculo_obj = cur.fetchone()
    cur.close()
    conn.close()

    if veiculo_obj:
        colunas = [desc[0] for desc in cur.description]
        return jsonify(dict(zip(colunas, veiculo_obj)))
        
    return jsonify({"message": "Veículo não encontrado"}), 404


@api.route('/veiculos', methods=['POST'])
def add_veiculo():
    """Adiciona um novo veículo."""
    novo_veiculo = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadeiraextensao.veiculos (placa_veiculo, modelo_veiculo, ano_fabricacao, status_veiculo, deposito_id_base) VALUES (%s, %s, %s, %s, %s) RETURNING veiculo_id;',
        (novo_veiculo['placa_veiculo'], novo_veiculo['modelo_veiculo'], novo_veiculo['ano_fabricacao'], novo_veiculo.get('status_veiculo', 'Disponível'), novo_veiculo.get('deposito_id_base'))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Veículo adicionado com sucesso", "id": new_id}), 201


@api.route('/veiculos/<int:veiculo_id>', methods=['PUT'])
def update_veiculo(veiculo_id):
    """Atualiza os dados de um veículo existente."""
    dados_veiculo = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        """
        UPDATE cadeiraextensao.veiculos 
        SET placa_veiculo = %s, 
            modelo_veiculo = %s, 
            ano_fabricacao = %s,
            status_veiculo = %s,
            deposito_id_base = %s
        WHERE veiculo_id = %s;
        """,
        (
            dados_veiculo['placa_veiculo'], 
            dados_veiculo['modelo_veiculo'],
            dados_veiculo['ano_fabricacao'],
            dados_veiculo['status_veiculo'],
            dados_veiculo['deposito_id_base'],
            veiculo_id
        )
    )
    
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if updated_rows > 0:
        return jsonify({"message": f"Veículo {veiculo_id} atualizado com sucesso."})
    return jsonify({"message": "Veículo não encontrado"}), 404


@api.route('/veiculos/<int:veiculo_id>', methods=['DELETE'])
def delete_veiculo(veiculo_id):
    """Apaga um veículo. AVISO: Falhará se o veículo estiver em uso em uma rota."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    # NOTA: Esta operação irá falhar se este veículo estiver associado a qualquer
    # rota, devido à restrição de chave estrangeira na tabela 'rotas'.
    cur.execute('DELETE FROM cadeiraextensao.veiculos WHERE veiculo_id = %s;', (veiculo_id,))
    
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if updated_rows > 0:
        return jsonify({"message": f"Veículo {veiculo_id} apagado com sucesso."})
    return jsonify({"message": "Veículo não encontrado ou em uso"}), 404


# --- Endpoints para Rotas ---

@api.route('/rotas', methods=['GET'])
def get_rotas():
    """Retorna todas as rotas."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM cadeiraextensao.rotas;')
    
    colunas = [desc[0] for desc in cur.description]
    rotas_com_objetos = [dict(zip(colunas, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()

    # Conversão manual para os tipos date e time, evitando o TypeError
    rotas_serializaveis = []
    for rota in rotas_com_objetos:
        for key, value in rota.items():
            if isinstance(value, (date, time, datetime)):
                rota[key] = value.isoformat()
        rotas_serializaveis.append(rota)
    
    return jsonify(rotas_serializaveis)


@api.route('/rotas/<int:rota_id>', methods=['GET'])
def get_rota(rota_id):
    """Retorna uma rota específica e suas entregas associadas."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    # Busca os detalhes da rota
    cur.execute('SELECT * FROM cadeiraextensao.rotas WHERE rota_id = %s;', (rota_id,))
    
    rota_obj = cur.fetchone()
    if not rota_obj:
        cur.close()
        conn.close()
        return jsonify({"message": "Rota não encontrada"}), 404

    # Converte os dados da rota, tratando os tipos especiais
    colunas_rota = [desc[0] for desc in cur.description]
    rota_json = dict(zip(colunas_rota, rota_obj))
    for key, value in rota_json.items():
        if isinstance(value, (date, time, datetime)):
            rota_json[key] = value.isoformat()

    # Busca as entregas associadas
    cur.execute('SELECT * FROM cadeiraextensao.entregas WHERE rota_id = %s ORDER BY sequencia_na_rota;', (rota_id,))
    colunas_entregas = [desc[0] for desc in cur.description]
    entregas_com_objetos = [dict(zip(colunas_entregas, row)) for row in cur.fetchall()]
    
    # Converte os dados das entregas, tratando os tipos especiais
    entregas_serializaveis = []
    for entrega in entregas_com_objetos:
        for key, value in entrega.items():
            if isinstance(value, (date, time, datetime)):
                entrega[key] = value.isoformat()
        entregas_serializaveis.append(entrega)
    
    rota_json['entregas'] = entregas_serializaveis

    cur.close()
    conn.close()
    return jsonify(rota_json)


@api.route('/rotas', methods=['POST'])
def add_rota():
    """Adiciona uma nova rota."""
    nova_rota = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadeiraextensao.rotas (veiculo_id, motorista_id, deposito_partida_id, deposito_chegada_id, data_rota, horario_saida_previsto, horario_chegada_previsto, status_rota) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING rota_id;',
        (nova_rota['veiculo_id'], nova_rota['motorista_id'], nova_rota['deposito_partida_id'], nova_rota['deposito_chegada_id'], nova_rota['data_rota'], nova_rota.get('horario_saida_previsto'), nova_rota.get('horario_chegada_previsto'), nova_rota.get('status_rota', 'Planejada'))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Rota adicionada com sucesso", "id": new_id}), 201


@api.route('/rotas/<int:rota_id>', methods=['PUT'])
def update_rota(rota_id):
    """Atualiza os dados de uma rota existente."""
    dados_rota = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        """
        UPDATE cadeiraextensao.rotas 
        SET veiculo_id = %s, 
            motorista_id = %s, 
            data_rota = %s,
            status_rota = %s,
            horario_saida_previsto = %s,
            horario_chegada_previsto = %s
        WHERE rota_id = %s;
        """,
        (
            dados_rota['veiculo_id'], 
            dados_rota['motorista_id'],
            dados_rota['data_rota'],
            dados_rota['status_rota'],
            dados_rota.get('horario_saida_previsto'),
            dados_rota.get('horario_chegada_previsto'),
            rota_id
        )
    )
    
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if updated_rows > 0:
        return jsonify({"message": f"Rota {rota_id} atualizada com sucesso."})
    return jsonify({"message": "Rota não encontrada"}), 404


@api.route('/rotas/<int:rota_id>', methods=['DELETE'])
def delete_rota(rota_id):
    """Apaga uma rota e todas as suas entregas associadas."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    # Para manter a integridade dos dados, primeiro apagamos as entregas
    # que pertencem a esta rota.
    cur.execute('DELETE FROM cadeiraextensao.entregas WHERE rota_id = %s;', (rota_id,))
    
    # Em seguida, apagamos a rota principal
    cur.execute('DELETE FROM cadeiraextensao.rotas WHERE rota_id = %s;', (rota_id,))
    
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if updated_rows > 0:
        return jsonify({"message": f"Rota {rota_id} e suas entregas foram apagadas com sucesso."})
    return jsonify({"message": "Rota não encontrada"}), 404


# --- Endpoints para Entregas ---

@api.route('/entregas', methods=['GET'])
def get_entregas():
    """Retorna todas as entregas cadastradas."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM cadeiraextensao.entregas;')
    
    colunas = [desc[0] for desc in cur.description]
    entregas_com_objetos = [dict(zip(colunas, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()

    # Conversão manual para os tipos timestamp
    entregas_serializaveis = []
    for entrega in entregas_com_objetos:
        for key, value in entrega.items():
            if isinstance(value, (datetime, date, time)):
                entrega[key] = value.isoformat()
        entregas_serializaveis.append(entrega)
    
    return jsonify(entregas_serializaveis)

@api.route('/entregas/<int:entrega_id>', methods=['GET'])
def get_entrega(entrega_id):
    """Retorna uma entrega específica."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM cadeiraextensao.entregas WHERE entrega_id = %s;', (entrega_id,))
    
    colunas = [desc[0] for desc in cur.description]
    entrega_obj = cur.fetchone()
    cur.close()
    conn.close()

    if entrega_obj:
        entrega_dict = dict(zip(colunas, entrega_obj))
        for key, value in entrega_dict.items():
            if isinstance(value, (datetime, date, time)):
                entrega_dict[key] = value.isoformat()
        return jsonify(entrega_dict)
        
    return jsonify({"message": "Entrega não encontrada"}), 404

@api.route('/entregas', methods=['POST'])
def add_entrega():
    """Adiciona uma nova entrega a uma rota."""
    nova_entrega = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadeiraextensao.entregas (rota_id, cliente_id, sequencia_na_rota, status_entrega, data_hora_prevista_entrega, observacoes) VALUES (%s, %s, %s, %s, %s, %s) RETURNING entrega_id;',
        (nova_entrega['rota_id'], nova_entrega['cliente_id'], nova_entrega.get('sequencia_na_rota'), nova_entrega.get('status_entrega', 'Pendente'), nova_entrega.get('data_hora_prevista_entrega'), nova_entrega.get('observacoes'))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Entrega adicionada com sucesso", "id": new_id}), 201

@api.route('/entregas/<int:entrega_id>', methods=['PUT'])
def update_entrega(entrega_id):
    """Atualiza os dados de uma entrega (status, observações, etc.)."""
    dados_update = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    # Adicionando a data/hora real da entrega se o status for 'Entregue'
    data_hora_real = 'data_hora_real_entrega = CURRENT_TIMESTAMP' if dados_update.get('status_entrega') == 'Entregue' else 'data_hora_real_entrega = data_hora_real_entrega'

    cur.execute(
        f"""
        UPDATE cadeiraextensao.entregas 
        SET status_entrega = %s, 
            sequencia_na_rota = %s,
            observacoes = %s,
            {data_hora_real}
        WHERE entrega_id = %s;
        """,
        (dados_update.get('status_entrega'), dados_update.get('sequencia_na_rota'), dados_update.get('observacoes'), entrega_id)
    )
    
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if updated_rows > 0:
        return jsonify({"message": f"Entrega {entrega_id} atualizada com sucesso."})
    return jsonify({"message": "Entrega não encontrada"}), 404

@api.route('/entregas/<int:entrega_id>', methods=['DELETE'])
def delete_entrega(entrega_id):
    """Apaga uma entrega específica."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('DELETE FROM cadeiraextensao.entregas WHERE entrega_id = %s;', (entrega_id,))
    
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if updated_rows > 0:
        return jsonify({"message": f"Entrega {entrega_id} apagada com sucesso."})
    return jsonify({"message": "Entrega não encontrada"}), 404


# --- Endpoints para Motoristas ---

@api.route('/motoristas', methods=['GET'])
def get_motoristas():
    """Retorna todos os motoristas."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM cadeiraextensao.motoristas;')
    
    colunas = [desc[0] for desc in cur.description]
    motoristas = [dict(zip(colunas, row)) for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    return jsonify(motoristas)


@api.route('/motoristas/<int:motorista_id>', methods=['GET'])
def get_motorista(motorista_id):
    """Retorna um motorista específico."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute('SELECT * FROM cadeiraextensao.motoristas WHERE motorista_id = %s;', (motorista_id,))
    
    motorista_obj = cur.fetchone()
    cur.close()
    conn.close()

    if motorista_obj:
        colunas = [desc[0] for desc in cur.description]
        return jsonify(dict(zip(colunas, motorista_obj)))
        
    return jsonify({"message": "Motorista não encontrado"}), 404


@api.route('/motoristas', methods=['POST'])
def add_motorista():
    """Adiciona um novo motorista."""
    novo_motorista = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadeiraextensao.motoristas (nome_motorista, cpf_motorista, cnh_motorista, telefone_motorista) VALUES (%s, %s, %s, %s) RETURNING motorista_id;',
        (novo_motorista['nome_motorista'], novo_motorista['cpf_motorista'], novo_motorista['cnh_motorista'], novo_motorista.get('telefone_motorista'))
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Motorista adicionado com sucesso", "id": new_id}), 201


@api.route('/motoristas/<int:motorista_id>', methods=['PUT'])
def update_motorista(motorista_id):
    """Atualiza os dados de um motorista existente."""
    dados_motorista = request.get_json()
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    cur.execute(
        """
        UPDATE cadeiraextensao.motoristas 
        SET nome_motorista = %s, 
            cpf_motorista = %s, 
            cnh_motorista = %s,
            telefone_motorista = %s
        WHERE motorista_id = %s;
        """,
        (
            dados_motorista['nome_motorista'], 
            dados_motorista['cpf_motorista'],
            dados_motorista['cnh_motorista'],
            dados_motorista.get('telefone_motorista'),
            motorista_id
        )
    )
    
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if updated_rows > 0:
        return jsonify({"message": f"Motorista {motorista_id} atualizado com sucesso."})
    return jsonify({"message": "Motorista não encontrado"}), 404


@api.route('/motoristas/<int:motorista_id>', methods=['DELETE'])
def delete_motorista(motorista_id):
    """Apaga um motorista. AVISO: Falhará se o motorista estiver em uso em uma rota."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    # NOTA: Esta operação irá falhar se este motorista estiver associado a qualquer
    # rota, devido à restrição de chave estrangeira na tabela 'rotas'.
    cur.execute('DELETE FROM cadeiraextensao.motoristas WHERE motorista_id = %s;', (motorista_id,))
    
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if updated_rows > 0:
        return jsonify({"message": f"Motorista {motorista_id} apagado com sucesso."})
    return jsonify({"message": "Motorista não encontrado ou em uso"}), 404
