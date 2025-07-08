# API de Gerenciamento de Entregas (Projeto PCV)

Este repositório contém o código-fonte da API RESTful desenvolvida para o Projeto de Programação de Aplicação (PCV), focado em um sistema de gerenciamento de rotas de entrega.

## 🎯 Objetivo do Projeto

O objetivo principal desta API é servir como backend para uma aplicação de visualização de rotas de entrega. Ela gerencia todas as entidades necessárias, como clientes, veículos, motoristas e as próprias rotas, permitindo que uma aplicação cliente (frontend) consuma esses dados para construir mapas, otimizar trajetos e monitorar o status das entregas.

## ✨ Funcionalidades Principais

* Gerenciamento completo (CRUD) de Clientes.
* Gerenciamento de Veículos, Motoristas e Depósitos.
* Criação e consulta de Rotas e suas Entregas associadas.
* Atualização do status de uma Entrega (ex: de 'Pendente' para 'Entregue').
* Página inicial na raiz da API (`/api/`) para descoberta de recursos.
* Redirecionamento da raiz do site (`/`) para a página inicial da API.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **Framework:** Flask
* **Gerenciador de Dependências:** Poetry
* **Banco de Dados:** PostgreSQL (hospedado no AWS RDS)
* **Servidor de Produção:** Gunicorn
* **Hospedagem:** Render

## 🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e rodar a API em um ambiente de desenvolvimento local.

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/fhugomp/CasasBahia-API.git](https://github.com/fhugomp/CasasBahia-API.git)
    ```

    ```bash
    cd CasasBahia-API
    ```

2.  **Instale as Dependências:**
    Certifique-se de ter o [Poetry](https://python-poetry.org/docs/#installation) instalado. Em seguida, execute:
    ```bash
    poetry install
    ```

3.  **Configure as Variáveis de Ambiente:**
    * Crie um arquivo chamado `.env.development` dentro da pasta `app/`.
    * Preencha o arquivo com as credenciais do seu banco de dados de **teste**, usando o exemplo abaixo como modelo:
        ```.env
        # app/.env.development
        DB_TYPE=postgres
        DB_NAME=casasbahia_test
        DB_USER=seu_usuario
        DB_PASSWORD=sua_senha
        DB_HOST=seu_host_do_banco
        DB_PORT=5432
        ```

4.  **Inicie o Servidor:**
    ```bash
    poetry run python run.py
    ```
    A API estará disponível em `http://127.0.0.1:5000`.

## 📚 Documentação da API

A URL base da API é `/api`. Todos os endpoints estão abaixo deste prefixo.

| Entidade | Método | Endpoint | Descrição da Ação |
| :--- | :--- | :--- | :--- |
| **Home** | `GET` | `/api/` | Exibe uma mensagem de boas-vindas e os recursos disponíveis. |
| **Clientes** | `POST` | `/api/clientes` | Cria um novo cliente. |
| | `GET` | `/api/clientes` | Lista todos os clientes. |
| | `GET`, `PUT`, `DELETE` | `/api/clientes/<id>` | Obtém, atualiza ou apaga um cliente específico. |
| **Depósitos**| `POST` | `/api/depositos` | Cria um novo depósito. |
| | `GET` | `/api/depositos` | Lista todos os depósitos. |
| | `GET`, `PUT`, `DELETE` | `/api/depositos/<id>` | Obtém, atualiza ou apaga um depósito específico. |
| **Veículos** | `POST` | `/api/veiculos` | Cria um novo veículo. |
| | `GET` | `/api/veiculos` | Lista todos os veículos. |
| | `GET`, `PUT`, `DELETE` | `/api/veiculos/<id>` | Obtém, atualiza ou apaga um veículo específico. |
| **Motoristas**| `POST` | `/api/motoristas` | Cria um novo motorista. |
| | `GET` | `/api/motoristas` | Lista todos os motoristas. |
| | `GET`, `PUT`, `DELETE`| `/api/motoristas/<id>`| Obtém, atualiza ou apaga um motorista específico. |
| **Rotas** | `POST` | `/api/rotas` | Cria uma nova rota. |
| | `GET` | `/api/rotas` | Lista todas as rotas. |
| | `GET`, `PUT`, `DELETE` | `/api/rotas/<id>` | Obtém, atualiza ou apaga uma rota específica. |
| **Entregas** | `POST` | `/api/entregas` | Adiciona uma entrega a uma rota. |
| | `GET` | `/api/entregas` | Lista todas as entregas. |
| | `GET`, `PUT`, `DELETE`| `/api/entregas/<id>` | Obtém, atualiza ou apaga uma entrega específica. |

*Para detalhes sobre o corpo (body) de cada requisição, consulte o código-fonte em `app/routes.py` ou a documentação completa fornecida à equipe.*

## ☁️ Deploy

Esta API está configurada para deploy contínuo na plataforma [Render](https://render.com/) a partir da branch `main`.
