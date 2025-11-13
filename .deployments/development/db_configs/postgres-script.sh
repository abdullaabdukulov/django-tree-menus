#!/bin/sh
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  alter role $POSTGRES_USER superuser;
  create extension if not exists "pg_trgm";
  create extension if not exists "uuid-ossp";
EOSQL

exec "$@"