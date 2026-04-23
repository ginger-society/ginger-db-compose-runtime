#!/bin/bash

sleep 5

DB_NAME=${DB_NAME:-"test"}
PSQL_USER=${DB_USERNAME:-"postgres"}
PSQL_PASSWORD=${DB_PASSWORD:-"postgres"}
PSQL_HOST=${DB_HOST:-""}
PSQL_PORT=${DB_PORT:-"5432"}

export PGPASSWORD=$PSQL_PASSWORD
export DJANGO_SETTINGS_MODULE=server.settings

# -----------------------------------
# 👉 ONLY RUN POSTGRES LOGIC IF HOST EXISTS
# -----------------------------------
if [ -z "$PSQL_HOST" ]; then
    echo "No PSQL_HOST provided. Skipping Postgres setup..."
    python3 manage.py migrate
    python3 manage.py runserver 0.0.0.0:8000 --noreload
    exit 0
fi

echo "Postgres detected at $PSQL_HOST:$PSQL_PORT"

if ! psql -U "$PSQL_USER" -h "$PSQL_HOST" -p "$PSQL_PORT" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    createdb -U "$PSQL_USER" -h "$PSQL_HOST" -p "$PSQL_PORT" "$DB_NAME"
    echo "Database $DB_NAME created."
else
    echo "Database $DB_NAME already exists."
fi

unset PGPASSWORD

python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000 --noreload