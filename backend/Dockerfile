# Usa uma imagem leve e oficial do Python 3.10
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Variáveis de ambiente para otimização do Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema necessárias para o psycopg2 (PostgreSQL) e compilação
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia o requirements primeiro (Aproveita o cache do Docker se as libs não mudarem)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do backend para o container
COPY . .

# Comando matador para Produção:
# O Render injeta a porta dinamicamente na variável $PORT. 
# O Gunicorn vai escutar nessa porta rodando a nossa aplicação Flask.
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} wsgi:app