#!/bin/sh

echo "Starting the Django application setup..."

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting the Gunicorn server..."
exec gunicorn --bind :8888 didar.wsgi:application
