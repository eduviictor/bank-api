#!/bin/bash
# This file is used to run the application inside the container on startup development server.
echo "Instalando dependências"
cd /home/app
make install

echo "Esperando o banco de dados conectar"
postgres_ready() {
poetry run python3 << END
import os
import sys
import asyncio
import asyncpg

db_url = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:postgres@bank-api-postgres:5432/bank-api')
print(db_url)

async def connect():
    try:
        await asyncpg.connect(db_url.replace("+asyncpg", ""))
        print("Conectado ao banco de dados")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(-1)

loop = asyncio.new_event_loop()
loop.run_until_complete(connect())
END
}

until postgres_ready; do
  >&2 echo "PostgreSQL não está disponível ainda - Espere..."
  sleep 1
done

echo "Rodando migrações"
make migrate
export ENVIRONMENT=${ENVIRONMENT:-development}
export PORT=${APP_PORT:-8000}
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=/home/app
make seed
python3 -m poetry run debugpy --listen 0.0.0.0:5676 -m gunicorn "src.main:create_app()" \
    --worker-class uvicorn_workers.RestartableUvicornWorker \
    --bind 0.0.0.0:$PORT \
    --graceful-timeout 0 \
    --timeout 0 \
    --access-logfile - \
    --chdir $PYTHONPATH \
    --reload
