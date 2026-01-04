#!/usr/bin/env bash
set -e

# apply migration tiap container start (aman untuk dev)
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

# jalanin server
python manage.py runserver 0.0.0.0:8000
