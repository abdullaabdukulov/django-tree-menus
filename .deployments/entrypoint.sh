#!/bin/bash

set -e
set -o errexit
# set -o pipefail
set -o nounset

postgres_ready() {
    python << END
import sys
from psycopg2 import connect
from psycopg2.errors import OperationalError
try:
    connect(
        dbname="${DB_NAME}",
        user="${DB_USER}",
        password="${DB_PASSWORD}",
        host="${DB_HOST}",
        port="${DB_PORT}",
    )
except OperationalError:
    sys.exit(-1)
END
}

until postgres_ready; do
  >&2 echo "Waiting for PostgreSQL to become available..."
  sleep 5
done
>&2 echo "PostgreSQL is available"
exec "$@"