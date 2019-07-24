#!/bin/sh
set -e

python manage.py migrate
python manage.py collectstatic --noinput
gunicorn test_assignment.wsgi:application -b 0.0.0.0:$PORT --workers=3 --log-file=-
