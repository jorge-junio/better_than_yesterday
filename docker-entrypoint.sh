#!/bin/sh
set -e

# Aguarda o Postgres aceitar conexões antes de tentar migrar.
python - <<'PY'
import os
import socket
import sys
import time

host = os.getenv("DB_HOST", "172.17.0.1")
port = int(os.getenv("DB_PORT", "5432"))
deadline = time.time() + 120

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        if time.time() >= deadline:
            print(f"Postgres indisponível em {host}:{port} após 120s.", file=sys.stderr)
            sys.exit(1)
        time.sleep(2)
PY

# Aplica as migrações no boot da aplicação.
python manage.py migrate_schemas --noinput

exec "$@"
