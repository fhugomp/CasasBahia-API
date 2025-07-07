from flask import Flask, jsonify

app = Flask(__name__)

deposito = {
    "nome": "Centro de Distribuição Casas Bahia - Fortaleza",
    "endereco": "Av. dos Expedicionários, 5720, Montese, Fortaleza-CE",
    "gps": {"latitude": -3.7689, "longitude": -38.5432}
}

clientes = [
    {"id_cliente": 1, "nome": "Júlia Mendes", "endereco": "Rua das Flores, 10, Aldeota", "gps": {"latitude": -3.7327, "longitude": -38.5233}},
    {"id_cliente": 2, "nome": "Carlos Eduardo", "endereco": "Av. Beira Mar, 2500, Meireles", "gps": {"latitude": -3.7258, "longitude": -38.4919}},
    {"id_cliente": 3, "nome": "Mariana Costa", "endereco": "Rua Barão do Rio Branco, 1000, Centro", "gps": {"latitude": -3.7271, "longitude": -38.5267}},
    # Adicionar os outros 47 clientes aqui para completar 50...
]

# a) Uso de 4 a 6 veículos por dia, de um total de 8 [cite: 108]
veiculos = [
    {"id_veiculo": "FROTA-01", "modelo": "Fiat Fiorino", "motorista_escala": {"dia_1": "João Silva", "dia_2": "Pedro Alves"}},
    {"id_veiculo": "FROTA-02", "modelo": "Renault Kangoo", "motorista_escala": {"dia_1": "Ana Pereira", "dia_2": "Carlos Lima"}},
    {"id_veiculo": "FROTA-03", "modelo": "Fiat Ducato", "motorista_escala": {"dia_1": "Márcia Souza", "dia_2": "José Santos"}},
    {"id_veiculo": "FROTA-04", "modelo": "Mercedes-Benz Sprinter", "motorista_escala": {"dia_1": "Bia Rodrigues", "dia_2": "Tiago Ferreira"}},
    # Adicionar os outros veículos para completar 8...
]

rotas_diarias = [
    {
        "data": "2025-07-08", # Simulação para o dia seguinte à data atual
        "rotas": [
            {
                "id_veiculo": "FROTA-01",
                "motorista": "João Silva",
                "sequencia_entrega": [
                    {"id_cliente": 2, "ordem": 1},
                    {"id_cliente": 3, "ordem": 2}
                ]
            },
            {
                "id_veiculo": "FROTA-02",
                "motorista": "Ana Pereira",
                "sequencia_entrega": [
                    {"id_cliente": 1, "ordem": 1}
                ]
            }
            # Adicionar as rotas dos outros veículos do dia...
        ]
    }
    # Adicionar os dados para as 2 semanas de simulação... [cite: 112]
]

# CRIAÇÃO DOS ENDPOINTS DA API

@app.route('/')
def home():
    return "Bem-vindo à API do Projeto PCV Casas Bahia! Acesse os endpoints /api/clientes, /api/veiculos, /api/deposito, /api/rotas."

@app.route('/api/deposito', methods=['GET'])
def get_deposito():
    return jsonify(deposito)

@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    return jsonify(clientes)

@app.route('/api/veiculos', methods=['GET'])
def get_veiculos():
    return jsonify(veiculos)

@app.route('/api/rotas', methods=['GET'])
def get_rotas():
    return jsonify(rotas_diarias)

# EXECUÇÃO DA APLICAÇÃO
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')