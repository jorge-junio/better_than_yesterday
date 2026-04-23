#!/bin/sh
set -e

# Aplica as migrações no boot da aplicação.
python manage.py migrate_schemas --noinput

exec "$@"
