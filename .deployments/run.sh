#!/bin/bash

set -e

cd /code

PROCESS_TYPE=$1

case $PROCESS_TYPE in
    app)
        python manage.py collectstatic --noinput
        python manage.py migrate
        gunicorn \
            --bind 0.0.0.0:8000 \
            --workers 4 \
            --timeout 300 \
            --graceful-timeout 10 \
            --log-level info \
            --access-logfile "-" \
            --error-logfile "-" \
            config.wsgi:application \

        exit 1
        ;;
    test)
        python manage.py migrate
        python manage.py test
        exit 1
        ;;
esac

exec "$@"