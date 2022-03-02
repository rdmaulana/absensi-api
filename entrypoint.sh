#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgress..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

flask db init
flask db migrate -m "initial model"
flask db upgrade

exec "$@"