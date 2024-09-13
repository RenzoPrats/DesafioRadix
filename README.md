# Desafio Radix

Este é um projeto que envolve um backend em Django Rest Framework e um frontend em React para a coleta, agregação e visualização de dados de sensores.

## Estrutura do Projeto

- `frontend`: Aplicação frontend desenvolvida em React.
- `backend`: API desenvolvida com Django Rest Framework para manipulação de dados de sensores.

## Configuração

### Requisitos

- [Node.js](https://nodejs.org/)
- [Docker](https://www.docker.com/)

### Frontend

1. Acesse a pasta `frontend`:
    ```bash
    cd frontend
    ```

2. Instale as dependências:
    ```bash
    npm install
    ```

3. Inicie o servidor:
    ```bash
    npm start
    ```

A aplicação estará disponível em [http://localhost:3000](http://localhost:3000).

### Backend

1. Acesse a pasta `backend`:
    ```bash
    cd backend
    ```

2. Inicie o backend utilizando Docker:
    ```bash
    docker-compose up --build
    ```

A API estará disponível em [http://localhost:8000](http://localhost:8000).

### Endpoints da API

- **`POST /sensor-data`**: Enviar dados de sensores.
- **`POST /upload-csv`**: Fazer upload de um arquivo CSV com dados de sensores.
- **`GET /aggregated-data?period=24h`**: Recuperar dados agregados dos sensores para um período (`24h`, `48h`, `1w`, `1m`).
- **`POST /register`**: Registrar um novo usuário.
- **`POST /token`**: Obter token JWT.
- **`POST /token/refresh`**: Atualizar token JWT.

### Testes

Para rodar os testes da API, utilize o comando:
```bash
python manage.py test
