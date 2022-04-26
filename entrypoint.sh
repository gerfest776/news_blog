#!/bin/bash

echo "Waiting for postgres..."
while ! nc -z database 5432; do
  sleep 0.1
done

echo "Collect static files"

echo yes | python manage.py collectstatic


echo "PostgreSQL started"

python manage.py migrate

echo "
O——————————————————O
     LIIS_test started…
O——————————————————O
"
exec "$@"